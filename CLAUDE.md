# linkedin-rag-content

Pipeline automático e gratuito de posts técnicos sobre RAG no LinkedIn:
fila de conteúdo versionada → imagem renderizada com Pillow → publicação via
LinkedIn Posts API (ou draft em issue), agendado por GitHub Actions 3x/semana.

## Índice de contexto (tudo vive em docs/)

- PRD: `docs/prd.md`
- HLD do domínio: `docs/domains/content-pipeline/hld.md`
- FDD da feature 1: `docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`
- Diagramas: `docs/domains/content-pipeline/diagrams/mermaid/`
- ADRs: `docs/adrs/generated/CONTENT-PIPELINE/`
- Guidelines Python: `docs/guidelines/python.md`
- Pesquisa (LinkedIn API / Napkin): `docs/research/linkedin-napkin-apis.md`
- Gitflow: `docs/gitflow.md` · Config DD: `docs/dd.md`
- Runbook de operação (tokens, troubleshooting): `docs/operations/runbook.md`

## Comandos

- Testes: `python -m pytest tests/ -q`
- Rodar pipeline local (draft): `python -m linkedin_pipeline.run --dry-run` (a partir de `src/`, ou `PYTHONPATH=src`)
- Gerar novos posts para a fila: seguir `scripts/PROMPT_GERACAO.md`

## Regras do projeto

- Custo zero é requisito: nenhuma dependência paga em runtime.
- Posts da fila: markdown com frontmatter YAML em `content/queue/NNN-slug.md`;
  publicados vão para `content/published/`.
- Idioma do conteúdo e docs: português brasileiro.
