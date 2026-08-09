# ADR-004 — Publishing: LinkedIn Posts API with draft mode as fallback

- Status: accepted (2026-08-09, autonomous mode)
- Domain: CONTENT-PIPELINE

## Context

Publishing requires LinkedIn's official API (free, but with manual setup: an app in
the Developer Portal + a 60-day OAuth token with no programmatic refresh for standard
apps). The system must be useful today, before that setup.

## Decision

Publish via the **versioned LinkedIn Posts API** (`/rest/posts` + `/rest/images`,
parameterized `LinkedIn-Version` header) when `LINKEDIN_ACCESS_TOKEN` is configured
as a secret. **Without a token, operate in draft mode**: render the image, commit it
to `out/`, and open a GitHub issue with the caption ready to paste — the post stays
in the queue.

## Alternatives considered

- **Third-party schedulers (Buffer etc.)** — rejected: limited free tiers, third-party
  credentials, less control.
- **Browser automation (selenium) on LinkedIn** — rejected: violates the ToS, risk of
  account lockout.
- **Draft only (no API)** — rejected as the end state: does not satisfy "automated".

## Consequences

- One-time setup documented in the runbook (`docs/operations/runbook.md`); token
  renewal every ~50 days via the Developer Portal's Token Generator.
- A 401/expired token brings the job down with a clear error; a reminder issue is opened.
- The same code serves both modes — draft is the natural degradation path.
