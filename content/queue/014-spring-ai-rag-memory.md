---
id: "014"
topic: spring ai
title: "Spring AI RAG in production: advisors, memory and trust boundaries"
image:
  palette: spring
  headline: "Spring AI RAG: one advisor, grounded answers"
  diagram: |
    flowchart LR
        Q["User<br/>question"]:::accent --> QA["QuestionAnswer<br/>Advisor"]:::good
        QA --> VS["Vector store<br/>lookup"]:::good
        VS --> CTX["Context +<br/>chat memory"]:::good
        CTX --> ANS["Grounded<br/>answer"]:::accent
        Q --> RAW["Bare model<br/>call"]:::bad
        RAW --> HALL["Confident<br/>hallucination"]:::bad
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "QuestionAnswerAdvisor turns a chat model into RAG — retrieve, inject, answer"
    - "Three memory strategies: full messages, token-cheap summary, or vector recall"
    - "Retrieved docs are untrusted input — RAG context is a prompt-injection surface"
alt_text: "Diagram contrasting a bare model call that hallucinates against a Spring AI RAG path that retrieves from a vector store before answering"
status: ready
---
One advisor turns a chat model into a RAG pipeline.

In Spring AI, retrieval isn't a rewrite — it's a QuestionAnswerAdvisor you drop into the ChatClient. It queries your vector store, appends the matches to the prompt, and the model answers from your data instead of guessing.

Picture two answers to the same question: the bare model call confidently invents details; the RAG path retrieves your documents first and stays grounded.

Making it production-grade:

1. Pick a memory strategy on purpose: full messages for context, prompt summaries for token cost, vector recall for long sessions. The wrong one blows up spend or drops context.
2. Keep the VectorStore abstraction — swap PGVector for another store without touching retrieval code.
3. Treat retrieved chunks as untrusted input. A poisoned document is a prompt-injection vector; keep instructions separate from data.
4. Reindex when embeddings change — mixed vectors fail silently.

The bigger lesson: RAG quality is an architecture problem, not a model problem. The advisor is the easy part; memory, chunking and trust boundaries are where systems live or die.

Which memory strategy are you running today? 👇

📚 Part 2 of 3 — Spring AI for Microservices. Next: tool calling, MCP and the agent scaling trap.

#SpringAI #RAG
