---
id: "027"
topic: rag
title: "RAG in 3 hops: retrieve, augment, generate"
animation:
  title: "RAG in 3 Hops"
  subtitle: "Query path · retrieve, augment, generate"
  nodes:
    - {id: user, label: User, sub: "asks a question", at: [0, 0], color: blue}
    - {id: app, label: RAG Service, sub: "orchestrator", at: [1, 0], color: violet}
    - {id: llm, label: LLM, sub: "writes the answer", at: [2, 0], color: green}
    - {id: vdb, label: Vector DB, sub: "your documents", at: [1, 1], color: yellow}
  edges:
    - {from: user, to: app, label: question}
    - {from: app, to: user, label: answer}
    - {from: app, to: vdb, label: retrieve}
    - {from: vdb, to: app, label: chunks}
    - {from: app, to: llm, label: augment}
    - {from: llm, to: app, label: generate}
  steps:
    - caption: "The question does not go straight to the LLM"
      packets:
        - {path: [user, app], kind: info}
    - caption: "1. Retrieve: find the most relevant chunks"
      packets:
        - {path: [app, vdb, app], kind: warn, count: 3, every: 0.3}
    - caption: "2. Augment: question + chunks in one prompt"
      packets:
        - {path: [app, llm], kind: warn}
    - caption: "3. Generate: an answer grounded in your data"
      packets:
        - {path: [llm, app, user], kind: ok, turns: 0}
alt_text: "Animated diagram of the RAG query path: the user's question reaches the RAG service, which first retrieves relevant chunks from the vector database, then sends question plus chunks to the LLM, and returns an answer grounded in the retrieved data"
status: ready
---
3 hops. That is the whole trick behind RAG.

Watch the question: it stops at the vector DB first, picks up the most relevant chunks, and only then reaches the LLM with that context attached.

The model does not know your data. It reads it at question time, so better retrieval beats a bigger model.

Which hop breaks first in your pipeline? 👇

#RAG #AIEngineering #LLM
