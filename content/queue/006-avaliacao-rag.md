---
id: "006"
topic: evaluation
title: "RAG evaluation: without metrics every pipeline looks good"
image:
  headline: "CI for answer quality: the RAG evaluation loop"
  diagram: |
    flowchart LR
        VIBES["Ship on vibes<br/>'tested it, works'"]:::bad --> REG["Silent regressions<br/>weeks later"]:::bad
        GOLD["Golden set<br/>50-100 real questions"]:::accent --> RET["Retrieval metrics<br/>recall@k &middot; MRR"]
        RET --> GEN["Generation metrics<br/>faithfulness &middot; completeness"]
        GEN --> LOOP["Re-run on EVERY<br/>pipeline change"]:::good
        LOOP --> SHIP["Ship with<br/>evidence"]:::good
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Measure retrieval separately: if the right document never arrived, don't judge the answer"
    - "LLM-as-judge needs a closed rubric — written criteria on a 1-5 scale, not 'rate this'"
    - "Changed the prompt, chunking or model? Golden set runs again. Every time."
alt_text: "Diagram of a RAG evaluation loop with a golden set, retrieval metrics, generation metrics and regression on every change"
status: ready
---
"I tested it and it answered correctly."

That sentence has shipped more broken RAG systems than any bug. You tweak the chunking, the demo feels better, you deploy — and weeks later recall has quietly dropped for half the questions nobody tried.

Two cultures, two outcomes: "ship on vibes" flows straight into silent regressions; the evaluation culture runs every change through a golden set, retrieval metrics and generation metrics before anything ships.

The minimum evaluation kit:

1. Golden set — 50-100 REAL questions from logs and tickets, each with the correct answer and source document annotated. One day of work.

2. Retrieval metrics first — recall@k and MRR answer "did the right document arrive?". Most RAG problems die right here, before generation.

3. Generation metrics — faithfulness and completeness, scored by an LLM judge with a written 1-5 rubric. Frameworks like RAGAS structure this.

4. Regression on every change — prompt, chunking, model: golden set runs again. It's CI for answer quality.

The bigger lesson: instrument first, optimize second. Optimization without measurement is just motion — it feels like progress and proves nothing.

Does your RAG have a golden set? 👇

#RAG #MLOps #AIEngineering
