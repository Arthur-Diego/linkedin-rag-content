---
id: '017'
topic: spring ai
title: 'Spring AI LLM-as-a-judge: a second model that can veto the first'
image:
  palette: spring
  headline: Let a second model grade the first
  diagram: "flowchart LR\n    Q[\"User<br/>prompt\"]:::accent --> GEN[\"Generate<br/>(model\
    \ A)\"]:::accent\n    GEN --> JUDGE[\"Judge<br/>(model B)\"]:::accent\n    JUDGE\
    \ -->|\"score &ge; 4\"| OK[\"Return<br/>answer\"]:::good\n    JUDGE -->|\"score\
    \ &lt; 4\"| FB[\"Feedback into<br/>prompt\"]:::bad\n    FB --> GEN\n    FB -->|\"\
    cap hit\"| LAST[\"Return last,<br/>flag it\"]:::bad\n    classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d\n\
    \    classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d\n    classDef accent\
    \ fill:#0284c7,stroke:#0369a1,color:#ffffff\n"
  bullets:
  - Judge scores 1-4; below the bar, its feedback goes back into the prompt
  - Use a separate judge model. Models grade their own answers too kindly
  - Cap retries at 2-3. Every loop multiplies tokens and latency
alt_text: 'Diagram of a self-refine loop: model A generates, model B judges on a 1
  to 4 scale, a passing score returns the answer, a failing score feeds feedback back
  into the prompt until a retry cap is hit'
status: published
published_at: '2026-09-25T18:29:06+00:00'
linkedin_post_id: urn:li:share:7509318075008163840
---
Your unit tests are green. Your LLM answers are still wrong.

Assertions can't grade prose. Spring AI's answer is a recursive advisor: an interceptor that can call the chain again, turning "generate" into "generate, judge, refine".

Picture two answers leaving your service: one goes straight to the user; the other passes a second model that scores it 1 to 4, and only a 4 gets through.

How to run the loop in production:

1. Wire a SelfRefineEvaluationAdvisor: it asks a judge for rating, evaluation and feedback as structured output, and appends the feedback to the prompt on failure.
2. Use a different model as judge. A model scores its own output too kindly. A small local judge on Ollama costs nothing per call.
3. Bound the loop. The reference example allows 15 attempts. In production, 2 or 3. Each retry doubles tokens and adds a round trip.
4. Keep it off the streaming path. Recursive advisors are call-only, so gate only the endpoints where a wrong answer costs more than 2 seconds.

The bigger lesson: quality gates belong in the request path, not only in CI. Evaluation is a runtime concern now.

Would you let a second model veto your first model's answer? 👇

📚 Part 2 of 3 — Trustworthy Spring AI. Next: Part 3 makes the model return a Java record.

#SpringAI #LLMEvaluation #JavaDevelopers
