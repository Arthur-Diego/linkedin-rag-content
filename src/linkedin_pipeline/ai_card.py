"""Primary card renderer: gpt-image-2 infographic built from the post's diagram spec."""

from __future__ import annotations

import base64
from pathlib import Path

import requests

OPENAI_API = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-2"
SIZE = "1088x1360"  # exact 4:5 portrait, multiples of 16
DEFAULT_QUALITY = "high"

FREE_PROMPT_TEMPLATE = """\
Create a striking, professional infographic card for a LinkedIn post about a \
software engineering topic. Portrait 4:5.

TOPIC: "{topic}" — {headline}

CORE IDEAS — one visual panel per idea, in this order:
{takeaways}

VISUAL IDENTITY (fixed series style — every card must look like a sibling of the \
others): dark near-black navy background (deep #0a0a14 → #12122a tones), vibrant \
violet/purple (#7c5cff, #a78bfa) as the single accent family, white extra-bold \
modern sans-serif headline at the top with 1-2 key words highlighted in purple, \
one glossy 3D isometric vector object as the hero visual near the headline \
(cube, sphere, device — pick the best metaphor for the topic), and below it \
rounded dark panels with thin outlines — ONE panel per core idea, each numbered \
in a small purple square (1, 2, 3), each panel illustrating its idea with small \
3D vector elements, green check marks for right/good and red crosses for \
wrong/bad. Subtle glow and depth shadows. Premium tech-brand editorial style, \
generous spacing, nothing cluttered.

CREATIVE FREEDOM: within that identity, you choose the metaphors, objects and \
per-panel compositions that best explain THIS topic.

REQUIRED: render the headline text "{headline}" prominently and legibly, spelled \
exactly as written. The numbered panel texts must copy the core ideas exactly, \
character by character. Any other text minimal and correctly spelled.
FORBIDDEN: watermarks, logos, brand names, author names, invented statistics, \
walls of text. All text legible on a phone screen.
"""

SPEC_PROMPT_TEMPLATE = """\
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


def resolve_style(post) -> str:
    """'free' (creative, fixed series identity — the default) or 'spec'
    (diagram-driven), overridable per post via image.style."""
    image_meta = post.meta.get("image") or {}
    style = str(image_meta.get("style", "")).strip().lower()
    return style if style in ("spec", "free") else "free"


def build_prompt(post) -> str:
    """Compose the image prompt from the post frontmatter, per resolved style."""
    image_meta = post.meta.get("image") or {}
    headline = image_meta.get("headline") or post.title
    topic = str(post.meta.get("topic", "RAG")).upper()
    bullets = image_meta.get("bullets") or []
    takeaways = "\n".join(f"{i}. {b}" for i, b in enumerate(bullets[:3], start=1))

    if resolve_style(post) == "free":
        return FREE_PROMPT_TEMPLATE.format(
            topic=topic, headline=headline, takeaways=takeaways)

    diagram = image_meta.get("diagram")
    if not diagram:
        raise AICardError(f"post {post.id} has no image.diagram")
    return SPEC_PROMPT_TEMPLATE.format(
        topic=topic, headline=headline, diagram=diagram.strip(),
        takeaways=takeaways)


def render_card(api_key: str, post, out_path: Path,
                quality: str = DEFAULT_QUALITY) -> Path:
    """Generate the card with gpt-image-2; raises AICardError on any failure."""
    print(f"AI card style: {resolve_style(post)}")
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
