# HLD — Domínio content-pipeline

> Aprovado em 2026-08-09 (modo autônomo). Fonte de negócio: `docs/prd.md`.

## 1. Visão

Um job agendado (GitHub Actions, cron seg/qua/sex) consome uma fila de posts
versionada no git, renderiza a imagem do post localmente e publica no LinkedIn.
Não há servidor, banco ou serviço 24/7: **o repositório é o sistema**.

## 2. Arquitetura

```
GitHub Actions (cron 3x/semana ou disparo manual)
  └─ python -m linkedin_pipeline.run
       ├─ queue_store: lê content/queue/, pega o post de menor id
       ├─ renderer:    gera out/<id>.png (Pillow, template de card)
       ├─ linkedin:    com LINKEDIN_ACCESS_TOKEN →
       │                 1. GET  /v2/userinfo            (URN do membro)
       │                 2. POST /rest/images?action=initializeUpload
       │                 3. PUT  <uploadUrl>              (binário do PNG)
       │                 4. POST /rest/posts              (post + imagem)
       │               sem token → modo draft:
       │                 gh issue com legenda pronta + imagem commitada
       ├─ queue_store: move o post para content/published/
       └─ (step do workflow) commit/push do resultado em main
```

## 3. Componentes

| Componente | Responsabilidade | Tecnologia |
|---|---|---|
| Fila de conteúdo | posts pendentes/publicados, formato frontmatter | git (`content/`) |
| `queue_store` | selecionar próximo post, mover para published | Python + PyYAML |
| `renderer` | card PNG 1200×1350 (título, bullets, rodapé) | Pillow |
| `linkedin` | upload de imagem + criação do post (API versionada) | requests |
| `run` | orquestração, CLI (`--dry-run`), modo draft | Python argparse |
| Agendador | cron + `workflow_dispatch` + commit do resultado | GitHub Actions |
| Abastecimento | geração de novos posts com Claude Code (humano no loop) | prompt em `scripts/` |

## 4. Fluxos principais

**Publicação (feliz)**: cron dispara → próximo post da fila → render PNG →
upload imagem → cria post → move para `published/` → commit
`publish(<mode>): <id> <título>` (feito por step do workflow, também no modo draft).

**Draft (sem token)**: mesmos passos de seleção e render; em vez de chamar a API,
abre issue no repositório com a legenda pronta para copiar e o caminho da imagem;
o post permanece na fila (não é consumido) até ser publicado de fato ou movido
manualmente.

**Fila baixa/vazia** (`queue_remaining ≤ 2` ou vazia): job termina com sucesso e abre a
issue `Fila de conteúdo baixa` — apenas se ainda não houver uma aberta — pedindo
reabastecimento (prompt em `scripts/PROMPT_GERACAO.md`).

**Token expirado (~60 dias)**: chamada retorna 401 → job falha com mensagem clara →
runbook `docs/operations/runbook.md` descreve a renovação.

## 5. Contratos externos consumidos

- LinkedIn API versionada (`LinkedIn-Version: 2xxxxx`): `/v2/userinfo`,
  `/rest/images?action=initializeUpload`, `/rest/posts`. Auth: OAuth 2.0 member token
  com scopes `openid profile w_member_social`. Gratuita para publicar no próprio perfil.
- GitHub: `gh` CLI no runner (issues) e git puro para commit/push. Auth: `GITHUB_TOKEN`
  do workflow.

## 6. Decisões estruturais (→ ADRs)

1. Agendador: GitHub Actions cron — ADR-001
2. Conteúdo pré-gerado versionado (sem LLM em runtime) — ADR-002
3. Imagem local com Pillow (não Napkin AI) — ADR-003
4. Publicação: LinkedIn Posts API + modo draft como fallback — ADR-004
5. Estado no git (sem banco) — ADR-005

## 7. Observabilidade e operação

- Log do job = log do GitHub Actions; falha de API derruba o job (visível + e-mail
  do GitHub ao owner).
- Issues do repo como canal de notificação (draft pronto / fila vazia).
- Runbook de tokens e troubleshooting em `docs/operations/runbook.md`.

## 8. Riscos

| Risco | Mitigação |
|---|---|
| Token LinkedIn expira em ~60 dias | falha alta + runbook de renovação; issue lembrete |
| LinkedIn mudar versão da API | `LINKEDIN_VERSION` parametrizada em um só lugar |
| Fila esvaziar sem aviso | issue automática quando restar ≤ 2 posts |
| Cron do GitHub atrasar (best-effort) | tolerável para rede social; `workflow_dispatch` manual |
