# ADR-001 — Scheduler: GitHub Actions cron

- Status: accepted (2026-08-09, autonomous mode)
- Domain: CONTENT-PIPELINE

## Context

The pipeline must run 3x/week with no server of its own and at no cost (PRD).

## Decision

Use **GitHub Actions** with `schedule` (cron Mon/Wed/Fri 11:30 UTC ≈ 08:30 BRT) and
`workflow_dispatch` for manual runs, on a **public repository** (unlimited Actions
minutes).

## Alternatives considered

- **Cron on a local machine (WSL2)** — rejected: the machine must be powered on; fragile.
- **Cloud scheduler (AWS/GCP)** — rejected: requires a cloud account, credit card, and
  infrastructure for a 1-minute job.
- **Claude Code scheduled routines (cloud)** — rejected as the primary scheduler:
  couples publishing to the Claude account; Actions is easier to observe and debug.

## Consequences

- GitHub's cron is best-effort (delays of minutes) — acceptable for social media.
- The workflow needs `permissions: contents: write, issues: write` to commit the
  result and open issues.
- A public repo exposes the queue of upcoming posts — accepted (the content will be
  public anyway).
