---
id: "001"
topic: chunking
title: "Chunking: o corte errado mata seu RAG"
image:
  headline: "Chunking: onde a maioria dos RAGs morre"
  bullets:
    - "Tamanho fixo é baseline, não solução"
    - "Respeite fronteiras semânticas: títulos, parágrafos, funções"
    - "Overlap de 10-20% evita perder contexto na borda"
    - "Meça retrieval antes de trocar de estratégia"
alt_text: "Card técnico sobre estratégias de chunking em RAG"
status: ready
---
Seu RAG não está ruim por causa do modelo. Está ruim por causa do chunking.

A maioria dos pipelines começa cortando documentos em blocos de 500 tokens com tamanho fixo. Funciona como baseline, mas tem um problema: o corte ignora a estrutura do documento. Uma tabela cortada ao meio, uma cláusula separada do seu título, uma função sem a assinatura — o retrieval até encontra o chunk, mas o modelo recebe um fragmento sem sentido.

Três upgrades que costumam pagar o esforço:

1. Chunking estrutural: corte respeitando títulos, seções e parágrafos. Markdown e HTML já te dão essas fronteiras de graça.

2. Overlap de 10 a 20%: o contexto que vive na fronteira entre dois chunks deixa de se perder.

3. Metadados no chunk: título do documento, seção e data anexados ao texto. O embedding fica mais rico e o filtro fica possível.

E o mais importante: não troque de estratégia no escuro. Monte um conjunto pequeno de perguntas com resposta conhecida e meça o recall do retrieval antes e depois. Chunking se decide com número, não com intuição.

Qual estratégia de chunking você usa hoje? 👇

#RAG #IA #LLM #NLP #EngenhariaDeIA
