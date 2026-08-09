# ADR-005 — Estado no git (sem banco de dados)

- Status: aceito (2026-08-09, modo autônomo)
- Domínio: CONTENT-PIPELINE

## Contexto

O sistema precisa saber quais posts estão pendentes e quais já foram publicados.
Qualquer banco/storage externo (S3, DynamoDB, SQLite hospedado) adiciona custo ou
infraestrutura para um estado minúsculo.

## Decisão

O **repositório git é o único storage**: `content/queue/` = pendentes,
`content/published/` = histórico (com `published_at` e id do post no frontmatter),
`out/` = imagens geradas. O job do Actions commita a transição em `main`
(`publish: <id> <título>`).

## Alternativas consideradas

- **S3/GCS** — rejeitada: conta cloud e custo para bytes de estado.
- **SQLite no repo** — rejeitada: binário em git dificulta diff/review; markdown é
  legível e editável.
- **GitHub Releases/Artifacts como storage** — rejeitada: artefatos expiram e não são
  fonte de verdade auditável.

## Consequências

- Histórico completo e auditável por `git log`.
- Concorrência é um não-problema (um job por vez; `concurrency` no workflow garante).
- `main` não pode ser reescrita (dependência do fast-forward do bot) — regra no
  `docs/gitflow.md`.
