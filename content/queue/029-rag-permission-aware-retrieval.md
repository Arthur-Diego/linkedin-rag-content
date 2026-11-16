---
id: "029"
topic: rag
title: "Permission-aware RAG: the LLM cannot leak what it never saw"
animation:
  title: "Permission-Aware RAG"
  subtitle: "Filter at retrieval, not in the prompt"
  nodes:
    - {id: user, label: User, sub: "role: intern", at: [0, 0], color: blue}
    - {id: app, label: RAG Service, sub: "knows who asks", at: [1, 0], color: violet}
    - {id: llm, label: LLM, sub: "sees the prompt", at: [2, 0], color: green}
    - {id: vdb, label: Vector DB, sub: "chunks + ACL", at: [1, 1], color: yellow}
  edges:
    - {from: user, to: app, label: question}
    - {from: app, to: user, label: answer}
    - {from: app, to: vdb, label: search}
    - {from: vdb, to: app, label: chunks}
    - {from: app, to: llm, label: context}
    - {from: llm, to: app}
  tally: {bad: "chunks leaked", ok: "chunks allowed"}
  steps:
    - caption: "An intern asks about salaries"
      packets:
        - {path: [user, app, vdb], kind: info}
    - caption: "No filter: a restricted chunk hits the prompt"
      packets:
        - {path: [vdb, app, llm], kind: bad, turns: 0}
    - caption: "Fix: send the user's ACL with the search"
      packets:
        - {path: [user, app, vdb], kind: info}
    - caption: "Only allowed chunks leave the index"
      packets:
        - {path: [vdb, app, llm], kind: ok, turns: 0, count: 2, every: 0.4}
    - caption: "The LLM cannot leak what it never saw"
      packets:
        - {path: [llm, app, user], kind: info}
alt_text: "Animated diagram of permission-aware retrieval in RAG: without a filter a restricted chunk travels from the vector database into the LLM prompt, and with the user's access control list applied inside the search only allowed chunks leave the index"
status: ready
---
The LLM cannot leak a document it never saw.

Watch the intern's question: without a filter, a restricted chunk travels straight into the prompt. With the ACL applied inside the search, only allowed chunks leave the index.

Filter at retrieval, not in the prompt. "Do not reveal this" is an instruction, not access control.

Where do you enforce permissions in your RAG? 👇

#RAG #AISecurity #AIEngineering
