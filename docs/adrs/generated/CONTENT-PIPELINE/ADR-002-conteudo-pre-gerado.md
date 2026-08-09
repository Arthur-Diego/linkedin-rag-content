# ADR-002 — Pre-generated, versioned content (no LLM at runtime)

- Status: accepted (2026-08-09, autonomous mode)
- Domain: CONTENT-PIPELINE

## Context

The original plan had Claude generating the content inside the scheduled job.
Calling an LLM at runtime in CI requires an Anthropic API key (cost per token) or a
Claude Code Action integration with OAuth — more moving parts and potential cost,
against the zero-cost requirement.

## Decision

Keep a **queue of pre-generated posts** (`content/queue/NNN-slug.md`, markdown with
YAML frontmatter) written by Claude Code **locally, on the owner's account** (cost
already covered by the subscription). The scheduled job only consumes the queue.
Replenishment is guided by the official prompt in `scripts/PROMPT_GERACAO.md`, and an
automatic issue warns when ≤ 2 posts remain.

## Alternatives considered

- **Claude API in CI** — rejected: cost per run.
- **claude-code-action with an OAuth token in CI** — rejected for now: extra setup and
  a sensitive credential dependency in the repo; may become a future evolution.
- **Static templates without an LLM** — rejected: insufficient content quality.

## Consequences

- Human in the loop every ~3 weeks (running the replenishment prompt) — acceptable.
- Reviewable quality: posts sit in a PR/commit before going live.
- The pipeline itself is 100% deterministic and testable.
