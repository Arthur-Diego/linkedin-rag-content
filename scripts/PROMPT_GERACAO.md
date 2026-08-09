# Prompt oficial — reabastecer a fila de conteúdo

Quando a issue "Fila de conteúdo baixa" aparecer (ou quando quiser renovar a pauta),
abra o Claude Code na raiz deste repositório e cole o prompt abaixo. Custo: coberto
pela assinatura do Claude — nada de API paga.

---

Leia `content/published/` e `content/queue/` para ver os temas já cobertos e o formato
dos posts. Depois crie N novos posts sobre RAG em `content/queue/`, continuando a
numeração dos ids.

Regras:

1. Formato idêntico aos existentes: frontmatter YAML com `id` (string de 3 dígitos),
   `topic`, `title`, `image.headline`, `image.bullets` (3 a 4 bullets curtos),
   `alt_text` e `status: ready`; corpo = legenda do LinkedIn.
2. Legenda em português brasileiro: gancho forte na primeira linha, 3 a 5 parágrafos
   curtos ou lista numerada, insight prático de produção (não teoria de tutorial),
   pergunta de engajamento no final e 5 hashtags.
3. Temas: aprofundar ou complementar os já publicados sem repetir ângulo. Sugestões de
   pauta: chunking avançado, fine-tuning de embeddings, RAG multimodal, segurança e
   permissões em RAG, RAG vs long-context, contextual retrieval, avaliação contínua,
   arquiteturas de produção, casos reais de falha.
4. Nomes de arquivo: `NNN-slug.md`.
5. Ao final, rode `python -m pytest tests/ -q` e valide um `--dry-run`; depois commite
   com a mensagem `content: +N posts na fila`.
