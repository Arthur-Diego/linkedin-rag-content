---
id: "001"
topic: chunking
title: "Chunking: where most RAG pipelines die"
image:
  headline: "Chunking decides your RAG ceiling"
  diagram: |
    flowchart LR
        DOC["Document"]:::accent --> FIX["Fixed-size cut<br/>500 tokens"]
        DOC --> STR["Structure-aware cut<br/>headings + paragraphs"]
        FIX --> BAD["Broken tables<br/>orphan clauses"]:::bad
        STR --> GOOD["10-20% overlap<br/>+ metadata"]:::good
        BAD --> LOW["Low recall"]:::bad
        GOOD --> DB[("Vector DB")]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Split along structure, not token counts — headings and paragraphs are free boundaries"
    - "10-20% overlap keeps context alive at chunk borders"
    - "Measure recall on 50 known questions before switching strategies"
alt_text: "Diagram comparing fixed-size chunking with structure-aware chunking in a RAG pipeline"
status: ready
---
500 tokens. That's where most RAG pipelines quietly break.

Fixed-size chunking is everyone's baseline — and the reason retrieval returns half a table, or a clause without its heading. The chunk arrives, but the meaning doesn't.

What actually works in production:

1. Split along structure — headings, paragraphs, functions. Markdown gives you these boundaries for free.

2. Add 10-20% overlap, so context at the borders survives the cut.

3. Attach metadata to every chunk — document title, section, date. Richer embeddings, and filtering becomes possible.

The bigger lesson: chunking looks like a preprocessing detail, but it sets the ceiling for your entire pipeline. No reranker, no bigger model can fix a chunk that arrived broken.

So before switching strategies: build 50 questions with known answers and measure recall before and after. Chunking is decided with numbers, not intuition.

What's your default chunk size today? 👇

#RAG #AIEngineering #LLM
