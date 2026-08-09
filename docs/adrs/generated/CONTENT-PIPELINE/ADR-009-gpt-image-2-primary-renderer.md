# ADR-009 — gpt-image-2 as primary card renderer (Mermaid/HTML as fallback)

- Status: accepted (2026-08-09, owner-requested) · Amends ADR-008
- Domain: CONTENT-PIPELINE

## Context

The owner found the HTML/Mermaid card visually weak and asked about gpt-image-2.
Research (`docs/research/image-models-2026.md`) confirmed: **gpt-image-2** (OpenAI,
April 2026) is the current #1 model for text-accurate infographics (~99% label
accuracy in scientific-diagram head-to-heads, vs ~95% for Google Nano Banana Pro,
which garbles small labels). Crucially, the **approval gate (ADR-007) now catches
any residual typo before publishing** — the risk that killed full-AI cards in
ADR-006/008 is mitigated by design.

## Decision

Renderer chain in `run.py`:

1. **gpt-image-2** (`ai_card.py`) when `OPENAI_API_KEY` is set: generates the full
   infographic (1088×1360, exact 4:5) from a structured prompt containing the
   post's topic, headline, the **Mermaid diagram source as the layout spec** (same
   red/green/blue semantics) and the 3 takeaways, with hard rules: exact text,
   no watermark/brand/author. Quality `high` (US$0.165/image ≈ US$2.15/month) via
   `IMAGE_QUALITY`.
2. **Mermaid/HTML card** (ADR-008) on any AI failure — or forced via
   `CARD_RENDERER=mermaid`.
3. **Pillow gradient card** (ADR-003) as last resort.

## Alternatives considered

- **Google Nano Banana Pro (gemini-3-pro-image)** — rejected: loses to gpt-image-2
  on small-label accuracy (α→a, "Elasticseach"-style typos), which is exactly our
  content; no free API tier either.
- **Keep Mermaid-only** — rejected by owner (visually weak); retained as fallback.
- **gpt-image-1.5 / 1 / 1-mini** — superseded/cheaper tiers with worse text
  fidelity; gpt-image-1 retires 2026-10-23 (third-party report).

## Consequences

- Publishing cost ≈ US$0.165/post (only paid component; rejected renders cost the
  same again on re-run). Removing the secret restores the free Mermaid pipeline.
- Every AI card MUST pass the human approval gate — never bypass it while this
  renderer is active.
- The `image.diagram` field now serves both renderers: spec for gpt-image-2,
  source for Mermaid fallback.
