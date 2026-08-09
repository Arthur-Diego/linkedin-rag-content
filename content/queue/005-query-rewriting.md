---
id: "005"
topic: query rewriting
title: "Query rewriting: o problema não é o índice, é a pergunta"
image:
  headline: "Reescreva a pergunta antes de buscar"
  bullets:
    - "Usuário pergunta mal, e tudo bem"
    - "Multi-query: 3 variações da mesma pergunta"
    - "HyDE: busque com a resposta hipotética"
    - "Decomponha perguntas compostas"
alt_text: "Card técnico sobre reescrita de queries em RAG"
status: ready
---
Passamos meses otimizando índice, chunking e embeddings — e esquecemos que a query do usuário costuma ser a pior parte do pipeline.

"não funciona o negócio do relatório" — é isso que chega no seu retrieval. Nenhum embedding salva uma pergunta assim. A boa notícia: você tem um LLM na mão, e reescrever texto é o que ele faz de melhor.

Três técnicas que uso em produção:

1. Multi-query: o LLM gera 3 variações da pergunta com vocabulários diferentes. Roda as buscas em paralelo e funde os resultados com RRF. Cobre o vão entre o jargão do usuário e o jargão dos documentos.

2. HyDE: peça ao modelo uma resposta hipotética para a pergunta e use ESSE texto como query. Uma resposta imaginária se parece muito mais com o documento real do que a pergunta original.

3. Decomposição: "compare a cobertura do plano X com o plano Y" vira duas buscas — uma por plano — e o modelo compõe a resposta no final. Perguntas compostas quase nunca são respondidas por um único chunk.

O custo? Uma chamada extra de um modelo pequeno e barato antes da busca. A latência sobe um pouco; a taxa de resposta certa sobe muito mais.

Antes de trocar seu vector store: sua query merece uma segunda chance? 👇

#RAG #IA #LLM #NLP #EngenhariaDeIA
