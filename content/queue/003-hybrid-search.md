---
id: "003"
topic: hybrid search
title: "Hybrid search: why vectors alone aren't enough"
image:
  headline: "Hybrid search: vectors + BM25"
  bullets:
    - "Vectors miss exact codes, acronyms and names"
    - "BM25 misses synonyms and paraphrases"
    - "RRF combines both with zero tuning"
    - "The cheapest retrieval upgrade you can ship"
  prompt: "Two abstract streams of light, one geometric and structured, one organic and flowing, merging into a single beam, dark navy background with cyan accents, minimal futuristic style"
alt_text: "Technical card about hybrid search combining vectors and BM25"
status: ready
---
Vector search finds what you meant. Lexical search finds what you typed. Your RAG needs both.

The classic case: a user asks about error "ORA-01555" or contract "CT-2024-0087". Vector search returns semantically similar documents — but not THE document, because an exact code isn't semantics. BM25 nails it in first position.

The reverse case exists too: the user asks "how to cancel my subscription" and the document says "plan termination". BM25 sees zero term overlap. Vectors get it instantly.

The fix is running both searches and fusing the results. The simplest, surprisingly effective method: Reciprocal Rank Fusion. The formula fits in a tweet — each document scores points based on its rank in each list, then you sum. No weights to calibrate, no score normalization across different systems.

Bonus: virtually every modern vector store already ships hybrid search natively — Qdrant, Weaviate, OpenSearch, pgvector with Postgres tsvector. It's configuration, not a project.

If you only run vector search today, hybrid search is probably the biggest retrieval gain per hour of work you can get.

Is your RAG hybrid yet? 👇

#RAG #HybridSearch #LLM #AI #InformationRetrieval
