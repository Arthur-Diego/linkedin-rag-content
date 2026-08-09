# ADR-006 — AI-generated card background via gpt-image-1 (optional, paid)

- Status: accepted (2026-08-09, owner-approved — supersedes part of ADR-003)
- Domain: CONTENT-PIPELINE

## Context

ADR-003 chose fully local Pillow rendering to keep the pipeline at zero cost. The
owner later provided an OpenAI API key and accepted a small cost (~US$0.5–2/month at
3 posts/week) in exchange for richer visuals.

## Decision

When the `OPENAI_API_KEY` secret is present, generate an **abstract, textless
background illustration** with **gpt-image-1** (1024×1536, medium quality) from the
post's `image.prompt` (or a topic-based default prompt), then **overlay all text with
Pillow** (chip, headline, bullets, footer) on a darkened version of it.

Hybrid rather than full-AI cards because image models still garble typography;
keeping text rendering in Pillow guarantees crisp, correct copy on every post.

**Fallback**: any failure (missing key, quota, API error) silently reverts to the
ADR-003 gradient — image generation can never break publishing.

## Alternatives considered

- **Full AI card (text included in the image)** — rejected: unsupervised typography
  errors would ship straight to LinkedIn.
- **Napkin AI** — rejected in ADR-003 (credit-based pricing, preview API).
- **Keep gradient only** — rejected by owner preference for richer visuals.

## Consequences

- The only paid component of the system; removable at any time by deleting the secret.
- ADR-003's Pillow renderer remains the guaranteed baseline and the test target.
- Per-post art direction via the optional `image.prompt` frontmatter field.
