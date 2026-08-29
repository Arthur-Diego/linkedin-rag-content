---
id: "019"
topic: lgpd
title: "LGPD for engineers: the fine is for silence, not the leak"
image:
  headline: "LGPD: the fine is for silence, not the leak"
  diagram: |
    flowchart LR
        INC["Data<br/>incident"]:::accent --> HIDE["Stay quiet,<br/>hope it passes"]:::bad
        HIDE --> FINE["Sanction up to<br/>R$50M"]:::bad
        INC --> LOG["Detect + log<br/>in hours"]:::good
        LOG --> NOTIFY["Notify ANPD<br/>in 3 days"]:::good
        NOTIFY --> TRUST["Mitigating<br/>factor"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "Most common ANPD violation: failing to notify, not the breach itself"
    - "Incident clock: 3 business days to notify ANPD and data subjects"
    - "Sanctions reach 2% of revenue, capped at R$50M per violation"
alt_text: "Diagram contrasting hiding a data incident (sanction up to R$50M) against detecting, logging and notifying ANPD within 3 business days"
status: ready
---
The most common LGPD violation isn't the leak. It's the silence after it.

In 2026 ANPD became a full regulatory agency and opened 19 sanctioning processes in one month. Its case map shows the recurring failure: companies that never notified — not companies that got hacked.

Picture two teams facing the same exposed S3 bucket. One quietly rotates keys. The other detects, logs and notifies. Only one walks into the hearing with a mitigating factor.

What engineering owns here:

1. Detection with a timestamp. The 3-business-day clock to notify ANPD starts when you knew — so alerts on public buckets and leaked tokens are compliance controls.
2. An incident log you can hand over: what data, how many subjects, which systems.
3. A path from on-call to the DPO in under an hour, or the deadline is gone.

The bigger lesson: regulators punish what you can't explain far harder than what you couldn't prevent. Fines reach 2% of revenue, capped at R$50M per violation — and good faith is weighed first.

Does your on-call runbook have a "personal data" branch? 👇

📚 Part 1 of 3 — LGPD for Engineers. Next: four controls that make LGPD deployable.

#LGPD #DataPrivacy #SoftwareEngineering
