# Runbook — Pipeline operations

## 1. Obtain/renew the LinkedIn token (every ~50 days)

1. Go to https://www.linkedin.com/developers/apps → your app (create one on first
   access; requires linking a Company Page — a simple page will do).
2. **Products** tab: add **Share on LinkedIn** and **Sign In with LinkedIn using
   OpenID Connect** (instant approval).
3. **Auth** tab → scroll to **OAuth 2.0 tools** → **Token Generator**: select the
   scopes `openid`, `profile`, `w_member_social` → generate the token (valid 60 days).
4. In the GitHub repository: Settings → Secrets and variables → Actions →
   secret `LINKEDIN_ACCESS_TOKEN` → paste the token.
5. Manual test: Actions tab → `publish-linkedin` workflow → Run workflow.

> Standard apps have no programmatic refresh token (approved-partner feature).
> Manual renewal is the supported path. Set a reminder (~50 days).

## 2. Symptoms and fixes

| Symptom | Likely cause | Action |
|---|---|---|
| Job fails with `LinkedInError 401` | expired/invalid token | renew the token (section 1) |
| Job fails with `LinkedInError 422 CONTENT_DUPLICATE` | caption identical to a recent post | edit the queued post |
| Job fails with `LinkedInError 426/400` citing the version | `LinkedIn-Version` retired | update the `LINKEDIN_VERSION` variable in the workflow to an active `YYYYMM` |
| "Content queue running low" issue | ≤ 2 ready posts | run `scripts/PROMPT_GERACAO.md` in Claude Code and commit new posts |
| Post didn't go out on time | GitHub's cron is best-effort (hours late), or the approval is still pending | check the Actions tab; approve the waiting run in the morning window |
| publish job fails with `outside the ... morning window` | approved in the afternoon/night | re-run the failed job the next morning (section 4) |
| prepare job fails with `out/NNN.gif not found` | post pushed without its GIF | run `python -m linkedin_pipeline.animate NNN` locally, commit `out/NNN.gif`, re-run the workflow |
| `animate` fails with `at most 250` frames | animation longer than 16.6 s (LinkedIn GIF limit) | shorten steps (`seconds`, `count`, `every`) |
| `animate` fails with `ffmpeg not found` / `frame capture failed` | local tooling missing | `brew install ffmpeg` · `python -m playwright install chromium` |
| GIF shows as a still image on LinkedIn | LinkedIn does not document GIF autoplay for API posts | check on the profile; fallback is posting `out/preview/NNN.mp4` (`animate NNN --mp4`) by hand |
| Queue reported empty but `content/queue/` has posts | they are card posts, parked while `MEDIA_MODE: gif` | add animated posts, or set `MEDIA_MODE: card` in the workflow to resume the card pipeline |
| (card mode) Card is the plain Mermaid style (not the AI infographic) | gpt-image-2 failed: quota/billing/key — see `AICardError` in the prepare log | check OpenAI billing or the `OPENAI_API_KEY` secret; the fallback card is still publishable |
| (card mode) Card came out as a plain gradient (no diagram) | Playwright/Chromium failed or Mermaid syntax error in `image.diagram` | check the prepare job log for `HTMLRenderError`; fix the diagram or the Chromium install step |
| (card mode) AI card has a typo or wrong arrow | gpt-image-2 imperfection (~1% of labels) | Reject in the approval gate and re-run the workflow — each render is unique |

## 3. Publishing a draft manually

Draft mode (no token): the issue carries the ready caption and the image path in
`out/`. Copy the caption, download the image from the repository, and post via the
LinkedIn app. Then move the post file from `content/queue/` to `content/published/`,
changing `status: published` (or run the pipeline with a token configured, which does
this on its own).

## 4. Schedule: posts go out in the morning

- **Days**: Mon/Wed/Fri. The cron in `.github/workflows/publish.yml` is
  `0 0 * * 1,3,5` (UTC) = 21:00 São Paulo time the evening before. GitHub delivered
  this workflow's cron 4-10 hours late between Sep and Nov 2026 (an 08:30 schedule
  fired between 12:00 and 18:30), so it is fired early on purpose: the approval
  request is already waiting when the morning starts.
- **Morning window**: the publish job refuses to post outside 06:00-12:00
  (`PUBLISH_TZ`, `PUBLISH_FROM_HOUR`, `PUBLISH_UNTIL_HOUR` in the workflow env).
  Approved outside the window: the job fails without publishing and the post stays
  queued. Open the run the next morning → **Re-run failed jobs** → approve again.
- **Override**: Actions → publish-linkedin → Run workflow → check `any_time`.
- To change days or window, edit the cron (UTC) and the three `PUBLISH_*` values.

## 5. Approving a post (approval flow — ADR-007)

Each run pauses before publishing and GitHub notifies you (e-mail "Review required"
+ push on the GitHub mobile app):

1. Open the run (link in the notification) → the **prepare** job summary shows the
   card image and the caption.
2. Click **Review deployments** → check `linkedin` → **Approve and deploy**
   (publishes) or **Reject** (nothing goes out; the post stays in the queue).
   Approve between 06:00 and 12:00 São Paulo time: outside that window the job stops
   without publishing (section 4).

Notes:
- A pending approval expires in 30 days; the post is never lost.
- An unapproved run blocks the next scheduled one (concurrency): reject or cancel
  stale runs you don't want.
- Want a different animation? Reject, edit the post's `animation:` block, re-render
  with `animate NNN --force`, push, and re-run the workflow.
- To go back to fully automatic publishing: remove the required reviewer from the
  `linkedin` environment (Settings → Environments).
