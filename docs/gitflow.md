# Gitflow

Projeto solo com automação de CI que também commita. Fluxo simples:

- Branch principal: `main`. É a branch publicada e a que o cron executa.
- Trabalho humano relevante: branch curta `feat/<nome>` → PR → merge em `main`.
  Ajustes pequenos (fila de conteúdo, docs) podem ir direto em `main`.
- O workflow de publicação commita em `main` (move post de `content/queue/` para
  `content/published/` e salva a imagem em `out/`). Mensagem: `publish: <id> <título>`.
- Nunca reescrever histórico de `main` (o bot depende de fast-forward).
