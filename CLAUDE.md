# linkedin-rag-content

Automated pipeline for technical RAG posts on LinkedIn: versioned content queue →
card image (optional gpt-image-1 background + Pillow text overlay) → LinkedIn
Posts API (or draft issue), scheduled by GitHub Actions 3x/week.

## Context index (everything lives in docs/)

- PRD: `docs/prd.md`
- Domain HLD: `docs/domains/content-pipeline/hld.md`
- Feature 1 FDD: `docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`
- Diagrams: `docs/domains/content-pipeline/diagrams/mermaid/`
- ADRs: `docs/adrs/generated/CONTENT-PIPELINE/` (001–006)
- Python guidelines: `docs/guidelines/python.md`
- Research (LinkedIn API / Napkin): `docs/research/linkedin-napkin-apis.md`
- Gitflow: `docs/gitflow.md` · DD config: `docs/dd.md`
- Operations runbook (tokens, troubleshooting): `docs/operations/runbook.md`

## Commands

- Tests: `python -m pytest tests/ -q`
- Local pipeline run (no publish): `PYTHONPATH=src python -m linkedin_pipeline.run --dry-run`
- Generate new queue posts: follow `scripts/PROMPT_GERACAO.md`

## Project rules

- Zero runtime cost is a requirement; the ONLY allowed paid dependency is the
  optional OpenAI image background (ADR-006), which must always fall back to the
  local gradient.
- Queued posts: markdown with YAML frontmatter in `content/queue/NNN-slug.md`;
  published ones move to `content/published/`.
- Language of content, code and docs: English (target audience: international).
