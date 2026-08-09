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
| Post didn't go out on time | GitHub's cron is best-effort | check the Actions tab; trigger manually if needed |
| Card missing the nice font | DejaVu absent on the runner | not a failure; install `fonts-dejavu-core` in the workflow |

## 3. Publishing a draft manually

Draft mode (no token): the issue carries the ready caption and the image path in
`out/`. Copy the caption, download the image from the repository, and post via the
LinkedIn app. Then move the post file from `content/queue/` to `content/published/`,
changing `status: published` (or run the pipeline with a token configured, which does
this on its own).

## 4. Changing the schedule/frequency

Edit the cron in `.github/workflows/publish.yml` (UTC). Default:
`30 11 * * 1,3,5` = Mon/Wed/Fri 08:30 BRT.

## 5. Approving a post (approval flow — ADR-007)

Each run pauses before publishing and GitHub notifies you (e-mail "Review required"
+ push on the GitHub mobile app):

1. Open the run (link in the notification) → the **prepare** job summary shows the
   card image and the caption.
2. Click **Review deployments** → check `linkedin` → **Approve and deploy**
   (publishes) or **Reject** (nothing goes out; the post stays in the queue).

Notes:
- A pending approval expires in 30 days; the post is never lost.
- An unapproved run blocks the next scheduled one (concurrency): reject or cancel
  stale runs you don't want.
- Want a different image? Reject, edit the post's `image.prompt`, and re-run the
  workflow (Actions → publish-linkedin → Run workflow).
- To go back to fully automatic publishing: remove the required reviewer from the
  `linkedin` environment (Settings → Environments).
