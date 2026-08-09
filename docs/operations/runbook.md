# Runbook — Operação do pipeline

## 1. Obter/renovar o token do LinkedIn (a cada ~50 dias)

1. Acesse https://www.linkedin.com/developers/apps → seu app (crie um, se primeiro
   acesso; exige vincular a uma Company Page — pode criar uma página simples).
2. Aba **Products**: adicione **Share on LinkedIn** e **Sign In with LinkedIn using
   OpenID Connect** (aprovação instantânea).
3. Aba **Auth** → role até **OAuth 2.0 tools** → **Token Generator**: selecione os
   scopes `openid`, `profile`, `w_member_social` → gere o token (validade 60 dias).
4. No repositório GitHub: Settings → Secrets and variables → Actions →
   secret `LINKEDIN_ACCESS_TOKEN` → cole o token.
5. Teste manual: aba Actions → workflow `publish-linkedin` → Run workflow.

> Apps padrão não têm refresh token programático (recurso de parceiros aprovados).
> Renovar manualmente é o caminho suportado. Agende um lembrete (~50 dias).

## 2. Sintomas e correções

| Sintoma | Causa provável | Ação |
|---|---|---|
| Job falha com `LinkedInError 401` | token expirado/ inválido | renovar token (seção 1) |
| Job falha com `LinkedInError 422 CONTENT_DUPLICATE` | legenda idêntica a post recente | editar o post da fila |
| Job falha com `LinkedInError 426/400` citando versão | `LinkedIn-Version` aposentada | atualizar variável `LINKEDIN_VERSION` no workflow para um `YYYYMM` ativo |
| Issue "Fila de conteúdo baixa" | ≤ 2 posts ready | rodar `scripts/PROMPT_GERACAO.md` no Claude Code e commitar novos posts |
| Post não saiu no horário | cron do GitHub é best-effort | conferir aba Actions; disparar manual se necessário |
| Card sem a fonte bonita | DejaVu ausente no runner | não é falha; instalar `fonts-dejavu-core` no workflow |

## 3. Publicar manualmente um draft

Modo draft (sem token): a issue traz a legenda pronta e o caminho da imagem em `out/`.
Copie a legenda, baixe a imagem do repositório e poste pelo app do LinkedIn. Depois
mova o arquivo do post de `content/queue/` para `content/published/` mudando
`status: published` (ou rode o pipeline com token configurado, que faz isso sozinho).

## 4. Alterar horário/frequência

Editar o cron em `.github/workflows/publish.yml` (UTC). Padrão:
`30 11 * * 1,3,5` = seg/qua/sex 08:30 BRT.
