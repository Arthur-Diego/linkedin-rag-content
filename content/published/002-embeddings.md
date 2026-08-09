---
id: '002'
topic: embeddings
title: 'Embeddings: benchmarks are not your domain'
image:
  headline: Pick embeddings with your data, not leaderboards
  diagram: "flowchart LR\n    Q[\"Which embedding<br/>model?\"]:::accent --> BENCH[\"\
    MTEB<br/>leaderboard\"]\n    BENCH --> TRAP[\"Generic corpus<br/>&ne; your domain\"\
    ]:::bad\n    Q --> TEST[\"Test 2-3 candidates<br/>on YOUR data\"]\n    TEST -->\
    \ METRIC[\"50 real questions<br/>recall@k &middot; latency &middot; cost\"]:::good\n\
    \    METRIC --> WIN[\"Pick winner<br/>reindex everything\"]:::accent\n    classDef\
    \ bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n\
    \    classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - A benchmark winner can lose badly on legal jargon, code or non-English text
  - 3072 dimensions cost ~4x more than 768 in storage and latency — check the recall
    gain first
  - 'Switched models? Reindex everything: mixed vectors are a silent bug'
alt_text: Diagram showing how to select an embedding model by testing on your own
  data instead of trusting benchmarks
status: published
published_at: '2026-08-09T22:04:28+00:00'
linkedin_post_id: urn:li:share:7492340043345387520
---
One afternoon of testing beats six months of mediocre retrieval.

That's the real cost equation of choosing an embedding model — and almost everyone skips the test and trusts the MTEB leaderboard instead.

The trap: benchmarks measure generic corpora. Your domain has legal jargon, source code, or non-English text — and models that win on averages routinely lose there.

Picture the two roads: one stops at the leaderboard and inherits its blind spots; the other runs 2-3 candidates against your own 50 questions and lets recall@k, latency and cost pick the winner.

The process that works:

1. Pick 2-3 candidates.
2. Run them on YOUR documents with 50 real questions.
3. Compare recall@k, latency and cost — 3072-dimension vectors cost roughly 4x more than 768 to store and search.
4. Crown the winner and reindex EVERYTHING. Mixed vectors from different models in one index fail silently.

The bigger lesson: in RAG, evidence from your own data always beats reputation. A leaderboard is where the shortlist starts, never where the decision ends.

Which embedding model are you running today? 👇

#RAG #Embeddings #AIEngineering
