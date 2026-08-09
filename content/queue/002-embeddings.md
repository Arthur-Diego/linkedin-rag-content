---
id: "002"
topic: embeddings
title: "Embeddings: the model matters less than you think"
image:
  headline: "Embeddings in RAG: 4 decisions that matter"
  bullets:
    - "Public benchmarks are not your domain"
    - "Bigger dimensions = bigger cost, not always gains"
    - "Normalize and fix your distance metric"
    - "Changed models? Reindex everything"
  prompt: "Abstract 3D vector space with glowing points clustering in constellations, depth and perspective, dark navy background with cyan and blue gradients, minimal futuristic style"
alt_text: "Technical card about choosing embedding models for RAG"
status: ready
---
Everyone asks which embedding model is best. Almost nobody asks the question that matters: how does it behave on YOUR domain?

The MTEB leaderboard is a great starting point — and a terrible finish line. A model that wins on generic benchmarks can stumble on legal jargon, source code, or non-English text. The only trustworthy answer comes from testing with your own documents and your own questions.

What I evaluate before choosing:

1. Language: is your corpus multilingual? Model quality varies wildly across languages.

2. Vector dimension: 3072 dimensions cost more in storage and latency than 768. If the recall gain is 1%, it doesn't pay.

3. The embedding context window: chunks longer than the limit get silently truncated — and you'll never get an error about it.

4. Consistency: switched models? Reindex EVERYTHING. Vectors from different models in the same index is a silent, guaranteed bug.

Practical rule: pick 2-3 candidates, run them on your data with 50 real questions, measure recall@k. One afternoon of work that saves months of mediocre retrieval.

Have you actually measured your retrieval recall, or are you trusting the benchmark? 👇

#RAG #Embeddings #LLM #AI #VectorSearch
