"""Pipeline orchestration: queue -> diagram card -> approval -> LinkedIn (or draft)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import html_renderer, linkedin, queue_store, renderer


def _gh_output(**kwargs) -> None:
    """Emit outputs for GitHub Actions (no-op outside CI)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        for key, value in kwargs.items():
            fh.write(f"{key}={value}\n")


def _render(post, image_path: Path) -> None:
    """Diagram card via HTML/Playwright; Pillow gradient card as emergency fallback."""
    try:
        html_renderer.render_card(post, image_path)
        print("Card rendered (HTML template + Mermaid diagram)")
    except html_renderer.HTMLRenderError as exc:
        print(f"HTML renderer unavailable ({exc}); falling back to Pillow card")
        renderer.render_card(post, image_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publish the next post in the queue.")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository root (default: cwd)")
    parser.add_argument("--dry-run", action="store_true",
                        help="render artifacts without publishing or consuming the queue")
    parser.add_argument("--render-only", action="store_true",
                        help="render artifacts and stop (approval flow, stage 1)")
    parser.add_argument("--publish-only", action="store_true",
                        help="publish previously rendered artifacts without re-rendering "
                             "(approval flow, stage 2)")
    args = parser.parse_args(argv)
    if args.render_only and args.publish_only:
        parser.error("--render-only and --publish-only are mutually exclusive")
    root = args.root.resolve()

    post = queue_store.next_post(root)
    if post is None:
        print("QUEUE_EMPTY: no 'ready' post in content/queue/")
        _gh_output(queue_empty="true", queue_remaining="0", mode="none")
        return 0

    print(f"Selected post: {post.id} — {post.title}")
    image_path = root / "out" / f"{post.id}.png"
    caption_path = root / "out" / f"{post.id}-caption.txt"

    if args.publish_only:
        if not image_path.exists():
            print(f"ERROR: {image_path} not found — run --render-only first.")
            return 1
        print(f"Reusing approved artifacts: {image_path}")
    else:
        _render(post, image_path)
        caption_path.parent.mkdir(parents=True, exist_ok=True)
        caption_path.write_text(post.caption + "\n", encoding="utf-8")
        print(f"Image: {image_path}\nCaption: {caption_path}")

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    version = os.environ.get("LINKEDIN_VERSION", linkedin.DEFAULT_VERSION)
    alt_text = str(post.meta.get("alt_text", post.title))

    if args.dry_run:
        mode = "dry-run"
        print("dry-run: nothing published, queue untouched.")
    elif args.render_only:
        mode = "rendered"
        print("render-only: artifacts ready for approval; queue untouched.")
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
