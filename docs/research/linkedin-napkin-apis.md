# Research — LinkedIn API and Napkin AI (2026-08-09)

> Targeted research (condensed format; the topic did not justify a 16-section Deep
> Research — decision per the dd-greenfield Step 2 rule). Feeds the HLD and the ADRs.

## LinkedIn — publishing to a personal profile

- **Free and self-serve**: create an app at https://www.linkedin.com/developers/apps
  (requires associating a Company Page), add the products **"Share on LinkedIn"**
  (grants `w_member_social`) and **"Sign In with LinkedIn using OpenID Connect"**
  (grants `openid profile`, needed for `GET /v2/userinfo` → `sub` field → author
  `urn:li:person:{sub}`).
- **Current (versioned) API**: `POST https://api.linkedin.com/rest/posts` with headers
  `LinkedIn-Version: YYYYMM` (monthly versions expire — keep it parameterized),
  `X-Restli-Protocol-Version: 2.0.0`. Success: `201` + id in the `x-restli-id` header.
- **Image**: `POST /rest/images?action=initializeUpload` with
  `{"initializeUploadRequest": {"owner": "urn:li:person:{sub}"}}` → the response carries
  `uploadUrl` (PUT the binary with Bearer auth) and `image` (`urn:li:image:...`), which
  goes into the post's `content.media.id`. PNG/JPG/GIF.
- **Token**: valid for **60 days**; standard apps **have no refresh token** (exclusive
  to approved partners). Renewal: repeat OAuth in the browser or use the Developer
  Portal's **Token Generator** (OAuth Tools) — the recommended path for personal use.
- **Rate limit**: 150 requests/day per member — irrelevant for 3 posts/week.
  Watch out for `CONTENT_DUPLICATE` (LinkedIn rejects a repeated identical post).
- Minimal payload for a personal post with an image: see FDD section 5.

Sources: learn.microsoft.com/linkedin (share-on-linkedin, posts-api view=li-lms-2026-06,
images-api, authorization-code-flow, programmatic-refresh-tokens, rate-limits).

## Napkin AI

- The API exists (developer preview, token at app.napkin.ai → Settings → Developers),
  but it **consumes paid credits** from the account (free ≈ 3 visuals; plans US$9–22/mo).
- **Verdict: incompatible with the zero-cost requirement** → replaced by local
  rendering with Pillow (ADR-003).

## Free image alternatives evaluated

| Option | Pros | Cons |
|---|---|---|
| **Pillow (chosen)** | lightweight, offline, unlimited, fast in CI | manual layout, simpler visuals |
| HTML→PNG (Playwright) | full CSS, rich visuals | ~300 MB of browser on the runner, slow |
| QuickChart/Kroki | ready-made diagrams over HTTP | external service dependency, limits on hosted tiers |
