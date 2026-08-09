---
id: "002"
topic: embeddings
title: "Embeddings: o modelo importa menos do que você pensa"
image:
  headline: "Embeddings em RAG: 4 decisões que importam"
  bullets:
    - "Benchmark público não é o seu domínio"
    - "Dimensão maior = custo maior, nem sempre ganho"
    - "Normalize e fixe a métrica de distância"
    - "Reindexar tudo a cada troca de modelo"
alt_text: "Card técnico sobre escolha de modelos de embedding em RAG"
status: ready
---
Todo mundo pergunta qual é o melhor modelo de embedding. Quase ninguém pergunta o que realmente importa: como ele se comporta no SEU domínio.

O ranking do MTEB é um ótimo ponto de partida — e um péssimo ponto de chegada. Um modelo campeão em benchmark genérico pode tropeçar em jargão jurídico, código-fonte ou português técnico. A única resposta confiável vem de um teste com seus próprios documentos e suas próprias perguntas.

O que eu avalio antes de escolher:

1. Idioma: seu corpus é em português? Modelos multilíngues variam muito de qualidade entre idiomas.

2. Dimensão do vetor: 3072 dimensões custam mais em storage e latência que 768. Se o ganho de recall for de 1%, não paga.

3. Janela de contexto do embedding: chunks maiores que o limite são truncados silenciosamente — e você nunca fica sabendo.

4. Consistência: trocou de modelo? Reindexe TUDO. Vetores de modelos diferentes no mesmo índice é bug garantido e silencioso.

Regra prática: escolha 2 ou 3 candidatos, rode nos seus dados com 50 perguntas reais e meça recall@k. Uma tarde de trabalho que evita meses de retrieval medíocre.

Você já mediu o recall do seu retrieval ou está confiando no benchmark? 👇

#RAG #Embeddings #IA #LLM #VectorSearch
