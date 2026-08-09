import base64
import io
import json

import pytest
from PIL import Image

from conftest import make_post
from linkedin_pipeline import ai_renderer, queue_store


def _png_b64(size=(64, 96)) -> str:
    buf = io.BytesIO()
    Image.new("RGB", size, (10, 20, 30)).save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


class FakeResponse:
    def __init__(self, status=200, body=None):
        self.status_code = status
        self.ok = 200 <= status < 300
        self._body = body or {}
        self.text = json.dumps(self._body)

    def json(self):
        return self._body


def test_build_prompt_default_uses_topic(repo):
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    prompt = ai_renderer.build_prompt(post)
    assert "chunking" in prompt
    assert "no text" in prompt


def test_build_prompt_custom_appends_no_text(repo):
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    post.meta["image"]["prompt"] = "glowing knowledge graph"
    prompt = ai_renderer.build_prompt(post)
    assert prompt.startswith("glowing knowledge graph")
    assert "no text" in prompt


def test_generate_background_happy_path(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"], captured["json"] = url, json
        return FakeResponse(body={"data": [{"b64_json": _png_b64()}]})

    monkeypatch.setattr(ai_renderer.requests, "post", fake_post)
    img = ai_renderer.generate_background("sk-test", "some prompt")
    assert img.size == (64, 96)
    assert captured["json"]["model"] == "gpt-image-1"
    assert captured["json"]["prompt"] == "some prompt"


def test_generate_background_error_raises(monkeypatch):
    monkeypatch.setattr(
        ai_renderer.requests, "post",
        lambda url, headers=None, json=None, timeout=None: FakeResponse(
            status=401, body={"error": {"message": "bad key"}}))
    with pytest.raises(ai_renderer.AIImageError, match="401"):
        ai_renderer.generate_background("sk-bad", "prompt")
