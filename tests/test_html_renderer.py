from pathlib import Path

import pytest
from PIL import Image

from linkedin_pipeline import html_renderer, queue_store

DIAGRAM_POST = """---
id: "042"
topic: test topic
title: "Test diagram post"
image:
  headline: "A headline with <special> & chars"
  diagram: |
    flowchart LR
        A["Start"]:::accent --> B["Middle"]
        B --> C["End"]:::good
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "first takeaway"
    - "second takeaway"
    - "third takeaway"
alt_text: "test"
status: ready
---
Caption body.
"""


@pytest.fixture
def diagram_post(repo):
    path = repo / "content/queue/042-diagram.md"
    path.write_text(DIAGRAM_POST, encoding="utf-8")
    return queue_store.next_post(repo)


def test_build_html_fills_template(diagram_post):
    html = html_renderer.build_html(diagram_post)
    assert "A headline with &lt;special&gt; &amp; chars" in html
    assert 'flowchart LR' in html
    assert html.count('class="takeaway"') == 3
    assert "TEST TOPIC".lower() in html.lower()
    assert "{{" not in html  # no unfilled placeholders


def test_build_html_requires_diagram(repo):
    from conftest import make_post
    make_post(repo, "001")  # conftest post has no image.diagram
    post = queue_store.next_post(repo)
    with pytest.raises(html_renderer.HTMLRenderError, match="no image.diagram"):
        html_renderer.build_html(post)


def test_render_card_produces_correct_png(diagram_post, repo):
    pytest.importorskip("playwright.sync_api")
    out = repo / "out/042.png"
    try:
        html_renderer.render_card(diagram_post, out)
    except html_renderer.HTMLRenderError as exc:
        pytest.skip(f"browser unavailable: {exc}")
    with Image.open(out) as img:
        assert img.size == (1200, 1350)
        assert img.format == "PNG"
