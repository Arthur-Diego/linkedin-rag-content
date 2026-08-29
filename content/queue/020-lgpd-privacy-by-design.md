---
id: "020"
topic: lgpd
title: "LGPD in production: privacy by design as four engineering controls"
image:
  headline: "Privacy by design: 4 controls that ship"
  diagram: |
    flowchart LR
        PII["Personal<br/>data"]:::accent --> RAW["Raw PII<br/>everywhere"]:::bad
        RAW --> LOGS["Leaks via logs<br/>+ backups"]:::bad
        PII --> MIN["Collect only<br/>what's needed"]:::good
        MIN --> TOKEN["Tokenize +<br/>encrypt"]:::good
        TOKEN --> TTL["Retention TTL<br/>+ audit trail"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Minimize: every field needs a purpose and a legal basis written down"
    - "Tokenize PII at the edge — one vault, not 40 copies across services"
    - "Retention as a TTL in code, not a policy PDF nobody enforces"
alt_text: "Diagram contrasting raw personal data spread across services and logs against minimization, tokenization and retention TTLs with an audit trail"
status: ready
---
40 copies of the same CPF is how a "small" breach becomes a big one.

Systems rarely leak from the database. They leak from the log line, the analytics event, the CSV export and the old backup that all carried raw PII because nobody decided where personal data was allowed to live.

Picture the two architectures: PII sprayed across every service versus one vault holding the real value and everything else holding a token. Same features, very different blast radius.

Privacy by design as controls you can deploy:

1. Minimize at the schema. Each personal field gets a purpose and a legal basis in the catalog. No purpose, no column.
2. Tokenize at the edge. Swap CPF, email and phone for vault tokens before they hit Kafka or your logs.
3. Encrypt with per-tenant keys and log every decrypt — that log answers "who accessed my data?"
4. Retention as a TTL job that deletes or anonymizes, tested like any feature. PDFs don't expire rows.

The bigger lesson: compliance in a document decays; compliance in the pipeline compounds. Teams that pass ANPD audits have architectures that prove things, not promise them.

Which of the four would break your stack first? 👇

📚 Part 2 of 3 — LGPD for Engineers. Next: personal data inside your LLM's context window.

#LGPD #PrivacyByDesign #DataEngineering
