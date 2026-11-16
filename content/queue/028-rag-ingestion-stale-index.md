---
id: "028"
topic: rag
title: "RAG ingestion: your answers are only as fresh as your index"
animation:
  title: "RAG Ingestion"
  subtitle: "Index path · runs before any question"
  nodes:
    - {id: docs, label: Documents, sub: "PDF · wiki · tickets", at: [0, 0], color: blue}
    - {id: chunker, label: Chunker, sub: "splits the text", at: [1, 0], color: violet}
    - {id: embed, label: Embedder, sub: "text to vector", at: [2, 0], color: orange}
    - {id: vdb, label: Vector DB, sub: "searchable index", at: [2, 1], color: yellow}
  edges:
    - {from: docs, to: chunker, label: document}
    - {from: chunker, to: embed, label: chunks}
    - {from: embed, to: vdb, label: vectors}
  tally: {ok: "chunks indexed", warn: "chunks re-indexed"}
  steps:
    - caption: "A document enters the pipeline"
      packets:
        - {path: [docs, chunker], kind: info}
    - caption: "One document becomes many chunks"
      packets:
        - {path: [chunker, embed], kind: info, count: 4, every: 0.3}
    - caption: "Each chunk is stored as one vector"
      packets:
        - {path: [embed, vdb], kind: ok, count: 4, every: 0.3}
    - caption: "The document changed? It makes the trip again"
      packets:
        - {path: [docs, chunker, embed, vdb], kind: warn, turns: 0, count: 2, every: 0.4}
alt_text: "Animated diagram of the RAG ingestion pipeline: a document is split into chunks by the chunker, each chunk is turned into a vector by the embedder and stored in the vector database, and when the document changes it travels the same path again to be re-indexed"
status: ready
---
Your RAG answers from the index, not from your documents.

Watch the pipeline: each document is split into chunks, each chunk becomes a vector, and only then can it be found. When a document changes, it has to make the same trip again.

Skip that re-index and the model keeps quoting the old version with full confidence.

How often do you re-index? 👇

#RAG #VectorDatabase #AIEngineering
