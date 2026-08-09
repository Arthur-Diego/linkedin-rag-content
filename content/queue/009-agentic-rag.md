---
id: "009"
topic: agentic rag
title: "Agentic RAG: when the pipeline becomes a loop"
image:
  headline: "Search, evaluate, search again — with a budget"
  diagram: |
    flowchart LR
        Q["Question"]:::accent --> NEED{"Needs<br/>retrieval?"}
        NEED -- "no" --> DIRECT["Answer<br/>directly"]:::good
        NEED -- "yes" --> SEARCH["Search"]
        SEARCH --> CHECK{"Context<br/>answers it?"}
        CHECK -- "no &middot; max 3" --> RW["Rewrite<br/>query"]:::bad
        RW --> SEARCH
        CHECK -- "yes" --> DRAFT["Draft<br/>answer"]
        DRAFT --> CRIT{"Claims<br/>supported?"}
        CRIT -- "no" --> SEARCH
        CRIT -- "yes" --> FINAL["Final<br/>answer"]:::good
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "The LLM decides IF, WHERE and HOW MANY TIMES to search — instead of one blind shot"
    - "A single 'does this context answer it?' check kills a whole family of hallucinations"
    - "Cap the loop at 2-3 iterations: cost and latency grow with every pass"
alt_text: "Diagram of an agentic RAG loop where the LLM evaluates retrieval quality and retries before answering"
status: ready
---
1 shot. That's what a traditional RAG pipeline gets: search once, build context, answer.

If retrieval failed, the answer is doomed at birth — and the model doesn't even know it.

That loop has two checkpoints — "does the context answer it?" and "is every claim supported?" — guarding the way to the final answer, and every "no" routes back through a query rewrite, capped at 3 passes so cost stays bounded.

Agentic RAG turns the line into a loop. The LLM becomes the pipeline's operator:

1. Decides IF it should search — "what's 15% of 300?" needs no retrieval.

2. Decides WHERE — contracts DB, technical docs and web search are different tools.

3. Evaluates what came back — "does this context answer the question?" If not: rewrite the query and retry, instead of hallucinating over bad context.

4. Critiques its own draft — every claim supported by a source? No? Back to searching.

The cost is proportional: each iteration is another LLM call, and latency stops being predictable. So the sensible design is hybrid — linear pipeline for the common case, a 2-3 iteration budget when self-evaluation rejects the retrieval.

The bigger lesson: start with step 3. One relevance check before generation is 80% of the benefit at 10% of the complexity.

Does your RAG get a second chance? 👇

#RAG #AIAgents #AIEngineering
