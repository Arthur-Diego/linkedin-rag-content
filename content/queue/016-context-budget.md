---
id: "016"
topic: context engineering
title: "Context engineering: the window is a budget, not a bucket"
image:
  palette: ai
  headline: "Context is a budget, not a bucket"
  diagram: |
    flowchart LR
        Q["Agent<br/>task"]:::accent --> DUMP["Dump whole<br/>window"]:::bad
        DUMP --> ROT["Context rot:<br/>quality drops"]:::bad
        Q --> CURATE["Curate high-<br/>signal tokens"]:::good
        CURATE --> BUDGET["Token budget<br/>per turn"]:::good
        BUDGET --> SHARP["Sharp, cheap<br/>answers"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Chroma tested 18 frontier models — every one degraded as context grew"
    - "More tokens mean more cost and more noise, not more accuracy"
    - "Goal: the smallest set of high-signal tokens that gets the outcome"
alt_text: "Diagram contrasting dumping the whole context window (context rot) against curating a high-signal token budget per turn"
status: ready
---
18 of 18 frontier models got worse as context grew.

That's Chroma's "context rot" finding — and it kills the instinct behind most AI systems: stuff everything into the window and let the model sort it out.

Context engineering flips that. Treat the window as a per-turn budget, not a bucket, and spend it on the smallest set of high-signal tokens that does the job.

Where teams blow the budget, and the fix:

1. Dumping full documents — retrieve, then rerank down to the top 3-5 chunks. Every extra token is cost and noise.
2. Keeping chat history verbatim — summarize old turns, keep only decisions and open threads.
3. Loading every tool "just in case" — the model reads all of it each turn, so load on demand.

The bigger lesson: prompt engineering asked "how do I ask?" Context engineering asks "what should the model see right now?" — and less, chosen well, beats more.

What's eating the most tokens in your context today? 👇

📚 Part 1 of 3 — Context Engineering. Next: why burying the answer mid-context costs 30% accuracy.

#AIEngineering #LLM
