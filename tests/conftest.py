import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

POST_TEMPLATE = """---
id: "{id}"
topic: chunking
title: "Post de teste {id}"
image:
  headline: "Headline {id}"
  bullets:
    - "primeiro ponto"
    - "segundo ponto"
alt_text: "card de teste"
status: {status}
---
Legenda do post {id} com #RAG e #IA.
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "content/queue").mkdir(parents=True)
    (tmp_path / "content/published").mkdir(parents=True)
    return tmp_path


def make_post(root: Path, id_: str, status: str = "ready") -> Path:
    path = root / "content/queue" / f"{id_}-teste.md"
    path.write_text(POST_TEMPLATE.format(id=id_, status=status), encoding="utf-8")
    return path
