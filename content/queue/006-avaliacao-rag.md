---
id: "006"
topic: avaliação
title: "Avaliação de RAG: sem métrica, todo pipeline parece bom"
image:
  headline: "Como saber se seu RAG melhorou?"
  bullets:
    - "Demo que funciona não é métrica"
    - "Meça retrieval e geração separados"
    - "50 perguntas reais com resposta conhecida"
    - "LLM-as-judge com rubrica fechada"
alt_text: "Card técnico sobre avaliação de sistemas RAG"
status: ready
---
"Testei aqui e respondeu certo" — assim morrem os RAGs em produção.

Sem um conjunto de avaliação, cada mudança no pipeline é um chute. Você troca o chunking, a demo parece melhor, faz o deploy — e descobre semanas depois que o recall caiu para metade das perguntas que ninguém testou.

O kit mínimo de avaliação que defendo:

1. Golden set: 50 a 100 perguntas REAIS — tiradas de logs, tickets, dúvidas de usuários — com resposta correta e documento-fonte anotados. Um dia de trabalho que vira o ativo mais valioso do projeto.

2. Métricas de retrieval separadas da geração: recall@k e MRR respondem "o documento certo chegou?". Se o retrieval falhou, nem adianta olhar a resposta final. A maioria dos problemas de RAG morre aqui.

3. Métricas de geração: fidelidade ao contexto e completude, avaliadas por um LLM juiz com rubrica fechada — nota de 1 a 5 com critérios escritos, não "avalie esta resposta". Frameworks como RAGAS já estruturam isso.

4. Regressão a cada mudança: mexeu no prompt, no chunking, no modelo? Roda o golden set de novo. É CI para qualidade de resposta.

A regra de ouro: primeiro instrumente, depois otimize. Otimização sem medição é só movimento.

Seu RAG tem golden set ou está no modo "testei aqui e funcionou"? 👇

#RAG #IA #LLM #MLOps #Qualidade
