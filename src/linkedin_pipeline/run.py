"""Orquestração do pipeline: fila -> imagem -> LinkedIn (ou draft)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import linkedin, queue_store, renderer


def _gh_output(**kwargs) -> None:
    """Emite outputs para o GitHub Actions (no-op fora do CI)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        for key, value in kwargs.items():
            fh.write(f"{key}={value}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publica o próximo post da fila.")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="raiz do repositório (default: cwd)")
    parser.add_argument("--dry-run", action="store_true",
                        help="renderiza artefatos sem publicar nem mover a fila")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    post = queue_store.next_post(root)
    if post is None:
        print("QUEUE_EMPTY: nenhum post 'ready' em content/queue/")
        _gh_output(queue_empty="true", queue_remaining="0", mode="none")
        return 0

    print(f"Post selecionado: {post.id} — {post.title}")
    image_path = renderer.render_card(post, root / "out" / f"{post.id}.png")
    caption_path = root / "out" / f"{post.id}-caption.txt"
    caption_path.write_text(post.caption + "\n", encoding="utf-8")
    print(f"Imagem: {image_path}\nLegenda: {caption_path}")

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    version = os.environ.get("LINKEDIN_VERSION", linkedin.DEFAULT_VERSION)
    alt_text = str(post.meta.get("alt_text", post.title))

    if args.dry_run:
        mode = "dry-run"
        print("dry-run: nada publicado, fila intacta.")
    elif token:
        post_id = linkedin.publish(token, version, post.caption, image_path, alt_text)
        dest = queue_store.mark_published(root, post, post_id)
        mode = "published"
        print(f"Publicado no LinkedIn (id={post_id}); post movido para {dest}")
    else:
        mode = "draft"
        print("Sem LINKEDIN_ACCESS_TOKEN: modo draft — post permanece na fila.")

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
