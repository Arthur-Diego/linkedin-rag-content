# AGENTS

Guide for AI agents working in this repository. The full context index is in
`CLAUDE.md` — read it first; all context lives in `docs/`.

Essential rules:
- Zero runtime cost: the pipeline runs in gif mode (ADR-010), animated GIFs rendered
  locally and committed to `out/`. The paid gpt-image-2 card (ADR-009) is switched
  off behind `MEDIA_MODE: card`.
- Never rewrite `main`'s history (the publishing bot commits to it).
- New posts carry an `animation:` block and follow `scripts/PROMPT_GERACAO.md`; to
  create them from a subject use the skill in `.claude/skills/linkedin-gifs/SKILL.md`.
- All content, code, and docs in English.
- Validate with `python -m pytest tests/ -q` before finishing.
