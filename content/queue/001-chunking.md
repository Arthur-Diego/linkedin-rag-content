---
id: "001"
topic: chunking
title: "Chunking: where most RAG pipelines die"
image:
  headline: "Chunking: where most RAG pipelines die"
  bullets:
    - "Fixed-size is a baseline, not a solution"
    - "Respect semantic boundaries: headings, paragraphs, functions"
    - "10-20% overlap saves context at the edges"
    - "Measure retrieval before switching strategies"
  prompt: "Abstract illustration of a large document being split into glowing organized fragments and blocks, dark navy background with cyan accents, geometric minimal style"
alt_text: "Technical card about chunking strategies in RAG"
status: ready
---
Your RAG isn't underperforming because of the model. It's underperforming because of your chunking.

Most pipelines start by slicing documents into fixed 500-token blocks. Fine as a baseline, but there's a problem: the cut ignores document structure. A table split in half, a clause separated from its heading, a function without its signature — retrieval finds the chunk, but the model receives a fragment that makes no sense.

Three upgrades that usually pay off:

1. Structure-aware chunking: split along headings, sections and paragraphs. Markdown and HTML give you these boundaries for free.

2. 10-20% overlap: the context living at the border between two chunks stops getting lost.

3. Metadata inside the chunk: document title, section and date attached to the text. Richer embeddings, and filtering becomes possible.

Most important of all: never switch strategies blindly. Build a small set of questions with known answers and measure retrieval recall before and after. Chunking decisions are made with numbers, not intuition.

What chunking strategy are you using today? 👇

#RAG #LLM #AI #MachineLearning #AIEngineering
