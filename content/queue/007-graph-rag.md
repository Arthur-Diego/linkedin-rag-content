---
id: "007"
topic: graph rag
title: "Graph RAG: quando busca por similaridade não alcança"
image:
  headline: "Graph RAG: respostas que exigem conexões"
  bullets:
    - "Similaridade não responde perguntas globais"
    - "Entidades e relações viram um grafo"
    - "Comunidades resumidas respondem o macro"
    - "Custo alto: use onde vetor comprovadamente falha"
alt_text: "Card técnico sobre Graph RAG e grafos de conhecimento"
status: ready
---
"Quais são os principais temas destes 10 mil documentos?" — essa pergunta quebra qualquer RAG tradicional.

Busca por similaridade responde perguntas locais: a resposta vive em um ou dois chunks. Mas perguntas globais — temas dominantes, conexões entre entidades, cadeias de dependência — não têm UM chunk certo. A resposta está espalhada pela coleção inteira.

Graph RAG ataca isso mudando a estrutura:

1. Na indexação, um LLM extrai entidades e relações de cada documento e monta um grafo de conhecimento.

2. Algoritmos de detecção de comunidades agrupam entidades conectadas, e cada comunidade ganha um resumo gerado previamente.

3. Na consulta, perguntas globais são respondidas pelos resumos das comunidades; perguntas locais navegam o grafo — da entidade citada aos seus vizinhos, juntando contexto que nenhuma busca vetorial encontraria junto.

O caso clássico: "qual a relação entre o fornecedor X e o incidente Y?" — a resposta atravessa 4 documentos que não compartilham vocabulário. Só o grafo conecta.

O preço é real: indexar com LLM custa caro, manter o grafo atualizado dá trabalho, e a latência sobe. Por isso minha regra: Graph RAG não substitui o RAG vetorial — complementa. Adote quando tiver perguntas que o vetor comprovadamente não responde, não porque é a sigla do momento.

Você já esbarrou em perguntas que o RAG tradicional não alcança? 👇

#RAG #GraphRAG #KnowledgeGraph #IA #LLM
