"""Optional AI-generated card background via OpenAI gpt-image-1."""

from __future__ import annotations

import base64
import io

import requests
from PIL import Image

OPENAI_API = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-1"
SIZE = "1024x1536"  # portrait, closest supported ratio to the 1200x1350 card

DEFAULT_PROMPT = (
    "Abstract futuristic technology illustration about {topic}, dark navy blue "
    "color palette with cyan accents, subtle geometric shapes and network "
    "patterns, minimal, atmospheric, high contrast, no text, no letters, no words"
)


class AIImageError(RuntimeError):
    pass


def build_prompt(post) -> str:
    """Post-specific visual prompt, or a topic-based default."""
    image_meta = post.meta.get("image") or {}
    custom = image_meta.get("prompt")
    if custom:
        return f"{custom}, no text, no letters, no words"
    return DEFAULT_PROMPT.format(topic=post.meta.get("topic", "artificial intelligence"))


def generate_background(api_key: str, prompt: str) -> Image.Image:
    """Generate a background illustration; raises AIImageError on any API failure."""
    resp = requests.post(
        OPENAI_API,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": MODEL, "prompt": prompt, "size": SIZE,
              "quality": "medium", "n": 1},
        timeout=300,
    )
    if not resp.ok:
        raise AIImageError(f"image generation: HTTP {resp.status_code} — {resp.text[:500]}")
    try:
        b64 = resp.json()["data"][0]["b64_json"]
    except (KeyError, IndexError, ValueError) as exc:
        raise AIImageError(f"unexpected image API response: {exc}") from exc
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
