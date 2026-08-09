# Official prompt — professional post generation

When the "Content queue running low" issue shows up (or whenever you want fresh
topics), open Claude Code at the root of this repository and paste the prompt below.
Cost: covered by your Claude subscription — no paid API involved.

The rules encode the research in `docs/research/linkedin-tech-content-playbook.md`
(1.2M-post hook analysis, van der Blom 2025 algorithm report, ByteByteGo-style
visual patterns). Don't relax them.

---

Read `content/published/` and `content/queue/` to see the topics already covered and
the exact post format. Then create N new posts about RAG in `content/queue/`,
continuing the id numbering. Audience: international engineers and recruiters.
Everything in English.

## Frontmatter (identical to existing posts)

`id` (3-digit string), `topic`, `title`, `image.headline`, `image.diagram`,
`image.bullets` (exactly 3), `alt_text`, `status: ready`. Optional `image.style`:
the default is **free** (creative card with the fixed dark/violet series
identity, one 3D panel per takeaway); set `spec` only to force a strict
diagram-drawn card. ALWAYS include `image.diagram` (it powers the free-tier
fallback renderer).

## The diagram (`image.diagram`) — the core of the post

Mermaid `flowchart LR`, rendered on a 4:5 card. Hard rules:

1. ONE concept per diagram. Rotate three archetypes across posts:
   step-by-step numbered flow · X-vs-Y comparison (wrong path vs right path) ·
   architecture boxes with labeled arrows.
2. Node labels: 1-4 words per line, max 2 lines (`<br/>`). Max ~8 nodes, max 5
   columns of depth — wider than that shrinks the render.
3. Use the standard classes and append their definitions verbatim:
   `:::accent` (entry/exit, blue) · `:::bad` (failure path, red) · `:::good`
   (solution path, green).
   ```
   classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
   classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
   classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
   ```
4. No emojis in the diagram. HTML entities for special chars (`&ne;` `&middot;`
   `&rarr;` `&ge;`). Real tech names ("BM25", "Vector DB") over generic boxes.
5. The diagram must teach the mechanism by itself — someone who reads only the
   image should learn the idea.

## The takeaways (`image.bullets`)

Exactly 3, one line each, concrete and specific (numbers > adjectives). They render
numbered 1-2-3 under the diagram.

## The caption (post body) — 700-1,000 characters

Structure, in order:

1. **Hook (first line, ≤ 10 words)**: a concrete number or a contrarian claim.
   NEVER a question (questions as openers measurably underperform: −34%).
   Patterns: "500 tokens. That's where most RAG pipelines break." /
   "50 in, 5 out. That ratio fixes more systems than any model upgrade."
2. **Image walkthrough (mandatory)**: 1-3 sentences that pull the reader into the
   visual before the list starts. Default (free style): narrate the CONCEPT
   ("Picture the two roads: ...") and never mention "the diagram". Only when a
   post explicitly sets `image.style: spec` may the caption narrate the diagram
   ("Red path: ... Green path: ...").
3. **Explanation (the meat)**: 1-2 line paragraphs, heavy white space, plain
   language. A numbered list of 3-4 production-grade steps with real numbers,
   thresholds and tool names. Teach the mechanism, not the marketing.
4. **Reflection ("The bigger lesson: ...")**: one short paragraph that zooms out —
   what this topic teaches about building systems in general. Mandatory.
5. **CTA**: ONE easy-to-answer question + 👇.
6. **Hashtags**: exactly 2-3, niche, at the end (e.g. #RAG #AIEngineering). Never
   more — 6+ measurably hurts reach.

No external links in the body. Optimize for saves: the post should read as
reference material someone bookmarks.

## Validate before finishing

1. `python -m pytest tests/ -q`
2. Render every new post and LOOK at each card (diagram fits, labels not clipped):
   dry-run renders only the next post, so render each new one explicitly via
   `html_renderer.render_card` or by temporarily reordering ids.
3. Commit: `content: +N posts in the queue`.
