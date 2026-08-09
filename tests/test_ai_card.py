import base64
import io
import json

import pytest
from PIL import Image

from linkedin_pipeline import ai_card, queue_store
from test_html_renderer import DIAGRAM_POST


@pytest.fixture
def diagram_post(repo):
    path = repo / "content/queue/042-diagram.md"
    path.write_text(DIAGRAM_POST, encoding="utf-8")
    return queue_store.next_post(repo)


class FakeResponse:
    def __init__(self, status=200, body=None):
        self.status_code = status
        self.ok = 200 <= status < 300
        self._body = body or {}
        self.text = json.dumps(self._body)

    def json(self):
        return self._body


def _png_b64() -> str:
    buf = io.BytesIO()
    Image.new("RGB", (64, 80), (250, 250, 252)).save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def test_spec_prompt_includes_exact_content(diagram_post):
    diagram_post.meta["image"]["style"] = "spec"
    prompt = ai_card.build_prompt(diagram_post)
    assert '"TEST TOPIC"' in prompt
    assert "A headline with <special> & chars" in prompt
    assert "flowchart LR" in prompt
    assert "1. first takeaway" in prompt
    assert "3. third takeaway" in prompt
    assert "no watermark" in prompt.lower()


def test_free_prompt_has_no_diagram_and_keeps_headline(diagram_post):
    diagram_post.meta["image"]["style"] = "free"
    prompt = ai_card.build_prompt(diagram_post)
    assert "flowchart LR" not in prompt
    assert "A headline with <special> & chars" in prompt
    assert "CREATIVE FREEDOM" in prompt
    assert "1. first takeaway" in prompt


def test_style_defaults_to_free(diagram_post):
    assert ai_card.resolve_style(diagram_post) == "free"
    diagram_post.meta["image"]["style"] = "spec"           # explicit opt-in wins
    assert ai_card.resolve_style(diagram_post) == "spec"


def test_free_prompt_carries_series_identity(diagram_post):
    prompt = ai_card.build_prompt(diagram_post)             # default = free
    assert "VISUAL IDENTITY" in prompt
    assert "#7c5cff" in prompt


def test_spec_prompt_requires_diagram(repo):
    from conftest import make_post
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    post.meta["image"]["style"] = "spec"  # conftest post has no image.diagram
    with pytest.raises(ai_card.AICardError, match="no image.diagram"):
        ai_card.build_prompt(post)


def test_render_card_happy_path(diagram_post, tmp_path, monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"], captured["json"] = url, json
        return FakeResponse(body={"data": [{"b64_json": _png_b64()}]})

    monkeypatch.setattr(ai_card.requests, "post", fake_post)
    out = tmp_path / "card.png"
    ai_card.render_card("sk-test", diagram_post, out, quality="high")
    assert out.exists()
    assert captured["json"]["model"] == "gpt-image-2"
    assert captured["json"]["size"] == "1088x1360"
    assert captured["json"]["quality"] == "high"


def test_render_card_error_raises(diagram_post, tmp_path, monkeypatch):
    monkeypatch.setattr(
        ai_card.requests, "post",
        lambda url, headers=None, json=None, timeout=None: FakeResponse(
            status=429, body={"error": {"message": "quota"}}))
    with pytest.raises(ai_card.AICardError, match="429"):
        ai_card.render_card("sk-test", diagram_post, tmp_path / "card.png")
