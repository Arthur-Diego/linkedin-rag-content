---
id: "009"
topic: agentic rag
title: "Agentic RAG: quando o pipeline vira um loop"
image:
  headline: "Agentic RAG: buscar, avaliar, buscar de novo"
  bullets:
    - "Pipeline linear busca uma vez e reza"
    - "Agente avalia o que achou e decide o próximo passo"
    - "Auto-crítica antes de responder"
    - "Custo e latência: use com parcimônia"
alt_text: "Card técnico sobre Agentic RAG e loops de retrieval"
status: ready
---
O RAG tradicional é uma linha reta: busca, monta o contexto, responde. Uma chance. Se o retrieval falhou, a resposta nasce condenada — e o modelo nem sabe disso.

Agentic RAG transforma a linha num loop. O LLM deixa de ser o último estágio e vira o operador do pipeline:

1. Decide SE precisa buscar — "quanto é 15% de 300?" não precisa de retrieval nenhum.

2. Decide ONDE buscar — base de contratos, documentação técnica ou busca na web são ferramentas diferentes para perguntas diferentes.

3. Avalia o que voltou — "esses chunks respondem a pergunta?" Se não, reformula a query e tenta de novo, em vez de alucinar por cima de contexto ruim.

4. Critica a própria resposta antes de entregar — a afirmação está sustentada pelas fontes? Falta cobrir metade da pergunta? Volta ao passo 2.

É a diferença entre um estagiário que devolve a primeira coisa que achou no Google e um analista que pesquisa até ter a resposta.

O custo é real e proporcional: cada iteração é mais uma chamada de LLM, e a latência deixa de ser previsível. Por isso a arquitetura sensata é híbrida — pipeline linear para o caso comum, com um teto de 2 ou 3 iterações extras quando a auto-avaliação reprova o retrieval.

Comece pelo passo 3: uma única checagem de "o contexto responde a pergunta?" antes da geração já elimina uma família inteira de alucinações.

Seu RAG tem direito a uma segunda tentativa? 👇

#RAG #AgenticAI #IA #LLM #AIAgents
