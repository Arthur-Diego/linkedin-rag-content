# linkedin-rag-content

Automated pipeline for technical RAG posts on LinkedIn: versioned content queue →
didactic infographic card (gpt-image-2 primary; Mermaid/Playwright and Pillow
fallbacks) → human approval gate → LinkedIn Posts API (or draft issue), scheduled
by GitHub Actions 3x/week.

## Context index (everything lives in docs/)

- PRD: `docs/prd.md`
- Domain HLD: `docs/domains/content-pipeline/hld.md`
- Feature 1 FDD: `docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`
- Diagrams: `docs/domains/content-pipeline/diagrams/mermaid/`
- ADRs: `docs/adrs/generated/CONTENT-PIPELINE/` (001–008)
- Python guidelines: `docs/guidelines/python.md`
- Research: `docs/research/linkedin-napkin-apis.md` (APIs),
  `docs/research/linkedin-tech-content-playbook.md` (content/copy rules)
- Gitflow: `docs/gitflow.md` · DD config: `docs/dd.md`
- Operations runbook (tokens, troubleshooting): `docs/operations/runbook.md`

## Commands

- Tests: `python -m pytest tests/ -q`
- List the queue (publication order + resolved palette): `PYTHONPATH=src python -m linkedin_pipeline.run --list`
- Local pipeline run (no publish): `PYTHONPATH=src python -m linkedin_pipeline.run --dry-run`
- Generate new queue posts: follow `scripts/PROMPT_GERACAO.md`

## Project rules

- The only allowed paid API is gpt-image-2 for the card (ADR-009, ~US$0.17/image);
  everything else must stay free, and the Mermaid/Pillow fallbacks must always work
  without the key.
- Queued posts: markdown with YAML frontmatter in `content/queue/NNN-slug.md`
  (must include `image.diagram`, Mermaid); published ones move to
  `content/published/`.
- Card color per subject: same layout, accent family swapped via `image.palette`
  (`java`=red, `spring`=green, `ai`/`orange`=orange; omit for the default violet).
  Palettes live in `src/linkedin_pipeline/palettes.py`; only the gpt-image-2
  renderer honors them.
- New content follows the hard rules in `scripts/PROMPT_GERACAO.md` (hook, length,
  diagram density) — they encode measured LinkedIn performance data.
- Language of content, code and docs: English (target audience: international).
