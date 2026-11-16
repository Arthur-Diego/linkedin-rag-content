# linkedin-rag-content

Automated pipeline for technical posts on LinkedIn: versioned content queue →
animated system-design GIF rendered locally and committed (ADR-010) → human approval
gate → LinkedIn Posts API (or draft issue), scheduled by GitHub Actions 3x/week.
The previous static-card pipeline (gpt-image-2 → Mermaid → Pillow) is switched off
via `MEDIA_MODE` and kept in the code.

## Context index (everything lives in docs/)

- PRD: `docs/prd.md`
- Domain HLD: `docs/domains/content-pipeline/hld.md`
- Feature 1 FDD: `docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`
- Diagrams: `docs/domains/content-pipeline/diagrams/mermaid/`
- ADRs: `docs/adrs/generated/CONTENT-PIPELINE/` (001–010)
- Python guidelines: `docs/guidelines/python.md`
- Research: `docs/research/linkedin-napkin-apis.md` (APIs),
  `docs/research/linkedin-tech-content-playbook.md` (content/copy rules)
- Gitflow: `docs/gitflow.md` · DD config: `docs/dd.md`
- Operations runbook (tokens, troubleshooting): `docs/operations/runbook.md`

## Commands

- Tests: `python -m pytest tests/ -q`
- List the queue (publication order + GIF rendered/missing): `PYTHONPATH=src python -m linkedin_pipeline.run --list`
- Render the GIFs of queued posts: `PYTHONPATH=src python -m linkedin_pipeline.animate`
  (`<id> --force` to redo one, `<id> --preview` for a live HTML in `out/preview/`)
- Local pipeline check (no publish): `PYTHONPATH=src python -m linkedin_pipeline.run --dry-run`
- Generate new queue posts from a subject: `/linkedin-gifs <subject> [count]`
  (skill in `.claude/skills/linkedin-gifs/`; rules in `scripts/PROMPT_GERACAO.md`)

## Project rules

- Media mode: `MEDIA_MODE=gif` (default, set in the workflow). Each mode only sees its
  own posts: `animation:` posts in gif mode, `image:` posts in card mode. The card
  posts still in the queue are parked, not lost; flip `MEDIA_MODE: card` to resume them.
- Queued posts: markdown with YAML frontmatter in `content/queue/NNN-slug.md` with an
  `animation:` block; published ones move to `content/published/`.
- GIFs are rendered locally (`linkedin_pipeline.animate`, needs Playwright Chromium +
  ffmpeg) and committed as `out/NNN.gif` together with the post. CI never renders
  them; a queued post without its GIF fails the run.
- Posts only go out in the morning (06:00-12:00 São Paulo): the cron fires the evening
  before and the publish job enforces the window (runbook §4).
- LinkedIn accepts at most 250 frames per GIF: at 15 fps an animation must stay under
  16.6 s (enforced by the renderer).
- Scenes live in `assets/scenes/`: `flow.html` is the generic spec-driven engine;
  a post may point `animation.scene` to a hand-written one (e.g. `token-bucket`).
- The pipeline is free in gif mode. gpt-image-2 (ADR-009, ~US$0.17/image) is only used
  in card mode, whose Mermaid/Pillow fallbacks must keep working without the key.
- New content follows the hard rules in `scripts/PROMPT_GERACAO.md` (hook, length,
  animation density) — they encode measured LinkedIn performance data.
- Language of content, code and docs: English (target audience: international).
