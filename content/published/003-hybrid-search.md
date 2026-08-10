---
id: '003'
topic: hybrid search
title: 'Hybrid search: why vectors alone aren''t enough'
image:
  headline: Vectors find meaning. BM25 finds exact terms.
  diagram: "flowchart LR\n    Q[\"Query\"]:::accent --> VEC[\"Vector search<br/>semantics\"\
    ]\n    Q --> BM[\"BM25<br/>exact terms\"]\n    VEC -.-> VMISS[\"Misses codes<br/>ORA-01555\"\
    ]:::bad\n    BM -.-> BMISS[\"Misses synonyms<br/>cancel &ne; terminate\"]:::bad\n\
    \    VEC --> RRF[\"Reciprocal Rank<br/>Fusion\"]:::good\n    BM --> RRF\n    RRF\
    \ --> TOP[\"Best of both<br/>in the top-k\"]:::accent\n    classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n\
    \    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n    classDef accent\
    \ fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - Error codes, contract numbers and acronyms are invisible to pure vector search
  - RRF fuses both rankings with zero tuning — no weights, no score normalization
  - Qdrant, Weaviate, OpenSearch and pgvector ship hybrid search natively
alt_text: Diagram of hybrid search fusing vector search and BM25 results with Reciprocal
  Rank Fusion
status: published
published_at: '2026-08-10T12:30:40+00:00'
linkedin_post_id: urn:li:share:7492558031621341184
---
2 searches. 1 fusion formula. That's the cheapest retrieval upgrade in RAG.

Vector search finds what the user meant. Lexical search finds what the user typed. Each engine alone carries a blind spot — vectors miss exact codes, BM25 misses synonyms — and RRF fusion erases both weaknesses in one move.

Production traffic proves it daily:

A user asks about error "ORA-01555" — vector search returns semantically similar documents, but not THE document. An exact code isn't semantics. BM25 nails it.

Another asks "how to cancel my subscription" — the document says "plan termination". Zero term overlap, BM25 is blind. Vectors get it instantly.

The fix: run both, then merge with Reciprocal Rank Fusion. Each document scores by its position in each ranking; sum the points. No weights to tune, no score normalization — and it consistently beats either search alone.

The bigger lesson: most RAG upgrades are trade-offs. Hybrid search is one of the few free lunches — your vector store almost certainly already supports it as configuration.

Is your retrieval hybrid yet? 👇

#RAG #InformationRetrieval #AIEngineering
