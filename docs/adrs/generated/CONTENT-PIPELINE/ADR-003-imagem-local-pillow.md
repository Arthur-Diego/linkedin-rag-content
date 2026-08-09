# ADR-003 — Image: local rendering with Pillow (not Napkin AI)

- Status: accepted (2026-08-09, autonomous mode)
- Domain: CONTENT-PIPELINE

## Context

The original plan used the Napkin AI API to generate the visuals. Research
(`docs/research/linkedin-napkin-apis.md`) showed that Napkin's API is in developer
preview and **consumes paid credits** (free ≈ 3 visuals; plans US$9–22/mo) —
incompatible with zero cost in continuous automation.

## Decision

Render a **1200×1350 PNG card** locally (4:5 ratio, ideal for the feed) with
**Pillow**: dark gradient background, topic chip, large title, bullets, and a
branding footer. Each post declares `image.headline` and `image.bullets` in its
frontmatter.

## Alternatives considered

- **Napkin AI API** — rejected: costs credits.
- **HTML→PNG via Playwright** — rejected: ~300 MB of browser on the runner and extra
  slowness for marginal aesthetic gain; possible future evolution.
- **QuickChart/Kroki (hosted)** — rejected as the default: external service dependency
  with limits; diagram aesthetics, not social-card aesthetics.

## Consequences

- Consistent, self-branded visuals, though simpler than AI illustrations.
- Zero external dependencies: rendering runs offline and on any runner.
- Typeface: DejaVu (present on the Ubuntu runner); falls back to Pillow's default
  font.
