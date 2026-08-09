---
id: "005"
topic: query rewriting
title: "Query rewriting: the problem isn't your index, it's the question"
image:
  headline: "Rewrite the question before you search"
  bullets:
    - "Users ask badly, and that's fine"
    - "Multi-query: 3 variations of the same question"
    - "HyDE: search with a hypothetical answer"
    - "Decompose compound questions"
  prompt: "Abstract illustration of a single beam of light refracting through a prism into multiple parallel beams, dark navy background with cyan and blue accents, minimal futuristic style"
alt_text: "Technical card about query rewriting in RAG"
status: ready
---
We spend months optimizing indexes, chunking and embeddings — and forget that the user's query is usually the worst part of the pipeline.

"the report thing doesn't work" — that's what reaches your retrieval. No embedding model can save a question like that. The good news: you have an LLM at hand, and rewriting text is what it does best.

Three techniques I use in production:

1. Multi-query: the LLM generates 3 variations of the question with different vocabulary. Run the searches in parallel and fuse results with RRF. It bridges the gap between the user's jargon and the documents' jargon.

2. HyDE: ask the model for a hypothetical answer to the question and use THAT text as the query. An imaginary answer looks far more like the real document than the original question does.

3. Decomposition: "compare plan X coverage with plan Y" becomes two searches — one per plan — and the model composes the final answer. Compound questions are almost never answered by a single chunk.

The cost? One extra call to a small, cheap model before the search. Latency goes up a little; the rate of correct answers goes up a lot more.

Before replacing your vector store: does your query deserve a second chance? 👇

#RAG #LLM #AI #NLP #AIEngineering
