---
id: "013"
topic: spring ai
title: "Spring AI: LLMs in your microservices without the Python tax"
image:
  palette: spring
  headline: "Spring AI: LLMs without the Python tax"
  diagram: |
    flowchart LR
        APP["Spring<br/>service"]:::accent --> RAW["Raw model<br/>HTTP calls"]:::bad
        RAW --> GLUE["Hand-rolled<br/>prompt glue"]:::bad
        APP --> CC["ChatClient"]:::good
        CC --> ADV["Advisor chain:<br/>memory &middot; RAG"]:::good
        ADV --> ANY["Swap any of<br/>20+ models"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "One ChatClient, 20+ models — swap Anthropic to OpenAI without touching logic"
    - "Advisors are a filter chain for AI: memory, RAG and logging as interceptors"
    - "No Python sidecar: the LLM shares your JVM, tracing and security"
alt_text: "Diagram contrasting hand-rolled raw model calls against a Spring AI ChatClient with an advisor chain over 20+ swappable models"
status: ready
---
20-plus models, one ChatClient. No Python sidecar required.

That's the pitch of Spring AI — and for teams already on Spring, it lands hard. Since 1.0 GA, generative AI is a first-class citizen of the same stack that runs your microservices.

Picture two ways to add an LLM to a service: one bolts on a separate Python app and hand-rolls the prompt, memory and retrieval glue; the other calls a ChatClient whose advisor chain handles all of it, like a filter chain for AI.

What the ChatClient model buys you:

1. Vendor neutrality — one API over 20-plus models, from Anthropic to OpenAI. Switch providers by config, not a rewrite.
2. Advisors compose cross-cutting concerns — chat memory, RAG, logging, guardrails — without cluttering business logic.
3. One runtime — the model call shares your JVM, tracing, metrics and security. No extra service to deploy and page on.

The bigger lesson: the winning AI stack isn't the flashiest framework, it's the one your team already operates. Spring AI meets Java shops exactly where they are.

Still routing AI calls through a separate Python service? 👇

📚 Part 1 of 3 — Spring AI for Microservices. Next: turning a chat model into a RAG pipeline with one advisor.

#SpringAI #Java
