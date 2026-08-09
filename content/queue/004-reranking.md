---
id: "004"
topic: reranking
title: "Reranking: a segunda opinião que seu retrieval precisa"
image:
  headline: "Reranking: precisão depois do recall"
  bullets:
    - "Retrieval otimiza recall, reranker otimiza precisão"
    - "Cross-encoder lê query + documento juntos"
    - "Busque top-50, reranqueie, envie top-5"
    - "Menos contexto lixo = menos alucinação"
alt_text: "Card técnico sobre reranking em pipelines RAG"
status: ready
---
Seu retrieval devolve 20 documentos. Quantos são realmente relevantes? Se a resposta é "uns 5", você não tem um problema de busca — tem um problema de ranking.

A busca vetorial usa bi-encoders: query e documento viram vetores separadamente, e a comparação é uma conta de similaridade. É rápido o suficiente para varrer milhões de documentos, mas superficial — os dois textos nunca se "leem".

O reranker é um cross-encoder: recebe query e documento JUNTOS e produz um score de relevância. É caro demais para rodar no corpus inteiro, mas perfeito para refinar uma lista curta.

O padrão que funciona:

1. Retrieval híbrido traz top-50 candidatos, otimizando recall.
2. Reranker reordena esses 50, otimizando precisão.
3. Só o top-5 entra no contexto do LLM.

O efeito colateral mais subestimado: menos lixo no contexto significa menos alucinação. O modelo não precisa adivinhar qual dos 20 trechos importa — os 5 que chegaram são os certos. E contexto menor ainda sai mais barato e mais rápido.

Para começar: os rerankers open source da família BGE rodam bem até em CPU para listas de 50 documentos. Custo de infra próximo de zero, ganho de qualidade visível no primeiro dia.

Você usa reranking ou manda o retrieval cru para o modelo? 👇

#RAG #Reranking #IA #LLM #NLP
