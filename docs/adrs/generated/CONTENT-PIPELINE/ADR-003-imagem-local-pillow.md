# ADR-003 — Imagem: renderização local com Pillow (não Napkin AI)

- Status: aceito (2026-08-09, modo autônomo)
- Domínio: CONTENT-PIPELINE

## Contexto

O plano original usava a Napkin AI API para gerar o visual. A pesquisa
(`docs/research/linkedin-napkin-apis.md`) mostrou que a API da Napkin está em
developer preview e **consome créditos pagos** (free ≈ 3 visuais; planos US$9–22/mês)
— incompatível com custo zero em automação contínua.

## Decisão

Renderizar localmente um **card PNG 1200×1350** (proporção 4:5, ideal para feed) com
**Pillow**: fundo em gradiente escuro, chip do tema, título grande, bullets e rodapé de
branding. Cada post declara `image.headline` e `image.bullets` no frontmatter.

## Alternativas consideradas

- **Napkin AI API** — rejeitada: custo em créditos.
- **HTML→PNG via Playwright** — rejeitada: ~300 MB de browser no runner e mais lentidão
  para ganho estético marginal; possível evolução futura.
- **QuickChart/Kroki (hosted)** — rejeitada como padrão: dependência de serviço externo
  com limites; estética de diagrama, não de card social.

## Consequências

- Visual consistente e de marca própria, porém mais simples que ilustrações de IA.
- Zero dependência externa: renderização roda offline e em qualquer runner.
- Fonte tipográfica: DejaVu (presente no runner Ubuntu); fallback para fonte default
  do Pillow.
