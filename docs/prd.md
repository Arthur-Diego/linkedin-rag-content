# PRD — Pipeline automático de conteúdo LinkedIn sobre RAG

> Aprovado em 2026-08-09 (modo autônomo delegado pelo owner).

## Problema

Manter presença técnica consistente no LinkedIn exige escrever posts de qualidade
várias vezes por semana — pesquisa do tema, texto, imagem e publicação no horário
certo. Feito manualmente, o processo é irregular e acaba abandonado.

## Usuários

- **Owner** (Arthur Diego): único usuário. Quer publicar 3x/semana conteúdo técnico
  sobre RAG (Retrieval-Augmented Generation) no perfil pessoal, com esforço próximo
  de zero e custo zero.

## Objetivo

Pipeline 100% automático e gratuito que, 3x por semana:
1. Seleciona o próximo post de uma fila de conteúdo sobre RAG.
2. Renderiza uma imagem de card técnico para o post.
3. Publica no LinkedIn via API oficial (ou, sem token configurado, entrega o post
   pronto como rascunho em uma issue do GitHub).

## Escopo

- Fila de posts versionada no git (markdown + frontmatter), pré-gerada pelo Claude Code.
- Renderização local de imagem (Pillow) — card com título e bullets.
- Publicação no perfil pessoal via LinkedIn Posts API (`w_member_social`).
- Agendamento via GitHub Actions cron (seg/qua/sex).
- Modo draft (fallback sem token): artefatos em `out/` + issue no GitHub.
- Reabastecimento da fila: prompt documentado para gerar novos posts com Claude Code.

## Fora de escopo

- Múltiplas redes sociais; páginas de empresa no LinkedIn.
- Analytics de engajamento.
- Geração de imagem por IA paga (Napkin AI, DALL-E etc.).
- Interface web/painel.

## Resultado esperado

A partir de hoje, com a fila abastecida (~3 semanas de conteúdo), o LinkedIn do owner
recebe 3 posts técnicos por semana sem intervenção manual — custo financeiro zero
(GitHub Actions em repo público + API gratuita do LinkedIn).
