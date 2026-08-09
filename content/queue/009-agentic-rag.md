---
id: "009"
topic: agentic rag
title: "Agentic RAG: when the pipeline becomes a loop"
image:
  headline: "Agentic RAG: search, evaluate, search again"
  bullets:
    - "Linear pipelines search once and pray"
    - "An agent evaluates results and decides the next step"
    - "Self-critique before answering"
    - "Cost and latency: use sparingly"
  prompt: "Abstract illustration of an intelligent feedback loop, circular flow of glowing arrows and decision nodes, autonomous agent concept, dark navy background with cyan and electric blue accents, futuristic minimal style"
alt_text: "Technical card about Agentic RAG and retrieval loops"
status: ready
---
Traditional RAG is a straight line: search, build context, answer. One shot. If retrieval failed, the answer is doomed at birth — and the model doesn't even know it.

Agentic RAG turns the line into a loop. The LLM stops being the last stage and becomes the pipeline's operator:

1. It decides WHETHER to search — "what's 15% of 300?" needs no retrieval at all.

2. It decides WHERE to search — the contracts database, technical docs, and web search are different tools for different questions.

3. It evaluates what came back — "do these chunks answer the question?" If not, it reformulates the query and tries again, instead of hallucinating on top of bad context.

4. It critiques its own answer before delivering — is every claim supported by the sources? Is half the question still uncovered? Back to step 2.

It's the difference between an intern who returns the first thing they found on Google and an analyst who keeps digging until they have the answer.

The cost is real and proportional: every iteration is another LLM call, and latency stops being predictable. So the sensible architecture is hybrid — a linear pipeline for the common case, with a cap of 2-3 extra iterations when self-evaluation rejects the retrieval.

Start with step 3: a single "does this context answer the question?" check before generation already eliminates a whole family of hallucinations.

Does your RAG get a second chance? 👇

#RAG #AgenticAI #LLM #AI #AIAgents
