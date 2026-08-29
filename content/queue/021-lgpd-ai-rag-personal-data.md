---
id: "021"
topic: lgpd
title: "LGPD meets AI: personal data in embeddings, prompts and model weights"
image:
  headline: "Your vector store is personal data too"
  diagram: |
    flowchart LR
        DOC["Docs with<br/>PII"]:::accent --> EMB["Embed raw<br/>into vectors"]:::bad
        EMB --> STUCK["Can't delete,<br/>can't explain"]:::bad
        DOC --> SCRUB["Scrub PII<br/>before chunking"]:::good
        SCRUB --> META["Subject ID in<br/>chunk metadata"]:::good
        META --> ERASE["Deletion +<br/>explanation"]:::accent
        classDef bad fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
        classDef good fill:#dcfce7,stroke:#22c55e,color:#14532d
        classDef accent fill:#0284c7,stroke:#0369a1,color:#ffffff
  bullets:
    - "AI is one of 4 ANPD priority axes for 2026-27, with 20 planned inspections"
    - "Embeddings of PII are personal data — deletion requests reach your index"
    - "Art. 20: automated decisions need a plain-language explanation on demand"
alt_text: "Diagram contrasting embedding raw personal data into vectors (cannot delete or explain) against scrubbing PII before chunking and tagging subjects for deletion and explanation"
status: ready
---
Embedding a document doesn't anonymize it. A vector of a medical record is still a medical record.

ANPD made AI one of four priority enforcement axes for 2026-27, with 20 inspections planned and a task force on training data. It already suspended Meta's use of Brazilian posts for training.

Picture two RAG pipelines: one embeds raw support tickets and can neither delete a customer nor explain a refusal; the other scrubs before chunking, tags every chunk with its subject, and answers both in minutes.

What separates a compliant AI stack from an exposed one:

1. PII detection before chunking — Presidio or regex+NER replacing names, CPFs and emails with placeholders. Retrieval quality barely moves.
2. Subject ID in chunk metadata. A deletion request becomes a filtered delete, not a full re-ingest.
3. Prompt and completion logs are personal data: TTL them, strip PII, no vendor without a transfer basis.
4. LGPD Art. 20: if the model influences credit, hiring or pricing, log inputs and retrieved chunks per decision for a plain-language explanation.

The bigger lesson: weights don't have a DELETE statement. RAG keeps personal data deletable — a legal architecture choice, not just a technical one.

Can your pipeline delete one person from the vector index today? 👇

📚 Part 3 of 3 — LGPD for Engineers.

#LGPD #RAG #AIEngineering
