# AGENTS

Guia para agentes de IA trabalhando neste repositório. O índice completo de contexto
está em `CLAUDE.md` — leia-o primeiro; todo contexto vive em `docs/`.

Regras essenciais:
- Custo zero em runtime (sem APIs pagas).
- Não reescrever histórico de `main` (o bot de publicação commita nela).
- Novos posts seguem o formato frontmatter descrito no FDD
  (`docs/domains/content-pipeline/features/001-pipeline-publicacao-fdd.md`).
- Validar com `python -m pytest tests/ -q` antes de finalizar.
