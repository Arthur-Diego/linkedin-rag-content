# Official prompt — professional post generation

When the "Content queue running low" issue shows up (or whenever you want fresh
topics), open Claude Code at the root of this repository and run
`/linkedin-gifs <subject> [count]` — the skill applies the rules below. (Pasting the
prompt below by hand works too.) Cost: covered by your Claude subscription — no paid
API involved.

The rules encode the research in `docs/research/linkedin-tech-content-playbook.md`
(1.2M-post hook analysis, van der Blom 2025 algorithm report, ByteByteGo-style
visual patterns). Don't relax them.

> The pipeline runs in **gif mode** (ADR-010): every new post is an animated
> system-design diagram. The static-card format (`image:` block) is switched off;
> its rules are in the git history of this file.

---

Read `content/published/` and `content/queue/` to see the topics already covered and
the exact post format. Then create N new animated posts in `content/queue/`,
continuing the id numbering. Audience: international engineers and recruiters.
Everything in English.

## Frontmatter

`id` (3-digit string), `topic`, `title`, `animation` (below), `alt_text` (describe
what moves, start with "Animated diagram of"), `status: ready`.

## The animation (`animation:`) — the core of the post

```yaml
animation:
  title: "Cache-Aside"                      # 1-3 words, the concept
  subtitle: "Read path · the app owns the cache"
  nodes:                                    # at: [column, row]
    - {id: client, label: Client, sub: "GET /product/42", at: [0, 0], color: blue}
    - {id: app, label: Service, sub: "cache-aside", at: [1, 0], color: violet}
    - {id: cache, label: Redis, sub: "TTL 5 min", at: [2, 0], color: yellow}
    - {id: db, label: PostgreSQL, sub: "source of truth", at: [1, 1], color: green}
  edges:
    - {from: client, to: app, label: read}
    - {from: app, to: cache, label: "1. get"}
  tally: {ok: "cache hits", warn: "database reads"}
  steps:
    - caption: "First read: the cache has nothing yet"
      packets:
        - {path: [client, app, cache, app], kind: bad, turns: 2}
    - caption: "Next reads never touch the database"
      packets:
        - {path: [client, app, cache, app, client], kind: ok, turns: 2, count: 4, every: 0.5}
```

Reference:

- `nodes`: `id`, `label` (1-2 words), optional `sub` (≤ 16 chars), `at`, `color`
  (`blue` `violet` `green` `red` `yellow` `orange` `slate`). Optional `meter: N` draws
  N dots inside the node (a bucket, a pool, a queue); steps move it with
  `meters: {node_id: value}`.
- `edges`: `from`, `to`, optional `label` (≤ 9 chars: it must fit in the gap between
  two boxes) and `color`. Declare both
  directions when traffic returns; the scene draws two lanes.
- `steps`: `caption` (mandatory) plus optional `packets`, `meters`, `seconds`
  (default: as long as its packets need).
- `packets`: `path` (node ids, ≥ 2), `kind` (`ok` green · `bad` red · `warn` yellow ·
  `info` blue), `count` and `every` (seconds between packets), `at` (delay inside the
  step), `turns` (hop where the packet takes its kind color; before it, blue).
- `tally`: label per packet kind (≤ 18 chars, at most 2 kinds); counts packets that
  finished their path.
- `scene`: omit for the generic engine. Set it to a file in `assets/scenes/` only
  when the mechanism needs a real simulation (see `token-bucket.html`).

Hard rules:

1. ONE mechanism per animation. Rotate archetypes: request lifecycle · failure path
   vs happy path · before/after of one change.
2. At most 5 nodes, grid 3 columns × 2 rows (4 × 4 is the hard limit). Real tech
   names ("Redis", "Kafka") over generic boxes.
3. 4-5 steps, total under 16 seconds (LinkedIn rejects GIFs above 250 frames = 16.6 s
   at 15 fps; the renderer enforces it). Aim for 10-14 s.
4. Step captions: ≤ 44 characters, present tense, no trailing period. Read in order
   they must tell the whole story without the post text.
5. The first frame is the thumbnail: title, subtitle and the full diagram must make
   sense with nothing moving.
6. End where it started (meters back to their initial value) so the loop is seamless.
7. No emojis inside the animation.

## The caption (post body) — 300-500 characters

Short, simple and objective (owner decision, 2026-11-16): the GIF teaches, the
caption only points at it. Four short blocks separated by blank lines, in order:

1. **Hook (first line, ≤ 10 words)**: a concrete number or a contrarian claim.
   NEVER a question (questions as openers measurably underperform: −34%).
   Patterns: "4 tokens. That is all that stands between your API and a flood." /
   "One miss. Then every read skips the database."
2. **What the animation shows**: 1-2 sentences narrating what moves
   ("Watch the bucket: ..."), so the reader looks back at the GIF.
3. **One takeaway**: a single practical point, 1-2 sentences, tied to what was just
   shown. No numbered lists, no "bigger lesson" paragraph, no second topic.
4. **CTA + hashtags**: ONE easy-to-answer question + 👇, then exactly 2-3 niche
   hashtags (e.g. #SystemDesign #Caching). Never more — 6+ measurably hurts reach.

Plain words, short sentences. No external links. If a sentence does not connect to
what the GIF shows, cut it.

## Validate before finishing

1. `python -m pytest tests/ -q`
2. Render every new post: `PYTHONPATH=src python -m linkedin_pipeline.animate`
   (iterate faster with `<id> --preview`, which writes a live HTML to `out/preview/`).
3. WATCH each GIF in `out/`: labels not clipped or overlapping, packets follow the
   story the captions tell, the tally ends on the numbers the post claims.
4. `PYTHONPATH=src python -m linkedin_pipeline.run --list` shows `gif:rendered` for
   every new post.
5. Commit the posts together with their GIFs: `content: +N animated posts in the queue`.
