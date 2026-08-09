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
  prompt: "abstract illustration idea"   # optional; AI background art direction
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
| `renderer` | `render_card(post, out_path, background=None)` | 1200×1350 PNG, chip, headline, bullets, footer; background = darkened AI illustration or default gradient |
| `ai_renderer` | `build_prompt(post)`, `generate_background(api_key, prompt)` | gpt-image-1 textless background from `image.prompt` (or topic default); raises `AIImageError` on failure (ADR-006) |
| `linkedin` | `publish(token, version, caption, image_path, alt_text)` | userinfo → initializeUpload → PUT binary → POST /rest/posts; returns id |
| `run` | CLI `python -m linkedin_pipeline.run [--dry-run] [--root PATH]` | orchestrates and emits outputs for GitHub Actions |

## 4. `run` flow

1. `next_post` — empty queue → logs `QUEUE_EMPTY`, outputs `queue_empty=true`,
   `mode=none`, exit 0.
2. With `OPENAI_API_KEY` set: try an AI background (`ai_renderer`); any failure logs
   and falls back to the gradient — never blocks publishing.
3. `render_card` → `out/<id>.png`; caption → `out/<id>-caption.txt`.
4. `--dry-run` → stops here (no LinkedIn API, no move) → `mode=dry-run`.
5. `LINKEDIN_ACCESS_TOKEN` present → `linkedin.publish` → `mark_published` →
   `mode=published`.
6. No token → `mode=draft` (the post does NOT leave the queue; artifacts committed
   by the workflow and an issue opened with the caption).

Outputs emitted to `$GITHUB_OUTPUT` (run ↔ workflow contract):

| Output | Values |
|---|---|
| `mode` | `none` (empty queue) · `dry-run` · `published` · `draft` |
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
| DejaVu font missing | falls back to Pillow's default font (degrades aesthetics, does not fail) |
| OpenAI image API failure (quota, 401, timeout) | logs the error and falls back to the gradient background; job continues |
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
