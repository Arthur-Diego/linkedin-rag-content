# ADR-007 — Human approval gate via GitHub Environments

- Status: accepted (2026-08-09, owner-approved)
- Domain: CONTENT-PIPELINE

## Context

With AI-generated backgrounds (ADR-006), each card is unique and non-deterministic.
The owner wants to see the image (and caption) before it reaches their LinkedIn
profile, with a push/e-mail notification and one-click approval.

## Decision

Split the workflow into two jobs:

1. **`prepare`** (unattended): renders image + caption, commits them to `out/`, and
   writes a preview (inline image + caption) to the job summary.
2. **`publish`**: bound to the **`linkedin` environment**, which has the owner as a
   **required reviewer**. GitHub pauses the job and notifies the owner (e-mail +
   GitHub mobile push); on Approve it publishes **the exact artifacts rendered by
   `prepare`** (`--publish-only`, no re-render — AI output is not reproducible);
   on Reject nothing is published and the post stays queued.

## Alternatives considered

- **Issue-based approval (comment "approve")** — rejected: requires a custom
  listener workflow and label plumbing; Environments give pause + notification +
  audit natively.
- **`workflow_dispatch` manual second stage** — rejected: no notification, two
  manual steps instead of one click.
- **Keep full auto-publish** — rejected by owner: wants editorial control over
  AI-generated visuals.

## Consequences

- Publishing time becomes "cron time + approval delay"; pending approvals expire
  after 30 days (post is never lost — it stays in the queue).
- An unapproved run holds the `publish` concurrency group; stale runs should be
  rejected/cancelled (runbook §5).
- Approval is free on public repos and fully audited in the deployment history.
