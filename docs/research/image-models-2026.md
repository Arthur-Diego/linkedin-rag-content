# Research — Image generation models for technical infographics (2026-08-09)

> Feeds ADR-009. Question: does gpt-image-2 exist, and which model renders
> text-heavy technical cards best?

## OpenAI lineup (Aug 2026)

| Model | Notes | Portrait price (low/med/high) |
|---|---|---|
| **gpt-image-2** (2026-04-21) | flagship; thinking mode; multilingual text; up to 3840px | $0.005 / $0.041 / **$0.165** |
| gpt-image-1.5 | previous flagship; API removal reported for 2026-12-01 | $0.013 / $0.05 / $0.20 |
| gpt-image-1 | retirement reported for 2026-10-23 | up to $0.25 |
| gpt-image-1-mini | cheap tier, weak text fidelity | ~$0.005–0.052 |

Endpoint: `POST /v1/images/generations`; `size` free-form (multiples of 16, ≤3:1 —
we use 1088×1360 = exact 4:5); `quality: low|medium|high|auto`; no free tier.

## Text-accuracy verdict

- Arena rankings (LMArena/Artificial Analysis): gpt-image-2 debuted and remains #1
  for text-to-image and editing.
- Scientific-diagram head-to-head (apiyi, 6 dimensions): gpt-image-2 ≈99% text
  accuracy incl. 8pt sub-labels; **Nano Banana Pro** (`gemini-3-pro-image`,
  $0.134/img) ≈95% with typos on small labels ("Evualation", α→a) — strong for
  long-paragraph posters, weaker for dense diagram labels.
- Reviews converge: choose gpt-image-2 for readable labels, ordered panels,
  diagrams, UI-like layouts (exactly our card).
- ByteByteGo-style cards (title + labeled flowchart + numbered takeaways) are
  reliably achievable; human review still recommended — which our approval gate
  (ADR-007) provides.

## Sources

developers.openai.com/api/docs (models/gpt-image-2, image-generation guide,
pricing) · ai.google.dev/gemini-api/docs (image-generation, pricing) ·
help.apiyi.com (gpt-image-2 vs nano-banana-pro scientific diagram test) ·
LMArena / Artificial Analysis image arena · costgoat.com/pricing/openai-images.
Deprecation dates are third-party reports (medium confidence).
