---
id: "005"
topic: query rewriting
title: "Query rewriting: fix the question before the search"
image:
  headline: "The worst input in your pipeline is the query"
  diagram: |
    flowchart LR
        Q["Vague question<br/>'report thing broken'"]:::bad --> MQ["Multi-query<br/>3 variations"]
        Q --> HY["HyDE<br/>hypothetical answer"]
        Q --> DE["Decompose<br/>1 question &rarr; 2 searches"]
        MQ --> S["Parallel<br/>searches"]:::accent
        HY --> S
        DE --> S
        S --> RRF["RRF merge"]:::good
        RRF --> DOCS["Right documents<br/>found"]:::good
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Multi-query bridges the gap between user jargon and document jargon"
    - "HyDE: a hypothetical answer looks more like the real document than the question does"
    - "One extra call to a small model — latency up a little, correct answers up a lot"
alt_text: "Diagram showing a vague query being rewritten via multi-query, HyDE and decomposition before searching"
status: ready
---
Months tuning the index. Zero minutes fixing the questions that hit it.

That's the usual budget split in RAG — inverted. Because what actually reaches your retrieval is "the report thing doesn't work". No embedding model saves that query.

You have an LLM sitting right there. Rewriting text is what it does best:

1. Multi-query — generate 3 variations with different vocabulary, search in parallel, merge with RRF. Bridges user jargon vs document jargon.

2. HyDE — ask for a hypothetical answer, then search with THAT text. An imagined answer resembles the real document far more than the question does.

3. Decomposition — "compare plan X with plan Y" becomes two searches, one per plan. Compound questions are almost never answered by a single chunk.

The cost: one call to a small, cheap model before the search.

The bigger lesson: garbage in, garbage out applies to retrieval too — and unlike most GIGO problems, this one has a one-afternoon fix.

Do you rewrite queries before searching? 👇

#RAG #LLM #AIEngineering
