---
id: "008"
topic: semantic cache
title: "Semantic caching: the most ignored cost optimization in RAG"
image:
  headline: "Semantic cache: pay once, answer a thousand times"
  bullets:
    - "Repeated questions dominate real traffic"
    - "Cache by similarity, not string equality"
    - "Wrong threshold = wrong answer served confidently"
    - "Invalidate when the source document changes"
  prompt: "Abstract illustration of caching and memory, layered translucent panels with glowing data streams being reused, dark navy background with cyan highlights, minimal futuristic style"
alt_text: "Technical card about semantic caching in LLM applications"
status: ready
---
Look at your RAG's production logs. I'd bet 30% of the questions are variations of the same 50 doubts.

"How do I get a copy of my invoice?", "invoice copy", "resend my invoice" — three different strings, one question, three full pipeline runs: retrieval, reranking, generation. Paying the LLM all three times.

Traditional caching doesn't help: the key never matches, because the string never repeats exactly. A semantic cache compares by embedding — if a new question is similar enough to one already answered, return the stored answer. Seconds become milliseconds; token cost becomes zero.

The three decisions that separate a useful cache from a wrong-answer factory:

1. A conservative threshold: start high, around 0.95. "Cancel plan A" and "cancel plan B" are neighbors in vector space — with different answers. A cache false positive is a wrong answer delivered with full confidence.

2. Source-based invalidation: store, next to each answer, the documents that produced it. Document updated → derived entries expire. A RAG cache without invalidation becomes a museum of outdated answers.

3. Per-user or per-tenant scope: answers that depend on permissions must never leak through a global cache.

It's an afternoon of implementation — you're already computing the embedding anyway — and your LLM bill will thank you at the end of the month.

How many times a day does your pipeline answer the same question? 👇

#RAG #LLM #AI #FinOps #AIEngineering
