---
id: "004"
topic: reranking
title: "Reranking: the second opinion your retrieval needs"
image:
  headline: "Reranking: precision after recall"
  bullets:
    - "Retrieval optimizes recall, rerankers optimize precision"
    - "Cross-encoders read query + document together"
    - "Fetch top-50, rerank, send top-5"
    - "Less junk context = fewer hallucinations"
  prompt: "Abstract illustration of glowing cards being sorted and reordered by priority, the top ones shining brighter, dark navy background with cyan accents, minimal futuristic style"
alt_text: "Technical card about reranking in RAG pipelines"
status: ready
---
Your retrieval returns 20 documents. How many are actually relevant? If the answer is "about 5", you don't have a search problem — you have a ranking problem.

Vector search uses bi-encoders: query and document become vectors separately, and comparison is just a similarity computation. Fast enough to scan millions of documents, but shallow — the two texts never actually "read" each other.

A reranker is a cross-encoder: it takes query and document TOGETHER and produces a relevance score. Far too expensive to run on the whole corpus, but perfect for refining a short list.

The pattern that works:

1. Hybrid retrieval brings the top-50 candidates, optimizing recall.
2. The reranker reorders those 50, optimizing precision.
3. Only the top-5 make it into the LLM context.

The most underrated side effect: less junk in the context means fewer hallucinations. The model doesn't have to guess which of 20 passages matters — the 5 that arrived are the right ones. And a smaller context is also cheaper and faster.

Getting started: the open-source BGE rerankers run fine even on CPU for lists of 50 documents. Near-zero infra cost, visible quality gains on day one.

Do you rerank, or does raw retrieval go straight to your model? 👇

#RAG #Reranking #LLM #AI #NLP
