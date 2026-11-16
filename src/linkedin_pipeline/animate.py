"""Local CLI: render the animated GIF of queued posts (the artifact you commit).

    python -m linkedin_pipeline.animate              # every ready post without a GIF
    python -m linkedin_pipeline.animate 025 026      # just these ids
    python -m linkedin_pipeline.animate 025 --force  # re-render after editing the post
    python -m linkedin_pipeline.animate 025 --preview  # live HTML to iterate in a browser
    python -m linkedin_pipeline.animate --review     # one page: every GIF next to its caption
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

from . import animation, queue_store


REVIEW_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>LinkedIn queue review</title>
<style>
  body {{ margin: 0; padding: 32px 16px 64px; background: #0b1220; color: #f8fafc;
         font: 16px/1.5 -apple-system, "Helvetica Neue", Arial, sans-serif; }}
  main {{ max-width: 1040px; margin: 0 auto; }}
  h1 {{ font-size: 26px; margin: 0 0 4px; }}
  .hint {{ color: #94a3b8; margin: 0 0 28px; }}
  article {{ display: flex; flex-wrap: wrap; gap: 28px; padding: 24px; margin-bottom: 24px;
            background: #111c33; border: 1px solid #1e293b; border-radius: 16px; }}
  img {{ width: 400px; max-width: 100%; height: auto; border-radius: 10px; align-self: flex-start; }}
  .text {{ flex: 1 1 380px; min-width: 0; }}
  .label {{ color: #94a3b8; font-size: 12px; font-weight: 600; letter-spacing: .08em;
           text-transform: uppercase; margin: 0 0 6px; }}
  .internal {{ color: #94a3b8; font-size: 14px; margin: 0 0 18px; }}
  .caption {{ white-space: pre-wrap; background: #0b1220; border-radius: 10px; padding: 16px;
             margin: 0 0 12px; font: inherit; }}
  .meta {{ color: #94a3b8; font-size: 14px; margin: 0 0 6px; }}
  .missing {{ color: #f87171; }}
</style></head><body><main>
<h1>LinkedIn queue review</h1>
<p class="hint">{count} post(s), in publication order. Each GIF is exactly what gets posted,
with the caption beside it. Approve or ask for changes back in Claude Code.</p>
{articles}
</main></body></html>
"""


def build_review_html(posts, root: Path) -> str:
    """One page with every post's GIF next to the caption that will be published."""
    articles = []
    for post in posts:
        gif = root / "out" / f"{post.id}.gif"
        media = (f'<img src="../{gif.name}" alt="{html.escape(post.title)}">' if gif.exists()
                 else '<p class="meta missing">GIF not rendered yet</p>')
        articles.append(
            f"<article>{media}<div class=\"text\">"
            f'<p class="label">Internal reference · not published</p>'
            f'<p class="internal">{html.escape(post.id)} · {html.escape(post.title)}</p>'
            f'<p class="label">Caption · published exactly like this</p>'
            f'<pre class="caption">{html.escape(post.caption)}</pre>'
            f'<p class="meta">{len(post.caption)} characters</p>'
            f'<p class="meta">Alt text: {html.escape(str(post.meta.get("alt_text", "")))}</p>'
            f"</div></article>")
    return REVIEW_PAGE.format(count=len(posts), articles="\n".join(articles))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render animated GIFs for queued posts.")
    parser.add_argument("ids", nargs="*", help="post ids (default: all ready posts)")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository root (default: cwd)")
    parser.add_argument("--force", action="store_true",
                        help="re-render even when out/<id>.gif already exists")
    parser.add_argument("--preview", action="store_true",
                        help="write out/preview/<id>.html (plays in a browser) instead of a GIF")
    parser.add_argument("--review", action="store_true",
                        help="write out/preview/review.html: each GIF beside its caption")
    parser.add_argument("--mp4", action="store_true",
                        help="also write out/preview/<id>.mp4 (not published)")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    posts = queue_store.list_ready(root, animated=True)
    if args.ids:
        wanted = set(args.ids)
        missing = wanted - {p.id for p in posts}
        if missing:
            print(f"ERROR: no ready animated post with id {', '.join(sorted(missing))}")
            return 1
        posts = [p for p in posts if p.id in wanted]
    if not posts:
        print("No ready post with an animation block in content/queue/")
        return 0

    out, preview = root / "out", root / "out" / "preview"
    if args.review:
        preview.mkdir(parents=True, exist_ok=True)
        page = preview / "review.html"
        page.write_text(build_review_html(posts, root), encoding="utf-8")
        print(f"review page ({len(posts)} posts): {page}")
        return 0
    failed = 0
    for post in posts:
        try:
            if args.preview:
                preview.mkdir(parents=True, exist_ok=True)
                html_path = preview / f"{post.id}.html"
                html_path.write_text(animation.build_html(post), encoding="utf-8")
                print(f"[{post.id}] preview: {html_path}")
                continue
            gif = out / f"{post.id}.gif"
            if gif.exists() and not args.force:
                print(f"[{post.id}] {gif.name} already rendered (use --force to redo)")
                continue
            mp4 = None
            if args.mp4:
                preview.mkdir(parents=True, exist_ok=True)
                mp4 = preview / f"{post.id}.mp4"
            frames = animation.render_gif(post, gif, mp4_path=mp4)
            (out / f"{post.id}-caption.txt").write_text(post.caption + "\n", encoding="utf-8")
            size_mb = gif.stat().st_size / 1_000_000
            print(f"[{post.id}] {gif.relative_to(root)} · {frames} frames · {size_mb:.1f} MB"
                  f" · {post.title}")
        except animation.AnimationError as exc:
            failed += 1
            print(f"[{post.id}] ERROR: {exc}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
