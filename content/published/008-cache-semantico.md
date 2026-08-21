---
id: 008
topic: semantic cache
title: 'Semantic caching: the most ignored cost lever in RAG'
image:
  headline: 'Same question, a thousand phrasings: cache by meaning'
  diagram: "flowchart LR\n    Q[\"New question\"]:::accent --> SIM{\"Similar to a\
    \ cached<br/>question? &ge; 0.95\"}\n    SIM -- \"yes\" --> HIT[\"Cached answer<br/>~ms\
    \ &middot; $0\"]:::good\n    SIM -- \"no\" --> PIPE[\"Full pipeline<br/>retrieve\
    \ + generate\"]\n    PIPE --> STORE[\"Store answer<br/>+ source doc ids\"]:::accent\n\
    \    STORE -.-> INV[\"Doc updated &rarr;<br/>expire entries\"]:::bad\n    classDef\
    \ bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n\
    \    classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - Cache by embedding similarity, not string equality — phrasings never repeat exactly
  - 'Threshold ~0.95: ''cancel plan A'' and ''cancel plan B'' are neighbors with different
    answers'
  - Store source doc ids with each answer; invalidate when the source changes
alt_text: Diagram of a semantic cache checking embedding similarity before running
  the full RAG pipeline
status: published
published_at: '2026-08-21T12:32:24+00:00'
linkedin_post_id: urn:li:share:7496544738217680897
---
30% of production RAG traffic is the same 50 questions, rephrased.

"How do I get an invoice copy?", "invoice copy", "resend my invoice" — three strings, one question, three full pipeline runs. Paying the LLM every time.

Traditional caching can't help: the key never matches, because the phrasing never repeats. A semantic cache compares by embedding, and the whole system is one decision: similarity ≥ 0.95 with an already-answered question takes the shortcut (cached answer, ~ms, $0); anything below runs the full pipeline and stores the new answer with its source doc ids for invalidation.

Three decisions separate a useful cache from a wrong-answer factory:

1. Conservative threshold (~0.95). "Cancel plan A" and "cancel plan B" are vector-space neighbors with different answers — and a cache false positive is a wrong answer served with confidence.

2. Source-based invalidation. Store the doc ids behind each answer; document updated → entries expire.

3. Per-tenant scope. Permission-dependent answers must never leak through a global cache.

The bigger lesson: you already compute the embedding for every question. The cheapest optimization is reusing work you've already paid for.

How often does your pipeline answer the same thing twice? 👇

#RAG #FinOps #AIEngineering
