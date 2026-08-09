---
id: "004"
topic: reranking
title: "Reranking: precision after recall"
image:
  headline: "Retrieve wide, rerank hard, send only the best"
  diagram: |
    flowchart LR
        DOCS[("1M docs")]:::accent --> RET["Hybrid retrieval<br/>top-50 &middot; recall"]
        RET --> RAW["Send raw top-20<br/>to the LLM"]
        RAW --> NOISE["Noisy context<br/>hallucinations"]:::bad
        RET --> RR["Cross-encoder<br/>rerank &middot; precision"]:::good
        RR --> TOP5["Top-5 only"]:::good
        TOP5 --> LLM["LLM answer<br/>grounded + cheaper"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Bi-encoders compare vectors; cross-encoders read query + document together"
    - "Rerank 50 candidates, keep 5 — precision where it matters"
    - "Open-source BGE rerankers run on CPU for lists this small"
alt_text: "Diagram of a RAG pipeline where hybrid retrieval fetches top-50 candidates and a cross-encoder reranker keeps only the top-5"
status: ready
---
50 in, 5 out. That ratio fixes more RAG systems than any model upgrade.

Vector search uses bi-encoders: query and document become vectors separately, then get compared. Fast enough for millions of documents — but the two texts never actually read each other.

A reranker is a cross-encoder: it reads query and document TOGETHER and scores real relevance. Too slow for a whole corpus, perfect for a short list.

Follow the two branches in the diagram: dumping the raw top-20 into the model (red) drags noise and hallucinations with it; inserting the reranker (green) means only 5 precision-picked chunks reach the LLM.

The production pattern:

1. Hybrid retrieval brings top-50 → optimizes recall.
2. Cross-encoder reranks them → optimizes precision.
3. Only top-5 reach the LLM context.

The side effect nobody prices in: less junk context means fewer hallucinations — the model stops guessing which of 20 passages matters. And a 5-chunk context is also cheaper and faster than a 20-chunk one.

The bigger lesson: retrieval and ranking are different jobs. Doing both with one similarity score is asking one metric to carry your whole pipeline.

Open-source BGE rerankers run fine on CPU for 50 documents. Do you rerank today? 👇

#RAG #Reranking #AIEngineering
