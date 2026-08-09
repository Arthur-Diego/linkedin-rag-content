# ADR-001 — Agendador: GitHub Actions cron

- Status: aceito (2026-08-09, modo autônomo)
- Domínio: CONTENT-PIPELINE

## Contexto

O pipeline precisa rodar 3x/semana sem servidor próprio e sem custo (PRD).

## Decisão

Usar **GitHub Actions** com `schedule` (cron seg/qua/sex 11:30 UTC ≈ 08:30 BRT) e
`workflow_dispatch` para execução manual, em **repositório público** (minutos
ilimitados de Actions).

## Alternativas consideradas

- **Cron em máquina local (WSL2)** — rejeitada: máquina precisa estar ligada; frágil.
- **Cloud scheduler (AWS/GCP)** — rejeitada: exige conta cloud, cartão e infraestrutura
  para um job de 1 minuto.
- **Rotinas agendadas do Claude Code (cloud)** — rejeitada como agendador primário:
  acopla a publicação à conta Claude; Actions é mais simples de observar e depurar.

## Consequências

- Cron do GitHub é best-effort (atrasos de minutos) — aceitável para rede social.
- O workflow precisa de `permissions: contents: write, issues: write` para commitar
  o resultado e abrir issues.
- Repo público expõe a fila de posts futuros — aceito (conteúdo será público de
  qualquer forma).
