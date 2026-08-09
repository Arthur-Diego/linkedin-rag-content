# AGENTS

Guide for AI agents working in this repository. The full context index is in
`CLAUDE.md` — read it first; all context lives in `docs/`.

Essential rules:
- Zero runtime cost (the only allowed paid piece is the optional AI background,
  ADR-006, which must always fall back to the local gradient).
- Never rewrite `main`'s history (the publishing bot commits to it).
- New posts follow the frontmatter format described in the FDD
  (`docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`).
- All content, code, and docs in English.
- Validate with `python -m pytest tests/ -q` before finishing.
