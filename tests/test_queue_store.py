import pytest

from conftest import make_post
from linkedin_pipeline import queue_store


def test_next_post_picks_lowest_id(repo):
    make_post(repo, "002")
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    assert post is not None and post.id == "001"


def test_next_post_ignores_non_ready(repo):
    make_post(repo, "001", status="published")
    assert queue_store.next_post(repo) is None


def test_next_post_empty_queue(repo):
    assert queue_store.next_post(repo) is None
    assert queue_store.count_ready(repo) == 0


def test_count_ready(repo):
    make_post(repo, "001")
    make_post(repo, "002")
    make_post(repo, "003", status="published")
    assert queue_store.count_ready(repo) == 2


def test_mark_published_moves_and_updates(repo):
    make_post(repo, "001")
    post = queue_store.next_post(repo)
    dest = queue_store.mark_published(repo, post, "urn:li:share:42")
    assert not post.path.exists()
    assert dest.parent.name == "published"
    republished = queue_store._parse(dest)
    assert republished.meta["status"] == "published"
    assert republished.meta["linkedin_post_id"] == "urn:li:share:42"
    assert "published_at" in republished.meta
    assert "Legenda do post 001" in republished.body


def test_invalid_frontmatter_raises(repo):
    (repo / "content/queue/bad.md").write_text("sem frontmatter", encoding="utf-8")
    with pytest.raises(ValueError, match="bad.md"):
        queue_store.next_post(repo)
