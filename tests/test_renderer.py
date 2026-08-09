from PIL import Image

from conftest import make_post
from linkedin_pipeline import queue_store, renderer


def test_render_card_creates_png(repo):
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    out = renderer.render_card(post, repo / "out" / "001.png")
    assert out.exists()
    with Image.open(out) as img:
        assert img.size == (1200, 1350)
        assert img.format == "PNG"


def test_render_card_long_text(repo):
    path = repo / "content/queue/009-longo.md"
    path.write_text(
        """---
id: "009"
topic: graph rag
title: "longo"
image:
  headline: "Um título consideravelmente longo que precisa quebrar em várias linhas no card"
  bullets:
    - "um bullet igualmente longo que também deve quebrar em mais de uma linha sem estourar a margem do card"
    - "segundo"
    - "terceiro"
    - "quarto"
alt_text: "x"
status: ready
---
corpo
""",
        encoding="utf-8",
    )
    post = queue_store.next_post(repo)
    out = renderer.render_card(post, repo / "out" / "009.png")
    assert out.exists()
