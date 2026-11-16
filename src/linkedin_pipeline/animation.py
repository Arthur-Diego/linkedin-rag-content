"""Animated diagram renderer: queued post -> HTML scene -> frames (Playwright) -> GIF (ffmpeg).

Runs on the author's machine only; the workflow publishes the committed GIF (ADR-010).
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

DEFAULT_ASSETS = Path(__file__).resolve().parents[2] / "assets"
DEFAULT_SCENE = "flow"
WIDTH, HEIGHT = 1080, 1350     # 4:5, the tallest ratio the LinkedIn feed shows uncropped
FPS = 15
MAX_FRAMES = 250               # LinkedIn Images API: "GIF format supports up to 250 frames"
MAX_GRID = (4, 4)              # columns, rows the flow scene can lay out legibly
PACKET_KINDS = {"info", "ok", "bad", "warn"}
MAX_TALLY_LABEL = 18           # two tallies sit side by side; longer labels overlap


class AnimationError(RuntimeError):
    pass


def spec_of(post) -> dict:
    spec = post.meta.get("animation")
    if not isinstance(spec, dict):
        raise AnimationError(f"post {post.id} has no animation block")
    return spec


def scene_name(spec: dict) -> str:
    return str(spec.get("scene") or DEFAULT_SCENE)


def validate(spec: dict) -> None:
    """Check a flow-scene spec; custom scenes (animation.scene) validate themselves."""
    if scene_name(spec) != DEFAULT_SCENE:
        return
    for key in ("title", "nodes", "steps"):
        if not spec.get(key):
            raise AnimationError(f"animation.{key} is required")

    ids: set[str] = set()
    cells: set[tuple] = set()
    for node in spec["nodes"]:
        node_id, at = node.get("id"), node.get("at")
        if not node_id or not node.get("label"):
            raise AnimationError(f"node needs id and label: {node}")
        if node_id in ids:
            raise AnimationError(f"duplicate node id: {node_id}")
        if (not isinstance(at, list) or len(at) != 2
                or not all(isinstance(v, int) and 0 <= v < limit
                           for v, limit in zip(at, MAX_GRID))):
            raise AnimationError(
                f"node {node_id}: 'at' must be [column, row] within a "
                f"{MAX_GRID[0]}x{MAX_GRID[1]} grid")
        if tuple(at) in cells:
            raise AnimationError(f"node {node_id}: grid cell {at} is already taken")
        ids.add(node_id)
        cells.add(tuple(at))

    def known(node_id, where: str) -> None:
        if node_id not in ids:
            raise AnimationError(f"{where}: unknown node '{node_id}'")

    for edge in spec.get("edges") or []:
        known(edge.get("from"), "edge")
        known(edge.get("to"), "edge")
    for kind, label in (spec.get("tally") or {}).items():
        if kind not in PACKET_KINDS:
            raise AnimationError(f"tally: kind must be one of {sorted(PACKET_KINDS)}")
        if len(str(label)) > MAX_TALLY_LABEL:
            raise AnimationError(
                f"tally label '{label}' is longer than {MAX_TALLY_LABEL} characters")
    for number, step in enumerate(spec["steps"], start=1):
        where = f"step {number}"
        if not step.get("caption"):
            raise AnimationError(f"{where}: caption is required")
        for group in step.get("packets") or []:
            path = group.get("path") or []
            if len(path) < 2:
                raise AnimationError(f"{where}: packet path needs at least 2 nodes")
            for node_id in path:
                known(node_id, where)
            if group.get("kind", "info") not in PACKET_KINDS:
                raise AnimationError(
                    f"{where}: packet kind must be one of {sorted(PACKET_KINDS)}")
        for node_id in step.get("meters") or {}:
            known(node_id, where)


def build_html(post, assets_dir: Path = DEFAULT_ASSETS) -> str:
    """Fill the scene template with the post's animation spec."""
    spec = spec_of(post)
    validate(spec)
    scene = assets_dir / "scenes" / f"{scene_name(spec)}.html"
    if not scene.is_file():
        raise AnimationError(f"scene not found: {scene}")
    payload = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    return (scene.read_text(encoding="utf-8")
            .replace("{{ASSETS}}", assets_dir.resolve().as_uri())
            .replace("{{SPEC}}", payload))


def _capture_frames(html_file: Path, frames_dir: Path) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise AnimationError(f"playwright not installed: {exc}") from exc
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
            page.goto(html_file.as_uri() + "#capture")
            page.wait_for_function("typeof window.renderAt === 'function'", timeout=30_000)
            page.evaluate("document.fonts.ready.then(() => true)")
            duration = float(page.evaluate("window.DURATION"))
            total = math.ceil(duration * FPS - 1e-6)
            if not 0 < total <= MAX_FRAMES:
                raise AnimationError(
                    f"animation lasts {duration:.1f}s = {total} frames at {FPS} fps; "
                    f"LinkedIn accepts at most {MAX_FRAMES} "
                    f"(keep it under {MAX_FRAMES / FPS:.1f}s)")
            for i in range(total):
                page.evaluate("t => window.renderAt(t)", i / FPS)
                page.screenshot(path=str(frames_dir / f"f_{i:04d}.png"))
            browser.close()
    except AnimationError:
        raise
    except Exception as exc:
        raise AnimationError(f"frame capture failed: {exc}") from exc
    return total


def _ffmpeg(args: list[str]) -> None:
    result = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise AnimationError(f"ffmpeg failed: {result.stderr.strip()[:500]}")


def render_gif(post, out_path: Path, assets_dir: Path = DEFAULT_ASSETS,
               mp4_path: Path | None = None) -> int:
    """Render the post's animation to a looping GIF; returns the frame count."""
    if shutil.which("ffmpeg") is None:
        raise AnimationError("ffmpeg not found on PATH (macOS: brew install ffmpeg)")
    page_html = build_html(post, assets_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / "scene.html"
        html_file.write_text(page_html, encoding="utf-8")
        frames_dir = Path(tmp) / "frames"
        frames_dir.mkdir()
        total = _capture_frames(html_file, frames_dir)
        source = ["-framerate", str(FPS), "-i", str(frames_dir / "f_%04d.png")]
        _ffmpeg([*source, "-vf",
                 "split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];"
                 "[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                 "-loop", "0", str(out_path)])
        if mp4_path is not None:
            _ffmpeg([*source, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                     str(mp4_path)])
    return total
