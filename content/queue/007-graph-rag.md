---
id: "007"
topic: graph rag
title: "Graph RAG: when similarity can't reach the answer"
image:
  headline: "Local questions need chunks. Global questions need graphs."
  diagram: |
    flowchart LR
        Q1["Local question<br/>'what is X?'"]:::accent --> V["Vector search"] --> A1["Answer lives in<br/>1-2 chunks"]:::good
        Q2["Global question<br/>themes &middot; connections"]:::accent --> V2["Vector search"] -.-> MISS["No single<br/>right chunk"]:::bad
        Q2 --> KG["Knowledge graph<br/>entities + relations"]
        KG --> COM["Community<br/>summaries"] --> A2["Answer spans the<br/>whole collection"]:::good
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "An LLM extracts entities and relations at indexing time and builds the graph"
    - "Community detection + pre-generated summaries answer the big-picture questions"
    - "LLM-powered indexing is expensive — adopt it only where vectors provably fail"
alt_text: "Diagram comparing vector RAG for local questions with Graph RAG using a knowledge graph for global questions"
status: ready
---
"What are the main themes across these 10,000 documents?"

One question, and your entire RAG breaks. Not because the model is weak — because similarity search answers LOCAL questions, where the answer lives in 1-2 chunks. Global questions have no right chunk: the answer is scattered across the collection.

Split the world in two: local questions ride vector search and land on 1-2 chunks; global questions hit a dead end there — no single right chunk exists — and only the knowledge-graph route, with entities and community summaries, reaches an answer.

Graph RAG builds that route:

1. At indexing, an LLM extracts entities and relations from each document → knowledge graph.

2. Community detection groups connected entities; each community gets a pre-generated summary.

3. At query time: global questions read the summaries; local ones traverse the graph — connecting facts that share no vocabulary across 4 different documents.

The price is real: LLM-powered indexing costs 10-100x more than embedding, and the graph needs maintenance.

The bigger lesson: Graph RAG complements vector RAG, it doesn't replace it. Adopt it for the questions vectors provably fail — not because it's the acronym of the month.

Have you hit questions your RAG simply can't reach? 👇

#RAG #GraphRAG #KnowledgeGraph
