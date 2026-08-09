---
id: "006"
topic: evaluation
title: "RAG evaluation: without metrics, every pipeline looks good"
image:
  headline: "How do you know your RAG got better?"
  bullets:
    - "A working demo is not a metric"
    - "Measure retrieval and generation separately"
    - "50 real questions with known answers"
    - "LLM-as-judge with a fixed rubric"
  prompt: "Abstract illustration of precision measurement, glowing gauges rulers and data charts floating in space, dark navy background with cyan accents, minimal futuristic style"
alt_text: "Technical card about evaluating RAG systems"
status: ready
---
"I tested it and it answered correctly" — that's how RAG systems die in production.

Without an evaluation set, every pipeline change is a guess. You tweak the chunking, the demo feels better, you ship — and weeks later discover that recall dropped for half the questions nobody tested.

The minimum evaluation kit I stand behind:

1. A golden set: 50-100 REAL questions — pulled from logs, tickets, user chats — with the correct answer and source document annotated. One day of work that becomes the most valuable asset in the project.

2. Retrieval metrics separate from generation: recall@k and MRR answer "did the right document arrive?". If retrieval failed, don't even bother judging the final answer. Most RAG problems die right here.

3. Generation metrics: faithfulness to the context and completeness, scored by an LLM judge with a closed rubric — a 1-5 scale with written criteria, not "rate this answer". Frameworks like RAGAS already structure this.

4. Regression on every change: touched the prompt, the chunking, the model? Re-run the golden set. It's CI for answer quality.

The golden rule: instrument first, optimize second. Optimization without measurement is just motion.

Does your RAG have a golden set, or is it still in "works on my machine" mode? 👇

#RAG #LLM #AI #MLOps #AIEngineering
