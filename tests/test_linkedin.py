import json
from pathlib import Path

import pytest

from linkedin_pipeline import linkedin


class FakeResponse:
    def __init__(self, status=200, body=None, headers=None):
        self.status_code = status
        self.ok = 200 <= status < 300
        self._body = body or {}
        self.headers = headers or {}
        self.text = json.dumps(self._body)

    def json(self):
        return self._body


def test_escape_commentary_keeps_hashtags():
    out = linkedin.escape_commentary("RAG (naive) *bold* #RAG @you")
    assert out == "RAG \\(naive\\) \\*bold\\* #RAG @you"


def test_publish_happy_path(monkeypatch, tmp_path):
    image = tmp_path / "img.png"
    image.write_bytes(b"png-bytes")
    calls = []

    def fake_get(url, headers=None, timeout=None):
        calls.append(("GET", url))
        return FakeResponse(body={"sub": "abc123"})

    def fake_post(url, headers=None, json=None, timeout=None):
        calls.append(("POST", url, headers, json))
        if "initializeUpload" in url:
            return FakeResponse(body={"value": {
                "uploadUrl": "https://upload.linkedin.test/x",
                "image": "urn:li:image:IMG1"}})
        return FakeResponse(status=201, headers={"x-restli-id": "urn:li:share:99"})

    def fake_put(url, data=None, headers=None, timeout=None):
        calls.append(("PUT", url, data))
        return FakeResponse(status=201)

    monkeypatch.setattr(linkedin.requests, "get", fake_get)
    monkeypatch.setattr(linkedin.requests, "post", fake_post)
    monkeypatch.setattr(linkedin.requests, "put", fake_put)

    post_id = linkedin.publish("tok", "202606", "Legenda (teste) #RAG", image, "alt")
    assert post_id == "urn:li:share:99"

    init_call = next(c for c in calls if c[0] == "POST" and "initializeUpload" in c[1])
    assert init_call[3] == {"initializeUploadRequest": {"owner": "urn:li:person:abc123"}}
    assert init_call[2]["LinkedIn-Version"] == "202606"
    assert init_call[2]["X-Restli-Protocol-Version"] == "2.0.0"

    put_call = next(c for c in calls if c[0] == "PUT")
    assert put_call[2] == b"png-bytes"

    post_call = next(c for c in calls if c[0] == "POST" and c[1].endswith("/rest/posts"))
    payload = post_call[3]
    assert payload["author"] == "urn:li:person:abc123"
    assert payload["commentary"] == "Legenda \\(teste\\) #RAG"
    assert payload["content"]["media"]["id"] == "urn:li:image:IMG1"
    assert payload["lifecycleState"] == "PUBLISHED"
    assert payload["visibility"] == "PUBLIC"


def test_error_raises_with_body(monkeypatch):
    monkeypatch.setattr(
        linkedin.requests, "get",
        lambda url, headers=None, timeout=None: FakeResponse(status=401, body={"message": "expired"}))
    with pytest.raises(linkedin.LinkedInError, match="401"):
        linkedin.get_person_urn("tok")
