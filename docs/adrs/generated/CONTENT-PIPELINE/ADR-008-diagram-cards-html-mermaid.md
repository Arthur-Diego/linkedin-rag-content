# ADR-008 — Didactic diagram cards via HTML/Mermaid/Playwright (supersedes ADR-006)

- Status: accepted (2026-08-09, owner-requested) · Supersedes: ADR-006, amends ADR-003
- Domain: CONTENT-PIPELINE

## Context

The owner rejected the first AI-background card: not professional or didactic
enough. Research (`docs/research/linkedin-tech-content-playbook.md`) shows top
technical creators (ByteByteGo, Level Up Coding) win with **infographic-style
diagram cards**: one concept, system-design flows, short labels, light background,
clean typography — optimized for saves (1 save ≈ 5× a like in reach).

## Decision

Render cards from an **HTML template** (`assets/card_template.html`) screenshot by
**Playwright/Chromium**: Inter typography (vendored woff2), subtle grid background,
title, a **real Mermaid flowchart** (vendored `mermaid.min.js`, no network) as the
centerpiece, 3 numbered takeaways, brand footer. Each post carries its diagram as
Mermaid code in `image.diagram` with standard classes (`bad`/`good`/`accent`).

gpt-image-1 backgrounds (ADR-006) are **retired**: abstract art added cost without
didactic value. The Pillow gradient card (ADR-003) remains the emergency fallback
when Playwright is unavailable.

## Alternatives considered

- **Keep AI backgrounds** — rejected by owner (not professional/didactic).
- **Pillow-drawn diagrams** — rejected: box/arrow layout by hand in Pillow is a
  layout engine reimplementation; Mermaid does it properly.
- **Mermaid CLI (mmdc)** — rejected: also needs a headless browser but without
  control over the surrounding card design.
- **Excalidraw-style hand-drawn** — attractive, but no headless deterministic
  pipeline; possible future evolution.

## Consequences

- CI installs Chromium (~1 min, cached via actions/cache); render is deterministic
  and free — the pipeline is back to 100% zero-cost.
- Diagram quality is authored, not generated: the content prompt
  (`scripts/PROMPT_GERACAO.md`) carries hard rules for labels, density and classes.
- `OPENAI_API_KEY` is no longer used (secret can be removed).
