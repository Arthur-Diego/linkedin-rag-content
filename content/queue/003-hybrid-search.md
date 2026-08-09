---
id: "003"
topic: hybrid search
title: "Hybrid search: por que só vetor não basta"
image:
  headline: "Busca híbrida: vetor + BM25"
  bullets:
    - "Vetores erram códigos, siglas e nomes exatos"
    - "BM25 erra sinônimos e paráfrases"
    - "RRF combina os dois sem tuning"
    - "É o upgrade mais barato do seu retrieval"
alt_text: "Card técnico sobre busca híbrida combinando vetores e BM25"
status: ready
---
Busca vetorial encontra o que você quis dizer. Busca lexical encontra o que você escreveu. Seu RAG precisa das duas.

O caso clássico: o usuário pergunta pelo erro "ORA-01555" ou pelo contrato "CT-2024-0087". A busca vetorial devolve documentos semanticamente parecidos — mas não O documento, porque código exato não é semântica. O BM25 acha na primeira posição.

O caso inverso também existe: o usuário pergunta "como cancelar a assinatura" e o documento diz "rescisão do plano". O BM25 não vê sobreposição de termos. O vetor entende na hora.

A solução é rodar as duas buscas e fundir os resultados. O jeito mais simples e surpreendentemente eficaz: Reciprocal Rank Fusion. A fórmula cabe num tweet — cada documento ganha pontos pela posição em cada ranking, soma-se tudo. Sem pesos para calibrar, sem normalização de score entre sistemas diferentes.

Bônus: praticamente todo vector store moderno já suporta busca híbrida nativa — Qdrant, Weaviate, OpenSearch, pgvector com tsvector do Postgres. É configuração, não projeto.

Se você só tem busca vetorial hoje, hybrid search é provavelmente o maior ganho de retrieval por hora de trabalho investida.

Seu RAG já é híbrido? 👇

#RAG #HybridSearch #IA #LLM #InformationRetrieval
