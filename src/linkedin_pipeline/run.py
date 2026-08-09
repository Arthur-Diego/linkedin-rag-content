"""Pipeline orchestration: queue -> image -> LinkedIn (or draft)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import ai_renderer, linkedin, queue_store, renderer


def _gh_output(**kwargs) -> None:
    """Emit outputs for GitHub Actions (no-op outside CI)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        for key, value in kwargs.items():
            fh.write(f"{key}={value}\n")


def _ai_background(post):
    """AI-generated background when OPENAI_API_KEY is set; None otherwise/on failure."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    prompt = ai_renderer.build_prompt(post)
    try:
        background = ai_renderer.generate_background(api_key, prompt)
        print("AI background generated (gpt-image-1)")
        return background
    except Exception as exc:  # any failure falls back to the gradient
        print(f"AI background failed, falling back to gradient: {exc}")
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish the next post in the queue.")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository root (default: cwd)")
    parser.add_argument("--dry-run", action="store_true",
                        help="render artifacts without publishing or consuming the queue")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    post = queue_store.next_post(root)
    if post is None:
        print("QUEUE_EMPTY: no 'ready' post in content/queue/")
        _gh_output(queue_empty="true", queue_remaining="0", mode="none")
        return 0

    print(f"Selected post: {post.id} — {post.title}")
    background = _ai_background(post)
    image_path = renderer.render_card(post, root / "out" / f"{post.id}.png",
                                      background=background)
    caption_path = root / "out" / f"{post.id}-caption.txt"
    caption_path.write_text(post.caption + "\n", encoding="utf-8")
    print(f"Image: {image_path}\nCaption: {caption_path}")

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    version = os.environ.get("LINKEDIN_VERSION", linkedin.DEFAULT_VERSION)
    alt_text = str(post.meta.get("alt_text", post.title))

    if args.dry_run:
        mode = "dry-run"
        print("dry-run: nothing published, queue untouched.")
    elif token:
        post_id = linkedin.publish(token, version, post.caption, image_path, alt_text)
        dest = queue_store.mark_published(root, post, post_id)
        mode = "published"
        print(f"Published to LinkedIn (id={post_id}); post moved to {dest}")
    else:
        mode = "draft"
        print("No LINKEDIN_ACCESS_TOKEN: draft mode — post stays in the queue.")

    _gh_output(
        mode=mode,
        post_id=post.id,
        post_title=post.title,
        image_path=str(image_path.relative_to(root)),
        caption_path=str(caption_path.relative_to(root)),
        queue_empty="false",
        queue_remaining=str(queue_store.count_ready(root)),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
