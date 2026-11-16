# linkedin-rag-content

An automated pipeline that publishes technical posts with animated system-design
diagrams to LinkedIn, 3x per week.

```
On your machine
   post in the queue (content/queue/NNN-slug.md, `animation:` block)
     └─► python -m linkedin_pipeline.animate  →  out/NNN.gif  (watch it)
           └─► git commit + push (post + GIF)

GitHub Actions (cron Mon/Wed/Fri)
   └─► next animated post from the queue + its committed GIF
         └─► ⏸ approval gate: GitHub notifies you (e-mail/push),
             you review the GIF + caption and click Approve
               └─► LinkedIn Posts API (with token)
                   or GitHub issue with the finished post (without token)
```

- **Free**: Actions on a public repo + LinkedIn's free official API; the GIF is
  rendered locally with Playwright and ffmpeg.
- **Animated by design**: each post is a looping diagram (packets flowing through an
  architecture, ByteByteGo school) described as data in the post's frontmatter;
  caption rules follow the research in
  `docs/research/linkedin-tech-content-playbook.md`.
- **State lives in git**: queue in `content/queue/`, history in
  `content/published/`, media in `out/`. No database, no server.
- **Content**: pre-generated with Claude Code and reviewable before going live.
- **Static cards switched off**: the previous gpt-image-2/Mermaid card pipeline is
  kept behind `MEDIA_MODE: card` in the workflow (ADR-010). Card posts still in the
  queue are parked until the mode is flipped back.

## How to use

### Works today (draft mode, no setup)

The workflow publishes Mon/Wed/Fri mornings, São Paulo time (or manually via **Actions →
publish-linkedin → Run workflow**). Without a token it:

1. Picks the next animated post and its committed GIF in `out/`.
2. Opens an **issue** with the caption ready to paste on LinkedIn.

Publish manually from the issue until you configure the token.

### Automatic publishing (one-time setup, ~15 min)

1. Create an app at https://www.linkedin.com/developers/apps (requires linking a
   Company Page — a simple one created for this works fine).
2. On the **Products** tab, add **Share on LinkedIn** and **Sign In with LinkedIn
   using OpenID Connect** (instant approval).
3. On **Auth → OAuth 2.0 tools → Token Generator**, generate a token with the
   scopes `openid`, `profile` and `w_member_social` (valid for 60 days).
4. On GitHub: **Settings → Secrets and variables → Actions → New repository
   secret** → name `LINKEDIN_ACCESS_TOKEN`, value = the token.
5. Test it: **Actions → publish-linkedin → Run workflow**. The post appears on
   your profile and the file moves to `content/published/`.

> The token expires in ~60 days (LinkedIn offers no automatic refresh for standard
> apps). Renew it in the Token Generator and update the secret — the runbook
> (`docs/operations/runbook.md`) covers this and other common issues.

### Approving each post

Every run pauses before publishing: the `prepare` job shows a preview (GIF +
caption) in its job summary, then GitHub notifies you by e-mail
and mobile push ("Review required"). Open the run → **Review deployments** →
**Approve and deploy** to publish, or **Reject** to skip (the post stays queued).
Details and tips in `docs/operations/runbook.md` §5.

### Replenishing the content queue

When the **"Content queue running low"** issue appears, open Claude Code in this
repository and run `/linkedin-gifs <subject> [count]` (e.g. `/linkedin-gifs kafka 3`).
The skill writes the posts, renders each GIF, opens a review page (GIF next to its
caption), asks for your approval and only then commits and pushes.
It follows the rules in `scripts/PROMPT_GERACAO.md` and uses your subscription (no
API cost).

### Creating a post (local)

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium     # one-time, captures the frames
brew install ffmpeg                                 # one-time, encodes the GIF

# 1. write content/queue/NNN-slug.md (or generate it: scripts/PROMPT_GERACAO.md)
PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.animate NNN --preview   # live HTML in out/preview/
PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.animate                 # out/NNN.gif for every post missing one
PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.run --list              # order + gif:rendered / gif:MISSING
git add content/queue out && git commit -m "content: +1 animated post" && git push
```

`animate NNN --force` re-renders after an edit; `--mp4` also writes a video to
`out/preview/` (not published). Tests: `.venv/bin/python -m pytest tests/ -q`.

## Post format

`content/queue/NNN-slug.md`:

```markdown
---
id: "010"
topic: topic name
title: "Internal title"
animation:
  title: "Concept"
  subtitle: "one line of context"
  nodes:
    - {id: client, label: Client, at: [0, 0], color: blue}
    - {id: api, label: API, sub: "service", at: [1, 0], color: green}
  edges:
    - {from: client, to: api, label: request}
  steps:
    - caption: "What happens in this step"
      packets:
        - {path: [client, api], kind: ok, count: 3}
alt_text: "Animated diagram of ..."
status: ready
---
LinkedIn caption (300-500 chars: number-led hook, what the GIF shows, one takeaway, one question, 2-3 hashtags).
```

Full field reference and the hard rules (node count, 250-frame limit, caption
structure): `scripts/PROMPT_GERACAO.md`.

Schedule: the cron in `.github/workflows/publish.yml` fires the evening before
(GitHub delivers it hours late), and the publish job only posts between 06:00 and
12:00 São Paulo time — approve inside that window. Details: runbook §4.

## Documentation

Design-doc driven project (`/dd` greenfield flow): PRD, HLD, FDD, ADRs, API
research and runbook live in [`docs/`](docs/) — index in [`CLAUDE.md`](CLAUDE.md).
