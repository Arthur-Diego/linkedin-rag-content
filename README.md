# linkedin-rag-content

Pipeline **100% gratuito** que publica posts técnicos sobre RAG no LinkedIn,
3x por semana, sem intervenção manual.

```
GitHub Actions (cron seg/qua/sex)
   └─► próximo post da fila (content/queue/*.md)
         └─► card PNG renderizado localmente (Pillow)
               └─► LinkedIn Posts API (com token)
                   ou issue com o post pronto (sem token)
```

- **Custo zero**: Actions em repo público + API oficial gratuita do LinkedIn +
  imagem renderizada localmente (sem Napkin/DALL-E).
- **Estado no git**: fila em `content/queue/`, histórico em `content/published/`,
  imagens em `out/`. Sem banco, sem servidor.
- **Conteúdo**: pré-gerado pelo Claude Code e revisável antes de ir ao ar; a fila
  já vem com 9 posts (~3 semanas).

## Como usar

### Já funciona hoje (modo draft, sem configurar nada)

O workflow roda seg/qua/sex 08:30 BRT (ou manualmente em **Actions →
publish-linkedin → Run workflow**). Sem token configurado, ele:

1. Renderiza a imagem do próximo post e commita em `out/`.
2. Abre uma **issue** com a legenda pronta para colar no LinkedIn.

Publique manualmente a partir da issue enquanto não configura o token.

### Publicação automática (setup único, ~15 min)

1. Crie um app em https://www.linkedin.com/developers/apps (exige vincular a uma
   Company Page — pode criar uma página simples só para isso).
2. Na aba **Products**, adicione **Share on LinkedIn** e **Sign In with LinkedIn
   using OpenID Connect** (aprovação instantânea).
3. Na aba **Auth → OAuth 2.0 tools → Token Generator**, gere um token com os scopes
   `openid`, `profile` e `w_member_social` (validade: 60 dias).
4. No GitHub: **Settings → Secrets and variables → Actions → New repository secret**
   → nome `LINKEDIN_ACCESS_TOKEN`, valor = o token.
5. Teste: **Actions → publish-linkedin → Run workflow**. O post sai no seu perfil e
   o arquivo move para `content/published/`.

> O token expira em ~60 dias (LinkedIn não dá refresh automático para apps padrão).
> Renove no Token Generator e atualize o secret — o runbook
> (`docs/operations/runbook.md`) detalha isso e outros problemas comuns.

### Reabastecer a fila de posts

Quando a issue **"Fila de conteúdo baixa"** aparecer, abra o Claude Code neste
repositório e siga `scripts/PROMPT_GERACAO.md` — ele gera novos posts no formato
certo usando sua assinatura (sem custo de API).

### Rodar localmente

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
PYTHONPATH=src .venv/bin/python -m linkedin_pipeline.run --dry-run   # gera out/ sem publicar
.venv/bin/python -m pytest tests/ -q                                 # testes
```

## Formato de um post

`content/queue/NNN-slug.md`:

```markdown
---
id: "010"
topic: nome do tema
title: "Título interno"
image:
  headline: "Título do card"
  bullets:
    - "ponto 1"
    - "ponto 2"
    - "ponto 3"
alt_text: "descrição da imagem"
status: ready
---
Legenda do LinkedIn com #hashtags no final.
```

Ajustes de horário/frequência: cron em `.github/workflows/publish.yml` (UTC).

## Documentação

Projeto guiado por design docs (fluxo `/dd` greenfield): PRD, HLD, FDD, ADRs,
pesquisa de APIs e runbook em [`docs/`](docs/) — índice em [`CLAUDE.md`](CLAUDE.md).
