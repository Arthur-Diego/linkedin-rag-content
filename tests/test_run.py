from conftest import make_post
from linkedin_pipeline import ai_renderer, linkedin, queue_store, run


def test_dry_run_keeps_queue(repo, monkeypatch):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    make_post(repo, "001")
    assert run.main(["--root", str(repo), "--dry-run"]) == 0
    assert (repo / "out/001.png").exists()
    assert (repo / "out/001-caption.txt").exists()
    assert queue_store.count_ready(repo) == 1


def test_draft_mode_without_token(repo, monkeypatch, tmp_path):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    gh_output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gh_output))
    make_post(repo, "001")
    assert run.main(["--root", str(repo)]) == 0
    assert queue_store.count_ready(repo) == 1  # draft does not consume the queue
    outputs = gh_output.read_text()
    assert "mode=draft" in outputs
    assert "queue_remaining=1" in outputs


def test_publish_mode_with_token(repo, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    make_post(repo, "001")
    monkeypatch.setattr(linkedin, "publish",
                        lambda *args, **kwargs: "urn:li:share:7")
    assert run.main(["--root", str(repo)]) == 0
    assert queue_store.count_ready(repo) == 0
    published = list((repo / "content/published").glob("*.md"))
    assert len(published) == 1


def test_empty_queue_exits_zero(repo, monkeypatch, capsys, tmp_path):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    gh_output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gh_output))
    assert run.main(["--root", str(repo)]) == 0
    assert "QUEUE_EMPTY" in capsys.readouterr().out
    outputs = gh_output.read_text()
    assert "queue_empty=true" in outputs
    assert "mode=none" in outputs


def test_render_only_keeps_queue_and_reports_rendered(repo, monkeypatch, tmp_path):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    gh_output = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gh_output))
    make_post(repo, "001")
    assert run.main(["--root", str(repo), "--render-only"]) == 0
    assert (repo / "out/001.png").exists()
    assert queue_store.count_ready(repo) == 1
    assert "mode=rendered" in gh_output.read_text()


def test_publish_only_reuses_artifacts_without_rerender(repo, monkeypatch):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    make_post(repo, "001")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert run.main(["--root", str(repo), "--render-only"]) == 0

    def no_ai(*args, **kwargs):
        raise AssertionError("publish-only must not call the image API")

    def no_render(*args, **kwargs):
        raise AssertionError("publish-only must not re-render the card")

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setattr(ai_renderer, "generate_background", no_ai)
    monkeypatch.setattr(run.renderer, "render_card", no_render)
    monkeypatch.setattr(linkedin, "publish", lambda *a, **k: "urn:li:share:7")
    assert run.main(["--root", str(repo), "--publish-only"]) == 0
    assert queue_store.count_ready(repo) == 0
    assert len(list((repo / "content/published").glob("*.md"))) == 1


def test_publish_only_fails_without_rendered_image(repo, monkeypatch, capsys):
    monkeypatch.setenv("LINKEDIN_ACCESS_TOKEN", "tok")
    make_post(repo, "001")
    assert run.main(["--root", str(repo), "--publish-only"]) == 1
    assert "run --render-only first" in capsys.readouterr().out
    assert queue_store.count_ready(repo) == 1


def test_ai_failure_falls_back_to_gradient(repo, monkeypatch, capsys):
    monkeypatch.delenv("LINKEDIN_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    make_post(repo, "001")

    def boom(api_key, prompt):
        raise ai_renderer.AIImageError("quota exceeded")

    monkeypatch.setattr(ai_renderer, "generate_background", boom)
    assert run.main(["--root", str(repo), "--dry-run"]) == 0
    assert (repo / "out/001.png").exists()
    assert "falling back to gradient" in capsys.readouterr().out
