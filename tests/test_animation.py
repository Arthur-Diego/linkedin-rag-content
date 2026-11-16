import copy
import json
import shutil

import pytest
from PIL import Image

from conftest import make_animated_post, make_post
from linkedin_pipeline import animate, animation, queue_store


@pytest.fixture
def animated_post(repo):
    make_animated_post(repo, "042")
    return queue_store.next_post(repo)


def test_build_html_embeds_the_spec(animated_post):
    html = animation.build_html(animated_post)
    assert "{{" not in html.split("<script>")[0]          # no unfilled placeholders
    assert "{{SPEC}}" not in html and "{{ASSETS}}" not in html
    assert json.dumps("One request") in html


def test_build_html_escapes_script_terminators(animated_post):
    animated_post.meta["animation"]["title"] = "</script><b>x"
    assert "</script><b>x" not in animation.build_html(animated_post)


def test_card_post_has_no_animation(repo):
    make_post(repo, "001")
    with pytest.raises(animation.AnimationError, match="no animation block"):
        animation.build_html(queue_store.next_post(repo))


def test_unknown_scene_is_rejected(animated_post):
    animated_post.meta["animation"]["scene"] = "does-not-exist"
    with pytest.raises(animation.AnimationError, match="scene not found"):
        animation.build_html(animated_post)


@pytest.mark.parametrize("mutate, message", [
    (lambda s: s.pop("title"), "animation.title is required"),
    (lambda s: s["nodes"].append({"id": "a", "label": "Dup", "at": [2, 0]}), "duplicate node id"),
    (lambda s: s["nodes"].append({"id": "c", "label": "Same cell", "at": [0, 0]}), "already taken"),
    (lambda s: s["nodes"][0].update(at=[9, 0]), "must be \\[column, row\\]"),
    (lambda s: s["edges"].append({"from": "a", "to": "ghost"}), "unknown node 'ghost'"),
    (lambda s: s.update(tally={"ok": "x" * 19}), "longer than 18 characters"),
    (lambda s: s.update(tally={"great": "hits"}), "tally: kind"),
    (lambda s: s["steps"][0].pop("caption"), "caption is required"),
    (lambda s: s["steps"][0]["packets"][0].update(path=["a"]), "at least 2 nodes"),
    (lambda s: s["steps"][0]["packets"][0].update(kind="great"), "packet kind"),
    (lambda s: s["steps"][0].update(meters={"ghost": 1}), "unknown node 'ghost'"),
])
def test_validate_rejects_broken_specs(animated_post, mutate, message):
    spec = copy.deepcopy(animated_post.meta["animation"])
    mutate(spec)
    with pytest.raises(animation.AnimationError, match=message):
        animation.validate(spec)


def test_custom_scenes_skip_flow_validation():
    animation.validate({"scene": "token-bucket"})   # no nodes/steps needed


def test_queued_animations_are_valid():
    """Every animated post shipped in the real queue must pass validation."""
    root = animation.DEFAULT_ASSETS.parent
    for post in queue_store.list_ready(root, animated=True):
        animation.build_html(post)


def test_animate_cli_previews_without_browser(repo, capsys):
    make_animated_post(repo, "042")
    assert animate.main(["--root", str(repo), "--preview"]) == 0
    assert (repo / "out/preview/042.html").exists()
    assert not (repo / "out/042.gif").exists()


def test_animate_cli_rejects_unknown_id(repo, capsys):
    make_animated_post(repo, "042")
    assert animate.main(["--root", str(repo), "999"]) == 1
    assert "no ready animated post with id 999" in capsys.readouterr().out


def test_animate_cli_skips_rendered_posts(repo, monkeypatch, capsys):
    make_animated_post(repo, "042")
    (repo / "out").mkdir()
    (repo / "out/042.gif").write_bytes(b"GIF89a")
    monkeypatch.setattr(animation, "render_gif",
                        lambda *a, **k: pytest.fail("must not re-render without --force"))
    assert animate.main(["--root", str(repo)]) == 0
    assert "already rendered" in capsys.readouterr().out


def test_render_gif_produces_looping_gif(animated_post, repo):
    pytest.importorskip("playwright.sync_api")
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg unavailable")
    out = repo / "out/042.gif"
    try:
        frames = animation.render_gif(animated_post, out)
    except animation.AnimationError as exc:
        pytest.skip(f"browser unavailable: {exc}")
    with Image.open(out) as img:
        assert img.format == "GIF"
        assert img.size == (animation.WIDTH, animation.HEIGHT)
        assert img.n_frames == frames <= animation.MAX_FRAMES
        assert img.info.get("loop") == 0


def test_review_page_shows_gif_and_caption(repo, capsys):
    make_animated_post(repo, "042")
    make_animated_post(repo, "043")
    (repo / "out").mkdir()
    (repo / "out/042.gif").write_bytes(b"GIF89a")
    assert animate.main(["--root", str(repo), "--review", "042", "043"]) == 0
    page = (repo / "out/preview/review.html").read_text()
    assert 'src="../042.gif"' in page
    assert "Caption of animated post 042." in page
    assert "GIF not rendered yet" in page          # 043 has no GIF
    assert "2 post(s)" in page
