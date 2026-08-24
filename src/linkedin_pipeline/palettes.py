"""Per-subject color palettes for the card's fixed series identity.

The card LAYOUT (dark card, 3D hero, one numbered panel per takeaway, green/red
check marks) is constant across every post — only the ACCENT family and the
background undertone change per subject, so every card still reads as a sibling.

A post picks a palette explicitly via `image.palette: <name>` in its frontmatter.
When that field is absent, the topic text is matched against known subjects; if
nothing matches, the default (violet) palette — the original series identity — is
used, so posts written before this feature render exactly as before.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    name: str
    bg: str            # background description (with hex tones) for the prompt
    accent_family: str  # accent color family description (with hex) for the prompt
    accent_name: str    # bare color word, e.g. "purple", used inline in the prompt


# The default palette reproduces the original hardcoded series identity verbatim.
DEFAULT = Palette(
    name="default",
    bg="dark near-black navy background (deep #0a0a14 → #12122a tones)",
    accent_family="vibrant violet/purple (#7c5cff, #a78bfa)",
    accent_name="purple",
)

PALETTES: dict[str, Palette] = {
    "default": DEFAULT,
    "java": Palette(
        name="java",
        bg="dark near-black background with a subtle warm charcoal undertone "
           "(deep #140a0a → #2a1212 tones)",
        accent_family="vibrant crimson/red (#e11d48, #f43f5e)",
        accent_name="red",
    ),
    "spring": Palette(
        name="spring",
        bg="dark near-black background with a subtle deep-forest undertone "
           "(deep #0a140d → #12261a tones)",
        accent_family="vibrant emerald/green (#22c55e, #4ade80)",
        accent_name="green",
    ),
}

# Fallback topic-keyword matching, tried only when image.palette is absent.
# Word-boundary patterns so "javascript" does NOT match the "java" palette.
# First match wins; add new subjects here as new palettes are introduced.
_TOPIC_PATTERNS: list[tuple[str, str]] = [
    ("java", r"\bjava\b"),
    ("spring", r"\bspring\b"),
]


def resolve_palette(post) -> Palette:
    """Resolve the palette for a post: explicit field, then topic match, then default."""
    image_meta = post.meta.get("image") or {}
    name = str(image_meta.get("palette", "")).strip().lower()
    if name in PALETTES:
        return PALETTES[name]

    topic = str(post.meta.get("topic", "")).lower()
    for palette_name, pattern in _TOPIC_PATTERNS:
        if re.search(pattern, topic):
            return PALETTES[palette_name]

    return DEFAULT
