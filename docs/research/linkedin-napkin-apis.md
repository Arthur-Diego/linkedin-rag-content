# Pesquisa — LinkedIn API e Napkin AI (2026-08-09)

> Pesquisa direcionada (formato reduzido; o tema não justificou Deep Research de 16
> seções — decisão por regra do Passo 2 do dd-greenfield). Alimenta o HLD e os ADRs.

## LinkedIn — publicar no perfil pessoal

- **Gratuito e self-serve**: criar app em https://www.linkedin.com/developers/apps
  (exige associar a uma Company Page), adicionar os produtos **"Share on LinkedIn"**
  (dá `w_member_social`) e **"Sign In with LinkedIn using OpenID Connect"**
  (dá `openid profile`, necessários para `GET /v2/userinfo` → campo `sub` → autor
  `urn:li:person:{sub}`).
- **API atual (versionada)**: `POST https://api.linkedin.com/rest/posts` com headers
  `LinkedIn-Version: YYYYMM` (versões mensais expiram — manter parametrizada),
  `X-Restli-Protocol-Version: 2.0.0`. Sucesso: `201` + id no header `x-restli-id`.
- **Imagem**: `POST /rest/images?action=initializeUpload` com
  `{"initializeUploadRequest": {"owner": "urn:li:person:{sub}"}}` → resposta traz
  `uploadUrl` (PUT do binário com Bearer) e `image` (`urn:li:image:...`) que vai em
  `content.media.id` do post. PNG/JPG/GIF.
- **Token**: validade **60 dias**; apps padrão **não têm refresh token** (exclusivo de
  parceiros aprovados). Renovação: repetir OAuth no navegador ou usar o **Token
  Generator** do Developer Portal (OAuth Tools) — caminho recomendado para uso pessoal.
- **Rate limit**: 150 requests/dia por membro — irrelevante para 3 posts/semana.
  Atenção a `CONTENT_DUPLICATE` (LinkedIn rejeita post idêntico repetido).
- Payload mínimo de post pessoal com imagem: ver FDD seção 5.

Fontes: learn.microsoft.com/linkedin (share-on-linkedin, posts-api view=li-lms-2026-06,
images-api, authorization-code-flow, programmatic-refresh-tokens, rate-limits).

## Napkin AI

- API existe (developer preview, token em app.napkin.ai → Settings → Developers), mas
  **consome créditos pagos** da conta (free ≈ 3 visuais; planos US$9–22/mês).
- **Veredicto: incompatível com o requisito de custo zero** → substituída por
  renderização local com Pillow (ADR-003).

## Alternativas gratuitas de imagem avaliadas

| Opção | Prós | Contras |
|---|---|---|
| **Pillow (escolhida)** | leve, offline, ilimitada, rápida no CI | layout manual, visual mais simples |
| HTML→PNG (Playwright) | CSS completo, visual rico | ~300 MB de browser no runner, lento |
| QuickChart/Kroki | diagramas prontos via HTTP | dependência de serviço externo, limites no hosted |
