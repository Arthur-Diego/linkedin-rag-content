"""Post queue versioned in git: content/queue/ -> content/published/."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import yaml

QUEUE_DIR = "content/queue"
PUBLISHED_DIR = "content/published"


@dataclass
class Post:
    path: Path
    meta: dict = field(default_factory=dict)
    body: str = ""

    @property
    def id(self) -> str:
        return str(self.meta["id"])

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.id))

    @property
    def caption(self) -> str:
        return self.body.strip()


def _parse(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"post without frontmatter: {path}")
    try:
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm)
    except (ValueError, yaml.YAMLError) as exc:
        raise ValueError(f"invalid frontmatter in {path}: {exc}") from exc
    if not isinstance(meta, dict) or "id" not in meta:
        raise ValueError(f"frontmatter missing 'id' in {path}")
    return Post(path=path, meta=meta, body=body)


def _ready_posts(root: Path) -> list[Post]:
    queue = root / QUEUE_DIR
    if not queue.is_dir():
        return []
    posts = [_parse(p) for p in sorted(queue.glob("*.md"))]
    return [p for p in posts if p.meta.get("status") == "ready"]


def next_post(root: Path) -> Post | None:
    """The 'ready' post with the lowest id, or None if the queue is empty."""
    posts = _ready_posts(root)
    return min(posts, key=lambda p: p.id) if posts else None


def count_ready(root: Path) -> int:
    return len(_ready_posts(root))


def mark_published(root: Path, post: Post, linkedin_post_id: str) -> Path:
    """Update the frontmatter and move the file to content/published/."""
    meta = dict(post.meta)
    meta["status"] = "published"
    meta["published_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    meta["linkedin_post_id"] = linkedin_post_id
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    dest_dir = root / PUBLISHED_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / post.path.name
    dest.write_text(f"---\n{fm}\n---\n{post.body.lstrip()}", encoding="utf-8")
    post.path.unlink()
    return dest
