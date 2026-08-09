import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

POST_TEMPLATE = """---
id: "{id}"
topic: chunking
title: "Test post {id}"
image:
  headline: "Headline {id}"
  bullets:
    - "first point"
    - "second point"
alt_text: "test card"
status: {status}
---
Caption of post {id} with #RAG and #AI.
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "content/queue").mkdir(parents=True)
    (tmp_path / "content/published").mkdir(parents=True)
    return tmp_path


def make_post(root: Path, id_: str, status: str = "ready") -> Path:
    path = root / "content/queue" / f"{id_}-test.md"
    path.write_text(POST_TEMPLATE.format(id=id_, status=status), encoding="utf-8")
    return path
