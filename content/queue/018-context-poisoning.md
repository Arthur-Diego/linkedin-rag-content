---
id: "018"
topic: context engineering
title: "Context poisoning: one bad fact corrupts an agent's whole run"
image:
  palette: ai
  headline: "Context poisoning: one bad fact, every step"
  diagram: |
    flowchart LR
        HALL["Hallucination<br/>enters context"]:::bad --> REUSE["Reused each<br/>step"]:::bad
        REUSE --> BREAK["Whole run<br/>corrupted"]:::bad
        SRC["Untrusted<br/>input"]:::accent --> ISO["Isolate +<br/>validate"]:::good
        ISO --> SAFE["Poison<br/>contained"]:::good
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "A single hallucination in context gets reused and compounds every step"
    - "Long-horizon agents rot without active curation, not just bigger windows"
    - "Treat retrieved and tool output as untrusted — isolate data from instructions"
alt_text: "Diagram contrasting a hallucination that propagates through every agent step against isolating and validating untrusted input to contain it"
status: ready
---
One hallucination in context poisons every step that follows.

It's called context poisoning: a false fact enters the window, the agent treats it as established, and every later step builds on it. In a long-horizon run, one bad token compounds into a broken outcome.

Picture two agents hitting the same bad input: one folds it into context and repeats it forever; the other isolates and validates it before it ever becomes "truth."

What separates a robust agent from a demo:

1. Treat retrieved docs and tool output as untrusted input. Keep data and instructions in separate, labeled sections.
2. Validate before committing a fact to long-term context — a cheap check beats a compounding error.
3. Curate memory actively: summarize, drop, re-verify. Bigger windows don't fix rot; disciplined context does.
4. Add tripwires — if the agent contradicts an earlier verified fact, stop and re-ground instead of pressing on.

The bigger lesson: an agent is only as reliable as the worst token in its context. Senior teams engineer context as an adversarial surface, not a scratchpad.

How do you keep bad facts out of your agent's memory? 👇

📚 Part 3 of 3 — Context Engineering.

#AIEngineering #AIAgents
