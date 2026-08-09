"""Minimal client for the versioned LinkedIn API: userinfo, image upload, post."""

from __future__ import annotations

from pathlib import Path

import requests

API = "https://api.linkedin.com"
DEFAULT_VERSION = "202606"
_RESERVED = "\\|{}[]()<>*_~"


class LinkedInError(RuntimeError):
    pass


def escape_commentary(text: str) -> str:
    """Escape little-text reserved characters (keeps # and @ intact)."""
    return "".join(f"\\{c}" if c in _RESERVED else c for c in text)


def _headers(token: str, version: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": version,
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def _check(resp: requests.Response, step: str) -> None:
    if not resp.ok:
        raise LinkedInError(f"{step}: HTTP {resp.status_code} — {resp.text[:500]}")


def get_person_urn(token: str) -> str:
    resp = requests.get(f"{API}/v2/userinfo",
                        headers={"Authorization": f"Bearer {token}"}, timeout=30)
    _check(resp, "userinfo")
    return f"urn:li:person:{resp.json()['sub']}"


def upload_image(token: str, version: str, owner_urn: str, image_path: Path) -> str:
    resp = requests.post(f"{API}/rest/images?action=initializeUpload",
                         headers=_headers(token, version),
                         json={"initializeUploadRequest": {"owner": owner_urn}},
                         timeout=30)
    _check(resp, "initializeUpload")
    value = resp.json()["value"]
    up = requests.put(value["uploadUrl"], data=image_path.read_bytes(),
                      headers={"Authorization": f"Bearer {token}"}, timeout=120)
    _check(up, "binary upload")
    return value["image"]


def create_post(token: str, version: str, author: str, commentary: str,
                image_urn: str, alt_text: str) -> str:
    payload = {
        "author": author,
        "commentary": escape_commentary(commentary),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "content": {"media": {"altText": alt_text, "id": image_urn}},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    resp = requests.post(f"{API}/rest/posts", headers=_headers(token, version),
                         json=payload, timeout=30)
    _check(resp, "create post")
    return resp.headers.get("x-restli-id", "")


def publish(token: str, version: str, caption: str, image_path: Path,
            alt_text: str) -> str:
    """Full flow: author -> image upload -> post. Returns the post id."""
    author = get_person_urn(token)
    image_urn = upload_image(token, version, author, image_path)
    return create_post(token, version, author, caption, image_urn, alt_text)
