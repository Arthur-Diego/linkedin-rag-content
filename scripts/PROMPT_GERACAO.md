# Official prompt — replenish the content queue

When the "Content queue running low" issue shows up (or whenever you want fresh
topics), open Claude Code at the root of this repository and paste the prompt below.
Cost: covered by your Claude subscription — no paid API involved.

---

Read `content/published/` and `content/queue/` to see the topics already covered and
the post format. Then create N new posts about RAG in `content/queue/`, continuing
the id numbering.

Rules:

1. Format identical to the existing posts: YAML frontmatter with `id` (3-digit
   string), `topic`, `title`, `image.headline`, `image.bullets` (3-4 short bullets),
   optional `image.prompt` (visual prompt for AI background generation — abstract
   illustration description, always textless), `alt_text`, and `status: ready`;
   body = the LinkedIn caption.
2. Caption in ENGLISH (target audience: international recruiters and engineers):
   strong hook in the first line, 3-5 short paragraphs or a numbered list,
   production-grade practical insight (not tutorial theory), an engagement question
   at the end, and 5 hashtags.
3. Topics: deepen or complement what's already published without repeating angles.
   Backlog ideas: advanced chunking, embedding fine-tuning, multimodal RAG, security
   and permissions in RAG, RAG vs long-context, contextual retrieval, continuous
   evaluation, production architectures, real failure stories.
4. File names: `NNN-slug.md`.
5. When done, run `python -m pytest tests/ -q`, validate with a `--dry-run`, then
   commit with the message `content: +N posts in the queue`.
