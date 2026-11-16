# ADR-010 — Animated system-design GIF, rendered locally, as the post media

- Status: accepted (2026-11-16, owner-requested) · Suspends ADR-009 (card renderers stay in the code)
- Domain: CONTENT-PIPELINE

## Context

The owner observed that the system-design posts that travel on LinkedIn are animated
diagrams ("dynamic pictures": packets flowing through an architecture) and asked for
the pipeline to produce that format instead of the static infographic card, keeping
the queue, the scheduled workflow and the approval gate. The profile is in English,
so content stays in English.

## Decision

1. **Post format**: queued posts carry an `animation:` block instead of `image:`.
   The default scene (`assets/scenes/flow.html`) is spec-driven: nodes on a grid,
   labelled edges, and timed steps with a caption, packets travelling a path,
   meters and a tally. A post may point `animation.scene` to a hand-written scene
   (e.g. `token-bucket`, a real simulation). Every scene exposes the same contract:
   `window.DURATION` and `window.renderAt(t)`, a pure function of time.
2. **Rendering is local** (`python -m linkedin_pipeline.animate`): Playwright steps
   the scene frame by frame (15 fps, 1080×1350) and ffmpeg encodes a looping GIF with
   a generated palette. The author looks at the GIF and commits `out/NNN.gif` with
   the post.
3. **CI only publishes**. `MEDIA_MODE=gif` (workflow env) makes `run.py` pick the next
   `animation:` post, require its committed GIF (missing GIF = failed run) and send it
   through the existing approval gate and LinkedIn Images/Posts API calls.
4. **The card pipeline is switched off, not removed**. `MEDIA_MODE=card` restores the
   ADR-009 chain. Each mode only sees its own posts, so the card posts still in the
   queue are parked untouched and resume when the mode is flipped back.

## Constraints verified

- LinkedIn Images API (learn.microsoft.com, read 2026-11-16): accepts "JPG, GIF, and
  PNG"; "GIF format supports up to 250 frames"; images under 36,152,320 pixels. The
  renderer rejects animations above 250 frames (16.6 s at 15 fps).
- Not documented by LinkedIn: whether a GIF uploaded through the Images API autoplays
  in the feed. Every scene therefore keeps a self-explanatory first frame (title and
  full diagram), and the first published post must be checked on the profile.

## Alternatives considered

- **Render the GIF in CI** — rejected: the author would approve an animation never
  watched in motion, and CI would need Chromium + ffmpeg on every run. A committed
  GIF is also exactly what gets published (no re-render drift).
- **MP4 video post** — sharper and smaller, but uses a different LinkedIn upload API
  (Videos API) and the owner asked for GIF. `animate --mp4` writes one to
  `out/preview/` for manual use.
- **Remotion / Motion Canvas** — richer authoring, but adds a Node toolchain and a
  company licence (Remotion) to a Python repo that already ships Playwright.
- **Hand-written scene per post** — most expressive, least reviewable; kept only as
  an escape hatch (`animation.scene`).

## Consequences

- Publishing cost drops to zero (no gpt-image-2 call in gif mode).
- The repository grows by about 1 MB per post (GIF in `out/`).
- Local setup now needs ffmpeg in addition to Playwright Chromium.
- A post committed without its GIF fails the scheduled run; `run --list` shows
  `gif:MISSING` before pushing.
