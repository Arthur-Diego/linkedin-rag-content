# ADR-002 — Conteúdo pré-gerado e versionado (sem LLM em runtime)

- Status: aceito (2026-08-09, modo autônomo)
- Domínio: CONTENT-PIPELINE

## Contexto

O plano original previa o Claude gerando o conteúdo dentro do job agendado. Chamar um
LLM em runtime no CI exige API key da Anthropic (custo por token) ou integração do
Claude Code Action com OAuth — mais partes móveis e custo potencial, contra o
requisito de custo zero.

## Decisão

Manter uma **fila de posts pré-gerados** (`content/queue/NNN-slug.md`, markdown com
frontmatter YAML) escrita pelo Claude Code **localmente, na conta do owner** (custo já
coberto pela assinatura). O job agendado apenas consome a fila. O reabastecimento é
guiado pelo prompt oficial em `scripts/PROMPT_GERACAO.md`, e uma issue automática avisa
quando restarem ≤ 2 posts.

## Alternativas consideradas

- **Claude API no CI** — rejeitada: custo por execução.
- **claude-code-action com token OAuth no CI** — rejeitada por ora: configuração
  adicional e dependência de credencial sensível no repo; pode virar evolução futura.
- **Templates estáticos sem LLM** — rejeitada: qualidade de conteúdo insuficiente.

## Consequências

- Humano no loop a cada ~3 semanas (rodar o prompt de reabastecimento) — aceitável.
- Qualidade revisável: os posts ficam em PR/commit antes de irem ao ar.
- O pipeline em si é 100% determinístico e testável.
