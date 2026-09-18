---
id: "024"
topic: spring ai
title: "Spring AI 2.0 typed output: records as contracts for a probabilistic model"
image:
  palette: spring
  headline: "A Java record is your best prompt"
  diagram: |
    flowchart LR
        P["Prompt"]:::accent --> ASK["Ask for JSON<br/>in prose"]:::bad
        ASK --> RGX["Regex parse,<br/>NPE at 2am"]:::bad
        P --> REC["Record +<br/>sealed schema"]:::good
        REC --> VAL["Validation<br/>advisor"]:::good
        VAL -->|"invalid"| REC
        VAL --> OBJ["Typed<br/>object"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Records + sealed interfaces become the schema the model must obey"
    - "Validation advisor re-asks on invalid output, with a retry cap"
    - "2.0: tools run only through ChatClient + ToolCallingAdvisor"
alt_text: "Diagram contrasting asking for JSON in prose and regex-parsing it against giving the model a Java record schema, validating the output with an advisor that re-asks when invalid, and receiving a typed object"
status: ready
---
A Java record is the best prompt you will ever write.

Spring AI 2.0 went GA in June 2026 on Spring Boot 4, with JSpecify null-safety across the API. The theme is one word: contracts.

Picture two integrations: one asks for "valid JSON please" and regex-parses the reply until it throws at 2am; the other hands the model a schema built from a record and gets a typed object or a retry.

What separates a senior integration from a demo:

1. Model the answer as a record, with a sealed interface for the variants. The output converter turns it into the JSON schema the model must satisfy.
2. Add StructuredOutputValidationAdvisor. Invalid output goes back with the error as feedback. Cap it at 2, not "until it works".
3. Migration trap: 2.0 removed the tool loop from ChatModel. Tools run only through ChatClient with ToolCallingAdvisor. Direct ChatModel calls silently stop executing tools.
4. Past 30 tools, switch to ToolSearchToolCallingAdvisor: the model discovers tools progressively instead of paying for the full catalog every request.

The bigger lesson: you don't make a probabilistic component reliable by asking nicely. You wrap it in contracts the compiler can check and bound every retry.

Records or raw JSON strings: what does your LLM return today? 👇

📚 Part 3 of 3 — Trustworthy Spring AI.

#SpringAI #Java #StructuredOutput
