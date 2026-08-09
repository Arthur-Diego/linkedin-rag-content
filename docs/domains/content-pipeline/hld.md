# HLD — content-pipeline domain

> Approved 2026-08-09 (autonomous mode). Business source: `docs/prd.md`.

## 1. Vision

A scheduled job (GitHub Actions, Mon/Wed/Fri cron) consumes a queue of posts
versioned in git, renders the post image locally, and publishes to LinkedIn.
There is no server, database, or 24/7 service: **the repository is the system**.

## 2. Architecture

```
GitHub Actions (cron 3x/week or manual trigger)
  └─ python -m linkedin_pipeline.run
       ├─ queue_store: reads content/queue/, picks the post with the lowest id
       ├─ ai_renderer: optional gpt-image-1 background (OPENAI_API_KEY set;
       │               any failure falls back to the local gradient)
       ├─ renderer:    generates out/<id>.png (Pillow, card template)
       ├─ linkedin:    with LINKEDIN_ACCESS_TOKEN →
       │                 1. GET  /v2/userinfo            (member URN)
       │                 2. POST /rest/images?action=initializeUpload
       │                 3. PUT  <uploadUrl>              (PNG binary)
       │                 4. POST /rest/posts              (post + image)
       │               without a token → draft mode:
       │                 gh issue with the ready caption + committed image
       ├─ queue_store: moves the post to content/published/
       └─ (workflow step) commit/push of the result to main
```

## 3. Components

| Component | Responsibility | Technology |
|---|---|---|
| Content queue | pending/published posts, frontmatter format | git (`content/`) |
| `queue_store` | select the next post, move it to published | Python + PyYAML |
| `renderer` | 1200×1350 PNG card (title, bullets, footer) | Pillow |
| `ai_renderer` | optional textless AI background (ADR-006) | OpenAI gpt-image-1 |
| `linkedin` | image upload + post creation (versioned API) | requests |
| `run` | orchestration, CLI (`--dry-run`), draft mode | Python argparse |
| Scheduler | cron + `workflow_dispatch` + result commit | GitHub Actions (2 jobs) |
| Approval gate | pauses `publish` until the owner approves; notifies by e-mail/push | GitHub Environment `linkedin` (required reviewer) |
| Replenishment | generating new posts with Claude Code (human in the loop) | prompt in `scripts/` |

## 4. Main flows

**Publish (happy path, approval flow — ADR-007)**: cron fires → `prepare` job renders
PNG + caption (`--render-only`), commits them to `out/` and posts a preview in the job
summary → the `publish` job pauses on the `linkedin` environment and GitHub notifies
the owner (e-mail + mobile push) → on **Approve**: `--publish-only` reuses the exact
approved artifacts → upload image → create post → move to `published/` → commit
`publish(<mode>): <id> <title>`. On **Reject**: nothing is published; the post stays
in the queue.

**Draft (no token)**: same selection and render steps; instead of calling the API,
opens an issue in the repository with the caption ready to copy and the image path;
the post stays in the queue (is not consumed) until it is actually published or
moved manually.

**Low/empty queue** (`queue_remaining ≤ 2` or empty): the job finishes successfully and
opens the `Content queue running low` issue — only if one isn't already open — asking
for replenishment (prompt in `scripts/PROMPT_GERACAO.md`).

**Expired token (~60 days)**: the call returns 401 → job fails with a clear message →
the runbook `docs/operations/runbook.md` describes the renewal.

## 5. External contracts consumed

- OpenAI Images API (`POST /v1/images/generations`, model gpt-image-1) — optional,
  only when `OPENAI_API_KEY` is set; the only paid component (~US$0.5–2/month).
- Versioned LinkedIn API (`LinkedIn-Version: 2xxxxx`): `/v2/userinfo`,
  `/rest/images?action=initializeUpload`, `/rest/posts`. Auth: OAuth 2.0 member token
  with scopes `openid profile w_member_social`. Free for publishing to one's own profile.
- GitHub: `gh` CLI on the runner (issues) and plain git for commit/push. Auth: the
  workflow's `GITHUB_TOKEN`.

## 6. Structural decisions (→ ADRs)

1. Scheduler: GitHub Actions cron — ADR-001
2. Pre-generated, versioned content (no LLM at runtime) — ADR-002
3. Local image with Pillow (not Napkin AI) — ADR-003
4. Publishing: LinkedIn Posts API + draft mode as fallback — ADR-004
5. State in git (no database) — ADR-005
6. Optional AI card background via gpt-image-1, Pillow text overlay — ADR-006
7. Human approval gate via GitHub Environments — ADR-007

## 7. Observability and operations

- Job log = GitHub Actions log; an API failure brings the job down (visible + GitHub
  e-mail to the owner).
- Repo issues as the notification channel (draft ready / empty queue).
- Token runbook and troubleshooting in `docs/operations/runbook.md`.

## 8. Risks

| Risk | Mitigation |
|---|---|
| LinkedIn token expires in ~60 days | loud failure + renewal runbook; reminder issue |
| LinkedIn changes the API version | `LINKEDIN_VERSION` parameterized in a single place |
| Queue drains without warning | automatic issue when ≤ 2 posts remain |
| GitHub cron runs late (best-effort) | tolerable for social media; manual `workflow_dispatch` |
