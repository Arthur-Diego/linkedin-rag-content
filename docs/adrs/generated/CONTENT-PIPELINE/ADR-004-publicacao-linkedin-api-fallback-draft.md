# ADR-004 — Publicação: LinkedIn Posts API com modo draft como fallback

- Status: aceito (2026-08-09, modo autônomo)
- Domínio: CONTENT-PIPELINE

## Contexto

Publicar exige a API oficial do LinkedIn (gratuita, mas com setup manual: app no
Developer Portal + token OAuth de 60 dias sem refresh programático para apps padrão).
O sistema precisa ser útil hoje, antes desse setup.

## Decisão

Publicar via **LinkedIn Posts API versionada** (`/rest/posts` + `/rest/images`,
header `LinkedIn-Version` parametrizado) quando `LINKEDIN_ACCESS_TOKEN` estiver
configurado como secret. **Sem token, operar em modo draft**: renderiza a imagem,
commita em `out/` e abre uma issue no GitHub com a legenda pronta para colar —
o post continua na fila.

## Alternativas consideradas

- **Agendadores third-party (Buffer etc.)** — rejeitada: free tiers limitados,
  credencial de terceiros, menos controle.
- **Automação de browser (selenium) no LinkedIn** — rejeitada: viola ToS, risco de
  bloqueio da conta.
- **Somente draft (sem API)** — rejeitada como estado final: não atende "automático".

## Consequências

- Setup único documentado no runbook (`docs/operations/runbook.md`); renovação de
  token a cada ~50 dias via Token Generator do Developer Portal.
- Token 401/expirado derruba o job com erro claro; issue de lembrete é aberta.
- O mesmo código serve aos dois modos — o draft é o caminho de degradação natural.
