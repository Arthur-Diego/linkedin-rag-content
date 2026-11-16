---
name: linkedin-gifs
description: Creates N animated system-design GIF posts for the LinkedIn queue from a subject. Use when the user gives a topic and asks for posts, GIFs, animated diagrams or content for LinkedIn (e.g. "/linkedin-gifs kafka 3", "create 4 gifs about circuit breakers"), or wants to replenish the content queue.
argument-hint: "<subject> [count]"
---

# linkedin-gifs — subject in, N queued animated posts out

Input: a subject and a count (default 3). Output: N posts in `content/queue/`, each
with its rendered `out/NNN.gif`, shown to the user, approved by them, then committed
and pushed so the scheduled workflow can publish.

Everything published is in **English** (posts, captions, labels), whatever language
the user writes in. Talk to the user in their language.

`scripts/PROMPT_GERACAO.md` is the source of truth for the post format, the
`animation:` field reference and the hard rules (node count, caption structure,
250-frame limit). Read it before writing; do not restate or relax it here.

## Steps

1. **Survey.** Read `scripts/PROMPT_GERACAO.md`, list `content/published/` and
   `content/queue/` (titles are enough) to avoid repeating a covered mechanism and
   to find the next free id. Read one queued animated post as a format example.
2. **Pick N angles.** Split the subject into N distinct mechanisms, one per post
   (e.g. "Kafka" → consumer groups rebalancing · the outbox pattern · dead-letter
   queues). Each must be showable as packets moving between at most 5 boxes. If the
   subject only supports fewer good angles than N, say so instead of padding.
   Only state technical facts you are sure of; numbers in a post must be defensible.
3. **Write the posts** as `content/queue/NNN-slug.md` following PROMPT_GERACAO.
   Use the generic engine (omit `animation.scene`). Write a custom scene in
   `assets/scenes/` only when the mechanism needs a real simulation and the user
   asked for that level of polish.
4. **Render.** `PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.animate --mp4`
   renders every post still missing a GIF. Fix any validation error it reports.
5. **Look at every animation.** A render that succeeded can still be wrong. For each
   new id, extract one frame per step and read the images:
   `ffmpeg -y -loglevel error -ss <seconds> -i out/preview/NNN.mp4 -frames:v 1 <scratch>/NNN-<n>.png`
   Check: no clipped or overlapping labels, packets take the path the caption
   describes, colors match the outcome (green ok, red failure), the tally ends on
   the numbers the caption claims, the first frame makes sense as a thumbnail.
   Edit the post and re-render with `animate NNN --force --mp4` until it is right.
6. **Verify.** `.venv/bin/python -m pytest tests/ -q`, then
   `PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.run --list` must show
   `gif:rendered` for every new post. Check each caption is 300-500 characters
   and only talks about what its GIF shows.
7. **Show everything (always, never skip).** Build the review page and open it:
   `PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.animate --review <new ids>`
   then `open -a "Google Chrome" out/preview/review.html` (plain `open` if Chrome is
   missing). The page plays each GIF next to the exact caption that will be posted.
   In the chat, also list per post: id, title, the angle in one line, and the full
   caption in a code block, so the user can validate the text without the browser.
8. **Ask for approval with a button.** Call AskUserQuestion (header "Approval") with:
   - "Approve and commit" — everything goes to GitHub, ready for publication;
   - "Request changes" — the user says what to change.
   The dialog is the approval button. If it is dismissed, unanswered or unavailable,
   ask the same thing in plain text ("Posso aprovar e commitar os N posts, ou quer
   ajustar algo?") and wait. Never commit on silence, and never treat a comment about
   one post as approval of all.
9. **On "Request changes"**: edit the posts, re-render what changed
   (`animate NNN --force --mp4`), re-check the frames, and go back to step 7.
10. **On approval, commit and push** so the scheduled workflow can publish:
    `git add content/queue out/NNN.gif out/NNN-caption.txt` (the new ids only), commit
    `content: +N animated posts in the queue`, and push to `main` (content goes
    straight to `main`, see `docs/gitflow.md`). If the working tree is on another
    branch or carries unrelated changes, say so and ask before pushing. Confirm with
    `git status` and `git log origin/main -1` that the push landed, then tell the
    user which post is next and that it will wait for their approval in GitHub, in
    the morning window, before going live. Never trigger the workflow from here.

## Notes

- Publication order is by id. To publish a new post earlier, ask the user before
  renumbering anything already in the queue.
- Posts with an `image:` block are the parked static-card format; leave them alone.
- If `animate` reports missing tooling: `brew install ffmpeg`,
  `.venv/bin/python -m playwright install chromium`.
