---
id: '001'
topic: chunking
title: 'Chunking: where most RAG pipelines die'
image:
  headline: Chunking decides your RAG ceiling
  diagram: "flowchart LR\n    DOC[\"Document\"]:::accent --> FIX[\"Fixed-size cut<br/>500\
    \ tokens\"]\n    DOC --> STR[\"Structure-aware cut<br/>headings + paragraphs\"\
    ]\n    FIX --> BAD[\"Broken tables<br/>orphan clauses\"]:::bad\n    STR --> GOOD[\"\
    10-20% overlap<br/>+ metadata\"]:::good\n    BAD --> LOW[\"Low recall\"]:::bad\n\
    \    GOOD --> DB[(\"Vector DB\")]:::accent\n    classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n\
    \    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n    classDef accent\
    \ fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - Split along structure, not token counts — headings and paragraphs are free boundaries
  - 10-20% overlap keeps context alive at chunk borders
  - Measure recall on 50 known questions before switching strategies
alt_text: Diagram comparing fixed-size chunking with structure-aware chunking in a
  RAG pipeline
status: published
published_at: '2026-08-09T21:47:30+00:00'
linkedin_post_id: urn:li:share:7492335775976566784
---
500 tokens. That's where most RAG pipelines quietly break.

Fixed-size chunking is everyone's baseline — and the reason retrieval returns half a table, or a clause without its heading. The chunk arrives, but the meaning doesn't.

The diagram shows the fork. Red path: a fixed 500-token cut slices through tables and clauses, and recall pays the price. Green path: cuts that follow the document's own structure, plus overlap and metadata, deliver retrieval-ready chunks to the vector DB.

What actually works in production:

1. Split along structure — headings, paragraphs, functions. Markdown gives you these boundaries for free.

2. Add 10-20% overlap, so context at the borders survives the cut.

3. Attach metadata to every chunk — document title, section, date. Richer embeddings, and filtering becomes possible.

The bigger lesson: chunking looks like a preprocessing detail, but it sets the ceiling for your entire pipeline. No reranker, no bigger model can fix a chunk that arrived broken.

So before switching strategies: build 50 questions with known answers and measure recall before and after. Chunking is decided with numbers, not intuition.

What's your default chunk size today? 👇

#RAG #AIEngineering #LLM
