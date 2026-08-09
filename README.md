# linkedin-rag-content

An automated pipeline that publishes technical posts about RAG to LinkedIn,
3x per week, with zero manual effort.

```
GitHub Actions (cron Mon/Wed/Fri)
   └─► next post from the queue (content/queue/*.md)
         └─► didactic diagram card: HTML template + Mermaid flowchart
             (Inter type, light theme) → PNG via headless Chromium
               └─► ⏸ approval gate: GitHub notifies you (e-mail/push),
                   you review the image + caption and click Approve
                     └─► LinkedIn Posts API (with token)
                         or GitHub issue with the finished post (without token)
```

- **100% free**: Actions on a public repo + LinkedIn's free official API + local,
  deterministic card rendering (no paid image APIs).
- **Didactic by design**: every card is a system-design style diagram (ByteByteGo
  school) with 3 numbered takeaways — the format with the highest save rate on
  LinkedIn; caption rules follow the research in
  `docs/research/linkedin-tech-content-playbook.md`.
- **State lives in git**: queue in `content/queue/`, history in
  `content/published/`, images in `out/`. No database, no server.
- **Content**: pre-generated with Claude Code and reviewable before going live;
  the queue ships with 9 posts (~3 weeks).

## How to use

### Works today (draft mode, no setup)

The workflow runs Mon/Wed/Fri 08:30 BRT (or manually via **Actions →
publish-linkedin → Run workflow**). Without a token it:

1. Renders the post image and commits it to `out/`.
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

Every run pauses before publishing: the `prepare` job renders the card and shows a
preview (image + caption) in its job summary, then GitHub notifies you by e-mail
and mobile push ("Review required"). Open the run → **Review deployments** →
**Approve and deploy** to publish, or **Reject** to skip (the post stays queued).
Details and tips in `docs/operations/runbook.md` §5.

### Replenishing the content queue

When the **"Content queue running low"** issue appears, open Claude Code in this
repository and follow `scripts/PROMPT_GERACAO.md` — it generates new posts in the
right format using your subscription (no API cost).

### Running locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium                      # one-time, for the card renderer
PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.run --dry-run   # renders out/ without publishing
.venv/bin/python -m pytest tests/ -q                                 # tests
```

## Post format

`content/queue/NNN-slug.md`:

```markdown
---
id: "010"
topic: topic name
title: "Internal title"
image:
  headline: "Card headline"
  diagram: |
    flowchart LR
        A["Start"]:::accent --> B["End"]:::good
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "takeaway 1"
    - "takeaway 2"
    - "takeaway 3"
alt_text: "image description"
status: ready
---
LinkedIn caption (700-1,000 chars, number-led hook, reflection, one question, 2-3 hashtags).
```

Schedule/frequency: edit the cron in `.github/workflows/publish.yml` (UTC).

## Documentation

Design-doc driven project (`/dd` greenfield flow): PRD, HLD, FDD, ADRs, API
research and runbook live in [`docs/`](docs/) — index in [`CLAUDE.md`](CLAUDE.md).
