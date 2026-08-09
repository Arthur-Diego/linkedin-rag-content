# ADR-005 — State in git (no database)

- Status: accepted (2026-08-09, autonomous mode)
- Domain: CONTENT-PIPELINE

## Context

The system needs to know which posts are pending and which have already been
published. Any external database/storage (S3, DynamoDB, hosted SQLite) adds cost or
infrastructure for a tiny amount of state.

## Decision

The **git repository is the only storage**: `content/queue/` = pending,
`content/published/` = history (with `published_at` and the post id in the
frontmatter), `out/` = generated images. The Actions job commits the transition to
`main` (`publish: <id> <title>`).

## Alternatives considered

- **S3/GCS** — rejected: cloud account and cost for a few bytes of state.
- **SQLite in the repo** — rejected: a binary in git hampers diff/review; markdown is
  readable and editable.
- **GitHub Releases/Artifacts as storage** — rejected: artifacts expire and are not
  an auditable source of truth.

## Consequences

- Complete history, auditable via `git log`.
- Concurrency is a non-issue (one job at a time; `concurrency` in the workflow
  guarantees it).
- `main` must never be rewritten (the bot depends on fast-forward) — rule in
  `docs/gitflow.md`.
