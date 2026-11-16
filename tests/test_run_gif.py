"""Default pipeline: publish the animated GIF rendered locally and committed to out/."""

import pytest

from conftest import make_animated_post, make_post
from linkedin_pipeline import animation, linkedin, queue_store, run


@pytest.fixture(autouse=True)
def gif_mode(monkeypatch):
    monkeypatch.delenv("MEDIA_MODE", raising=False)   # gif is the default
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)

    def never(*args, **kwargs):
        raise AssertionError("the pipeline must never render a GIF; only `animate` does")

    monkeypatch.setattr(animation, "render_gif", never)


def commit_gif(repo, id_):
    out = repo / "out"
    out.mkdir(exist_ok=True)
    (out / f"{id_}.gif").write_bytes(b"GIF89a")


def test_card_posts_are_parked(repo, capsys):
    make_post(repo, "001")              # legacy card post, lower id
    make_animated_post(repo, "002")
    commit_gif(repo, "002")
    assert run.main(["--root", str(repo), "--dry-run"]) == 0
    assert "Selected post: 002" in capsys.readouterr().out
    assert not (repo / "out/001.png").exists()


def test_queue_empty_when_only_card_posts(repo, tmp_path, monkeypatch):
    gh_output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gh_output))
    make_post(repo, "001")
    assert run.main(["--root", str(repo), "--render-only"]) == 0
    assert "queue_empty=true" in gh_output.read_text()


def test_render_only_reports_committed_gif(repo, tmp_path, monkeypatch):
    gh_output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gh_output))
    make_animated_post(repo, "002")
    commit_gif(repo, "002")
    assert run.main(["--root", str(repo), "--render-only"]) == 0
    outputs = gh_output.read_text()
    assert "mode=rendered" in outputs
    assert "image_path=out/002.gif" in outputs
    assert (repo / "out/002-caption.txt").read_text().startswith("Caption of animated post")
    assert queue_store.count_ready(repo) == 1


def test_missing_gif_fails_with_instructions(repo, capsys):
    make_animated_post(repo, "002")
    assert run.main(["--root", str(repo), "--render-only"]) == 1
    out = capsys.readouterr().out
    assert "out/002.gif not found" in out
    assert "linkedin_pipeline.animate 002" in out


def test_publish_uploads_the_gif(repo, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    make_animated_post(repo, "002")
    commit_gif(repo, "002")
    uploaded = []

    def fake_publish(token, version, caption, image_path, alt_text):
        uploaded.append((image_path.name, alt_text))
        return "urn:li:share:9"

    monkeypatch.setattr(linkedin, "publish", fake_publish)
    assert run.main(["--root", str(repo), "--publish-only"]) == 0
    assert uploaded == [("002.gif", "test animation")]
    assert queue_store.count_ready(repo) == 0
    assert len(list((repo / "content/published").glob("*.md"))) == 1


def test_list_shows_gif_state_and_parked_posts(repo, capsys):
    make_post(repo, "001")
    make_animated_post(repo, "002")
    make_animated_post(repo, "003")
    commit_gif(repo, "002")
    assert run.main(["--root", str(repo), "--list"]) == 0
    out = capsys.readouterr().out
    assert "[002]" in out and "gif:rendered" in out
    assert "[003]" in out and "gif:MISSING" in out
    assert "1 ready card post(s) parked" in out


def test_invalid_media_mode_is_rejected(repo, monkeypatch):
    monkeypatch.setenv("MEDIA_MODE", "video")
    with pytest.raises(SystemExit, match="MEDIA_MODE"):
        run.main(["--root", str(repo), "--list"])
