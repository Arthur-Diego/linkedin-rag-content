# Guideline — Python

> Stack decidida em modo autônomo (gate 2 do dd-greenfield): Python 3.12,
> dependências mínimas, sem framework web (não há servidor — o "runtime" é um job).

## Stack

| Área | Escolha | Motivo |
|---|---|---|
| Linguagem | Python 3.12 | disponível no ambiente e no runner `ubuntu-latest` |
| Imagem | Pillow | render local de cards, zero custo, sem serviço externo |
| HTTP | requests | cliente simples para a API REST do LinkedIn |
| Frontmatter | PyYAML | parse do frontmatter dos posts |
| Testes | pytest | padrão de facto |
| CI/agendador | GitHub Actions | cron gratuito em repo público |

Sem ORM e sem banco: o estado é o próprio git (fila em `content/queue/`,
histórico em `content/published/`).

## Convenções

- Código em `src/linkedin_pipeline/`, importado como `linkedin_pipeline.*`.
- Módulos pequenos e puros: `queue_store` (fila), `renderer` (imagem),
  `linkedin` (API), `run` (orquestração/CLI).
- Funções de I/O recebem caminhos por parâmetro (testabilidade); nada de caminho
  absoluto hardcoded.
- Erros de API viram exceção com corpo da resposta no texto — o job do Actions
  falha alto e o log conta o porquê.
- Segredos só via variáveis de ambiente (`LINKEDIN_ACCESS_TOKEN`); nunca em código
  ou committed.
- Type hints em assinaturas públicas; docstring de uma linha por módulo/função.
- Testes: unitários para fila e renderer (sem rede); API do LinkedIn testada com
  mocks de `requests`.
