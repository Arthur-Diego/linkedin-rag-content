---
id: "017"
topic: context engineering
title: "Lost in the middle: placement and compaction in production"
image:
  palette: ai
  headline: "Lost in the middle: placement beats length"
  diagram: |
    flowchart LR
        DOC["Key fact<br/>at start/end"]:::good --> HIT["Model<br/>attends"]:::good
        HIT --> ANS["Accurate<br/>answer"]:::accent
        MID["Key fact<br/>in middle"]:::bad --> MISS["Attention<br/>decays"]:::bad
        MISS --> DROP["-30%<br/>accuracy"]:::bad
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Evidence in the middle: accuracy drops 20-30% vs start or end (U-shape)"
    - "Compaction: summarize near the limit, restart the window with the summary"
    - "Position is a lever — put critical context first or last, never buried"
alt_text: "Diagram showing a U-shaped attention pattern: facts at the start or end are used, facts in the middle lose 30% accuracy"
status: ready
---
Bury the key fact mid-context and accuracy drops 30%.

Long context isn't a flat shelf. Model attention follows a U-shape — strong at the start and end, weak in the middle. Same evidence, worse answer, purely because of where it sits.

Picture the same document read two ways: the fact placed first or last gets used; the identical fact buried in the middle gets skipped.

Managing the window in production:

1. Place critical context first or last. After reranking, order matters as much as relevance.
2. Compact before you hit the limit — summarize the conversation, then restart the window with that summary instead of raw history.
3. Budget tokens per turn and measure. Track answer quality against context length, not just latency.
4. Cut low-signal filler; a shorter, well-ordered context usually beats a longer "complete" one.

The bigger lesson: with LLMs, where information sits is as important as whether it's there. Retrieval finds the right tokens; context engineering puts them where the model will actually read them.

Do you order your retrieved context, or just concatenate it? 👇

📚 Part 2 of 3 — Context Engineering. Next: how one bad fact poisons an agent's entire run.

#AIEngineering #ContextEngineering
