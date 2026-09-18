---
id: "016"
topic: spring ai
title: "Spring AI observability: the LLM call you can't see is the one that bills you"
image:
  palette: spring
  headline: "Your LLM call is already traced. Look."
  diagram: |
    flowchart LR
        REQ["ChatClient<br/>request"]:::accent --> BLIND["No spans,<br/>surprise bill"]:::bad
        REQ --> ADV["Advisor<br/>span"]:::good
        ADV --> MODEL["gen_ai.client<br/>.operation"]:::good
        MODEL --> TOOL["spring.ai<br/>.tool span"]:::good
        MODEL --> TOK["Token usage<br/>metric"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "gen_ai_client_token_usage_total: cost per model, out of the box, zero code"
    - "Every advisor, tool call and vector query becomes its own span"
    - "Prompt and completion logging is OFF by default. Keep it off in prod"
alt_text: "Diagram contrasting an untraced ChatClient request that ends in a surprise bill against a traced one where advisor, model, tool and token-usage observations form a chain"
status: ready
---
Your busiest endpoint is an LLM call and nobody knows what it cost yesterday.

Spring AI already emits Micrometer observations for every model call, advisor, tool execution and vector query, following the OpenTelemetry gen_ai conventions. Most teams never open the dashboard.

Picture two services under the same traffic: one sees a single HTTP span and a monthly invoice; the other sees a chain, with tokens counted at every link.

What separates a monitored AI service from a blind one:

1. Alert on tokens, not latency. gen_ai_client_token_usage_total, split by input and output per model, is your cost SLO. Latency hides a 10x prompt regression.
2. Trace the chain, not the call. One agent turn with 3 tools is 1 chat-client span, 4 model spans and 3 tool spans. Fan-out is where cost hides.
3. Prompt logging is opt-in for a reason: log-prompt defaults to false because prompts carry PII. Staging yes, prod never.
4. Streaming gotcha: the HTTP span is not parented under the model span. Attribute cost to gen_ai.client.operation, not to HTTP.

The bigger lesson: non-determinism is not a license to fly blind. The discipline that saved microservices is the one that saves agents.

Do you know what your busiest LLM endpoint cost yesterday? 👇

📚 Part 1 of 3 — Trustworthy Spring AI. Next: Part 2 puts a judge model in the advisor chain.

#SpringAI #Observability #JavaDevelopers
