---
id: "008"
topic: cache semântico
title: "Cache semântico: a otimização de custo mais ignorada em RAG"
image:
  headline: "Cache semântico: pague uma vez, responda mil"
  bullets:
    - "Perguntas repetidas dominam o tráfego real"
    - "Cache por similaridade, não por igualdade"
    - "Threshold errado = resposta errada com cara de certa"
    - "Invalide quando o documento-fonte mudar"
alt_text: "Card técnico sobre cache semântico em aplicações LLM"
status: ready
---
Olhe os logs do seu RAG em produção. Aposto que 30% das perguntas são variações das mesmas 50 dúvidas.

"Como emitir a segunda via?", "segunda via do boleto", "quero a 2ª via" — três strings diferentes, a mesma pergunta, três execuções completas do pipeline: retrieval, reranking, geração. Pagando LLM as três vezes.

Cache tradicional não resolve: a chave nunca bate, porque a string nunca é igual. Cache semântico compara por embedding — se a nova pergunta tem similaridade acima do threshold com uma pergunta já respondida, devolve a resposta guardada. Latência de segundos para milissegundos, custo de tokens para zero.

As três decisões que separam um cache útil de uma fábrica de respostas erradas:

1. Threshold conservador: comece alto, perto de 0.95. "Cancelar plano A" e "cancelar plano B" são vizinhos no espaço vetorial — e respostas diferentes. Falso positivo em cache é resposta errada entregue com confiança.

2. Invalidação por fonte: guarde junto da resposta os documentos que a geraram. Documento atualizado, entradas derivadas expiram. Cache de RAG sem invalidação vira um museu de respostas desatualizadas.

3. Escopo por usuário ou tenant: respostas que dependem de permissão nunca podem vazar pelo cache global.

É uma tarde de implementação — o embedding você já calcula de qualquer forma — e a conta do provedor de LLM agradece no fim do mês.

Seu pipeline responde a mesma pergunta quantas vezes por dia? 👇

#RAG #IA #LLM #FinOps #EngenhariaDeIA
