# FDD 001 — Automated publishing pipeline

> Approved 2026-08-09 (autonomous mode). Groundwork: `../hld.md`, `docs/prd.md`,
> ADRs 001–005.

## 1. Goal

A job that, on each scheduler trigger, publishes the next post from the queue to
LinkedIn (text + rendered image) or, without a token, delivers the finished post
as a draft.

## 2. Queued post format

`content/queue/NNN-slug.md` — markdown with YAML frontmatter:

```yaml
---
id: "001"                # orders the queue (lowest first)
topic: chunking          # chip displayed on the card
title: "Internal title"
image:
  headline: "Card headline (short)"
  bullets:
    - "line 1"
    - "line 2"
    - "line 3"
  style: spec                            # optional: spec | free; default alternates by id parity (odd=spec, even=free)
  diagram: |                             # Mermaid flowchart — spec-mode centerpiece, fallback source for free mode
    flowchart LR
        A["Start"]:::accent --> B["End"]:::good
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
alt_text: "image description for accessibility"  # optional; fallback = title
status: ready            # ready | published
---
Body of the LinkedIn caption (with hashtags at the end).
```

On publish: the frontmatter gains `status: published`, `published_at` (ISO-8601 UTC)
and `linkedin_post_id`; the file moves to `content/published/`.

## 3. Modules

| Module | Public function | Behavior |
|---|---|---|
| `queue_store` | `next_post(root)` | lowest `id` with `status: ready`; `None` if empty |
| | `count_ready(root)` | posts remaining in the queue |
| | `mark_published(root, post, post_id)` | updates frontmatter + moves to published/ |
| `ai_card` | `resolve_style(post)`, `build_prompt(post)`, `render_card(api_key, post, out_path, quality)` | gpt-image-2 card 1088×1360 (4:5), two styles: **spec** (Mermaid diagram as exact layout spec) and **free** (creative composition around the headline + takeaways); explicit `image.style` wins, default alternates by id parity; raises `AICardError` (ADR-009) |
| `html_renderer` | `build_html(post)`, `render_card(post, out_path)` | 1200×1350 PNG from `assets/card_template.html`: Inter type, Mermaid diagram from `image.diagram`, 3 numbered takeaways; Playwright/Chromium screenshot; raises `HTMLRenderError` (ADR-008) |
| `renderer` | `render_card(post, out_path)` | Pillow gradient card — emergency fallback when Playwright is unavailable (ADR-003) |
| `linkedin` | `publish(token, version, caption, image_path, alt_text)` | userinfo → initializeUpload → PUT binary → POST /rest/posts; returns id |
| `run` | CLI `python -m linkedin_pipeline.run [--dry-run] [--render-only] [--publish-only] [--root PATH]` | orchestrates and emits outputs for GitHub Actions; `--render-only`/`--publish-only` split the approval flow (ADR-007) |

## 4. `run` flow

1. `next_post` — empty queue → logs `QUEUE_EMPTY`, outputs `queue_empty=true`,
   `mode=none`, exit 0.
2. Render `out/<id>.png` through the chain: `ai_card` (gpt-image-2, when
   `OPENAI_API_KEY` is set and `CARD_RENDERER` ≠ `mermaid`) → `html_renderer`
   (Mermaid card) → Pillow gradient. Each failure logs and falls through —
   rendering never blocks publishing.
3. Caption → `out/<id>-caption.txt`.
4. `--dry-run` → stops here (no LinkedIn API, no move) → `mode=dry-run`.
5. `--render-only` (approval flow, stage 1) → stops here → `mode=rendered`; the
   workflow commits `out/` and shows a preview in the job summary.
6. `--publish-only` (approval flow, stage 2, runs after human approval) → skips
   rendering and REUSES `out/<id>.png` (fails with exit 1 if missing); then follows
   the token logic below.
7. `LINKEDIN_ACCESS_TOKEN` present → `linkedin.publish` → `mark_published` →
   `mode=published`.
8. No token → `mode=draft` (the post does NOT leave the queue; artifacts committed
   by the workflow and an issue opened with the caption).

Outputs emitted to `$GITHUB_OUTPUT` (run ↔ workflow contract):

| Output | Values |
|---|---|
| `mode` | `none` (empty queue) · `dry-run` · `rendered` · `published` · `draft` |
| `queue_empty` | `true` / `false` |
| `queue_remaining` | integer (workflow opens a replenishment issue if ≤ 2) |
| `post_id`, `post_title` | post identification (absent when the queue is empty) |
| `image_path`, `caption_path` | relative artifact paths (likewise) |

## 5. External contract consumed (LinkedIn, versioned API)

- `GET /v2/userinfo` → `sub` → author `urn:li:person:{sub}`.
- `POST /rest/images?action=initializeUpload` body
  `{"initializeUploadRequest":{"owner":"<author>"}}` → `uploadUrl` + `image` URN.
- `PUT <uploadUrl>` with the PNG binary and `Authorization: Bearer`.
- `POST /rest/posts` (201 + `x-restli-id` header):

```json
{
  "author": "urn:li:person:{sub}",
  "commentary": "<caption with reserved characters escaped>",
  "visibility": "PUBLIC",
  "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                    "thirdPartyDistributionChannels": []},
  "content": {"media": {"altText": "<alt_text>", "id": "urn:li:image:..."}},
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

- Headers: `LinkedIn-Version: <LINKEDIN_VERSION, default 202606>`,
  `X-Restli-Protocol-Version: 2.0.0`, `Content-Type: application/json`.
- Commentary escaping (little-text format): prefix `\` to
  `\ | { } [ ] ( ) < > * _ ~` — `#` and `@` stay untouched (hashtags/mentions).

## 6. Error matrix

| Scenario | Behavior |
|---|---|
| Empty queue | exit 0, `queue_empty=true`, replenishment issue |
| HTTP ≠ 2xx on any LinkedIn call | `LinkedInError` with status + body; job fails (visible in Actions) |
| 401 (expired token) | same as above; runbook covers renewal |
| Invalid frontmatter in a post | `ValueError` naming the file; job fails |
| gpt-image-2 failure (quota, 401, timeout, bad response) | `AICardError` logged; falls back to the Mermaid card; job continues |
| Playwright missing / Mermaid syntax error / render timeout | `HTMLRenderError` logged; falls back to the Pillow gradient card; job continues |
| DejaVu font missing (fallback card only) | falls back to Pillow's default font (degrades aesthetics, does not fail) |
| `--publish-only` without a rendered image in `out/` | exit 1 with a clear message; queue untouched |
| Duplicate post (`CONTENT_DUPLICATE`) | job fails; operator removes/edits the queued post |

## 7. Acceptance criteria

1. `--dry-run` with a stocked queue generates PNG + caption in `out/` and does not
   change the queue.
2. Without a token and without `--dry-run`, outputs indicate `mode=draft` and the
   queue is not consumed.
3. With a token (mocked in tests), the payload sent matches section 5 and the post
   moves to `content/published/` with `published_at` and `linkedin_post_id`.
4. An empty queue exits with code 0 and `queue_empty=true`.
5. `pytest` green covering the queue, renderer, and LinkedIn client (mocked).

## 8. Observability

Logs on the job's stdout; structured outputs via `$GITHUB_OUTPUT`; issues as the
notification channel. No additional metrics (scale of 3 runs/week).
