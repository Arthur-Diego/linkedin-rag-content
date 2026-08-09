"""Primary card renderer: gpt-image-2 infographic built from the post's diagram spec."""

from __future__ import annotations

import base64
from pathlib import Path

import requests

OPENAI_API = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-2"
SIZE = "1088x1360"  # exact 4:5 portrait, multiples of 16
DEFAULT_QUALITY = "high"

PROMPT_TEMPLATE = """\
Create a professional technical infographic card for a LinkedIn post. Portrait 4:5.

STYLE: clean flat vector infographic in the style of top system-design newsletters \
(ByteByteGo school). Very light background (#f8fafc) with a subtle grid. Modern \
geometric sans-serif typography (Inter-like), dark navy text (#0f172a). Rounded \
rectangles, thin colored outlines, subtle shadows, generous white space. Color \
semantics: BLUE (#0284c7) = entry/exit and neutral emphasis, LIGHT RED (#fee2e2 \
fill, #ef4444 border) = failure/wrong path, LIGHT GREEN (#dcfce7 fill, #22c55e \
border) = solution/right path.

LAYOUT, top to bottom:
1. Small blue pill badge, top-left, with the uppercase text: "{topic}"
2. Large extra-bold title: "{headline}"
3. CENTERPIECE (~55% of the card): a clean flowchart diagram. Its exact structure \
is specified below in Mermaid syntax — reproduce the same nodes, the same arrows, \
the same arrow labels and the same color classes (bad=red, good=green, \
accent=blue). Node text must be copied EXACTLY, character by character:
{diagram}
4. Bottom: three numbered takeaways in smaller text, each on its own line, \
numbered 1, 2, 3 inside small blue squares:
{takeaways}

HARD RULES: every piece of text must be rendered exactly as written above — no \
spelling changes, no abbreviations, no invented labels. No watermark, no logo, no \
author name, no brand name, no extra decorative text. English only. All text \
crisp and legible on a phone screen.
"""


class AICardError(RuntimeError):
    pass


def build_prompt(post) -> str:
    """Compose the infographic prompt from the post frontmatter."""
    image_meta = post.meta.get("image") or {}
    diagram = image_meta.get("diagram")
    if not diagram:
        raise AICardError(f"post {post.id} has no image.diagram")
    bullets = image_meta.get("bullets") or []
    takeaways = "\n".join(f"{i}. {b}" for i, b in enumerate(bullets[:3], start=1))
    return PROMPT_TEMPLATE.format(
        topic=str(post.meta.get("topic", "RAG")).upper(),
        headline=image_meta.get("headline") or post.title,
        diagram=diagram.strip(),
        takeaways=takeaways,
    )


def render_card(api_key: str, post, out_path: Path,
                quality: str = DEFAULT_QUALITY) -> Path:
    """Generate the card with gpt-image-2; raises AICardError on any failure."""
    resp = requests.post(
        OPENAI_API,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": MODEL, "prompt": build_prompt(post), "size": SIZE,
              "quality": quality, "n": 1},
        timeout=300,
    )
    if not resp.ok:
        raise AICardError(f"gpt-image-2: HTTP {resp.status_code} — {resp.text[:500]}")
    try:
        b64 = resp.json()["data"][0]["b64_json"]
    except (KeyError, IndexError, ValueError) as exc:
        raise AICardError(f"unexpected image API response: {exc}") from exc
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(b64))
    return out_path
