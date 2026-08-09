# FDD 001 — Pipeline de publicação automática

> Aprovado em 2026-08-09 (modo autônomo). Terreno: `../hld.md`, `docs/prd.md`,
> ADRs 001–005.

## 1. Objetivo

Job que, a cada disparo do agendador, publica no LinkedIn o próximo post da fila
(texto + imagem renderizada) ou, sem token, entrega o post pronto como draft.

## 2. Formato do post na fila

`content/queue/NNN-slug.md` — markdown com frontmatter YAML:

```yaml
---
id: "001"                # ordena a fila (menor primeiro)
topic: chunking          # chip exibido no card
title: "Título interno"
image:
  headline: "Título do card (curto)"
  bullets:
    - "linha 1"
    - "linha 2"
    - "linha 3"
alt_text: "descrição da imagem para acessibilidade"
status: ready            # ready | published
---
Corpo da legenda do LinkedIn (com hashtags no final).
```

Ao publicar: frontmatter ganha `status: published`, `published_at` (ISO-8601 UTC) e
`linkedin_post_id`; arquivo move para `content/published/`.

## 3. Módulos

| Módulo | Função pública | Comportamento |
|---|---|---|
| `queue_store` | `next_post(root)` | menor `id` com `status: ready`; `None` se vazia |
| | `count_ready(root)` | posts restantes na fila |
| | `mark_published(root, post, post_id)` | atualiza frontmatter + move para published/ |
| `renderer` | `render_card(post, out_path)` | PNG 1200×1350, gradiente, chip, headline, bullets, rodapé |
| `linkedin` | `publish(token, version, caption, image_path, alt_text)` | userinfo → initializeUpload → PUT binário → POST /rest/posts; retorna id |
| `run` | CLI `python -m linkedin_pipeline.run [--dry-run] [--root PATH]` | orquestra e emite outputs p/ GitHub Actions |

## 4. Fluxo do `run`

1. `next_post` — fila vazia → loga `QUEUE_EMPTY`, output `queue_empty=true`, exit 0.
2. `render_card` → `out/<id>.png`; legenda → `out/<id>-caption.txt`.
3. `--dry-run` → para aqui (nada de API, nada de move).
4. `LINKEDIN_ACCESS_TOKEN` presente → `linkedin.publish` → `mark_published` →
   output `mode=published`.
5. Sem token → output `mode=draft` (post NÃO sai da fila; artefatos commitados pelo
   workflow e issue aberta com a legenda).
6. Sempre: output `queue_remaining=<n>` (workflow abre issue de reabastecimento se ≤ 2).

## 5. Contrato externo consumido (LinkedIn, API versionada)

- `GET /v2/userinfo` → `sub` → autor `urn:li:person:{sub}`.
- `POST /rest/images?action=initializeUpload` body
  `{"initializeUploadRequest":{"owner":"<author>"}}` → `uploadUrl` + `image` URN.
- `PUT <uploadUrl>` com binário PNG e `Authorization: Bearer`.
- `POST /rest/posts` (201 + header `x-restli-id`):

```json
{
  "author": "urn:li:person:{sub}",
  "commentary": "<legenda com caracteres reservados escapados>",
  "visibility": "PUBLIC",
  "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                    "thirdPartyDistributionChannels": []},
  "content": {"media": {"altText": "<alt_text>", "id": "urn:li:image:..."}},
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

- Headers: `LinkedIn-Version: <LINKEDIN_VERSION, default 202606>`,
  `X-Restli-Protocol-Version: 2.0.0`.
- Escape do commentary (formato little-text): prefixar `\` em
  `\ | { } [ ] ( ) < > * _ ~` — `#` e `@` ficam intactos (hashtags/menções).

## 6. Matriz de erros

| Cenário | Comportamento |
|---|---|
| Fila vazia | exit 0, `queue_empty=true`, issue de reabastecimento |
| HTTP ≠ 2xx em qualquer chamada LinkedIn | `LinkedInError` com status + corpo; job falha (visível no Actions) |
| 401 (token expirado) | idem acima; runbook orienta renovação |
| Frontmatter inválido no post | `ValueError` nomeando o arquivo; job falha |
| Fonte DejaVu ausente | fallback para fonte default do Pillow (degrada estética, não falha) |
| Post duplicado (`CONTENT_DUPLICATE`) | job falha; operador remove/edita o post da fila |

## 7. Critérios de aceite

1. `--dry-run` com fila abastecida gera PNG + caption em `out/` e não altera a fila.
2. Sem token e sem `--dry-run`, outputs indicam `mode=draft` e a fila não é consumida.
3. Com token (mock nos testes), o payload enviado bate com a seção 5 e o post move
   para `content/published/` com `published_at` e `linkedin_post_id`.
4. Fila vazia encerra com exit 0 e `queue_empty=true`.
5. `pytest` verde cobrindo fila, renderer e cliente LinkedIn (mockado).

## 8. Observabilidade

Logs no stdout do job; outputs estruturados via `$GITHUB_OUTPUT`; issues como canal de
notificação. Sem métricas adicionais (escala de 3 execuções/semana).
