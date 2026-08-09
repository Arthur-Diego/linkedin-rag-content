from conftest import make_post
from linkedin_pipeline import linkedin, queue_store, run


def test_dry_run_keeps_queue(repo, monkeypatch):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    make_post(repo, "001")
    assert run.main(["--root", str(repo), "--dry-run"]) == 0
    assert (repo / "out/001.png").exists()
    assert (repo / "out/001-caption.txt").exists()
    assert queue_store.count_ready(repo) == 1


def test_draft_mode_without_token(repo, monkeypatch):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    make_post(repo, "001")
    assert run.main(["--root", str(repo)]) == 0
    assert queue_store.count_ready(repo) == 1  # draft não consome a fila


def test_publish_mode_with_token(repo, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    make_post(repo, "001")
    monkeypatch.setattr(linkedin, "publish",
                        lambda *args, **kwargs: "urn:li:share:7")
    assert run.main(["--root", str(repo)]) == 0
    assert queue_store.count_ready(repo) == 0
    published = list((repo / "content/published").glob("*.md"))
    assert len(published) == 1


def test_empty_queue_exits_zero(repo, monkeypatch, capsys):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    assert run.main(["--root", str(repo)]) == 0
    assert "QUEUE_EMPTY" in capsys.readouterr().out
