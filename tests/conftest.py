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


ANIMATED_POST_TEMPLATE = """---
id: "{id}"
topic: system design
title: "Animated post {id}"
animation:
  title: "Scene {id}"
  nodes:
    - {{id: a, label: Client, at: [0, 0]}}
    - {{id: b, label: Service, at: [1, 0], meter: 3}}
  edges:
    - {{from: a, to: b, label: call}}
  steps:
    - caption: "One request"
      packets:
        - {{path: [a, b], kind: ok}}
      meters: {{b: 2}}
alt_text: "test animation"
status: {status}
---
Caption of animated post {id}.
"""


def make_animated_post(root: Path, id_: str, status: str = "ready") -> Path:
    path = root / "content/queue" / f"{id_}-animated.md"
    path.write_text(ANIMATED_POST_TEMPLATE.format(id=id_, status=status), encoding="utf-8")
    return path
