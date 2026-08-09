"""Professional card renderer: HTML template + Mermaid diagram → PNG via Playwright."""

from __future__ import annotations

import html
import tempfile
from pathlib import Path

DEFAULT_ASSETS = Path(__file__).resolve().parents[2] / "assets"


class HTMLRenderError(RuntimeError):
    pass


def _takeaways_html(bullets: list) -> str:
    items = []
    for i, bullet in enumerate(bullets[:3], start=1):
        items.append(
            f'<div class="takeaway"><span class="num">{i}</span>'
            f"<span>{html.escape(str(bullet))}</span></div>"
        )
    return "".join(items)


def build_html(post, assets_dir: Path = DEFAULT_ASSETS) -> str:
    """Fill the card template with the post's frontmatter."""
    image_meta = post.meta.get("image") or {}
    diagram = image_meta.get("diagram")
    if not diagram:
        raise HTMLRenderError(f"post {post.id} has no image.diagram")
    headline = image_meta.get("headline") or post.title
    template = (assets_dir / "card_template.html").read_text(encoding="utf-8")
    return (
        template
        .replace("{{ASSETS}}", assets_dir.resolve().as_uri())
        .replace("{{TOPIC}}", html.escape(str(post.meta.get("topic", "RAG"))))
        .replace("{{TITLE}}", html.escape(headline))
        .replace("{{DIAGRAM}}", html.escape(diagram))
        .replace("{{TAKEAWAYS}}", _takeaways_html(image_meta.get("bullets") or []))
        .replace("{{NUMBER}}", html.escape(post.id))
    )


def render_card(post, out_path: Path, assets_dir: Path = DEFAULT_ASSETS) -> Path:
    """Render the diagram card to PNG; raises HTMLRenderError on any failure."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise HTMLRenderError(f"playwright not installed: {exc}") from exc

    page_html = build_html(post, assets_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / "card.html"
        html_file.write_text(page_html, encoding="utf-8")
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch()
                page = browser.new_page(viewport={"width": 1400, "height": 1500})
                page.goto(html_file.as_uri())
                page.wait_for_function("window.__ready === true || window.__error",
                                       timeout=30_000)
                error = page.evaluate("window.__error || ''")
                if error:
                    raise HTMLRenderError(f"mermaid render failed: {error}")
                page.locator("#card").screenshot(path=str(out_path))
                browser.close()
        except HTMLRenderError:
            raise
        except Exception as exc:
            raise HTMLRenderError(f"playwright render failed: {exc}") from exc
    return out_path
