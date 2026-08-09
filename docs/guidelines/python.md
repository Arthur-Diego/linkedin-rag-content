# Guideline — Python

> Stack decided in autonomous mode (dd-greenfield gate 2): Python 3.12,
> minimal dependencies, no web framework (there is no server — the "runtime" is a job).

## Stack

| Area | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 | available locally and on the `ubuntu-latest` runner |
| Image | Pillow | local card rendering, zero cost, no external service |
| HTTP | requests | simple client for the LinkedIn REST API |
| Frontmatter | PyYAML | parses the posts' frontmatter |
| Tests | pytest | de facto standard |
| CI/scheduler | GitHub Actions | free cron on a public repo |

No ORM and no database: git itself is the state (queue in `content/queue/`,
history in `content/published/`).

## Conventions

- Code lives in `src/linkedin_pipeline/`, imported as `linkedin_pipeline.*`.
- Small, pure modules: `queue_store` (queue), `renderer` (image),
  `linkedin` (API), `run` (orchestration/CLI).
- I/O functions take paths as parameters (testability); no hardcoded absolute
  paths.
- API errors become exceptions carrying the response body in the message — the
  Actions job fails loudly and the log explains why.
- Secrets only via environment variables (`LINKEDIN_ACCESS_TOKEN`); never in code
  or committed.
- Type hints on public signatures; one-line docstring per module/function.
- Tests: unit tests for the queue and renderer (no network); the LinkedIn API is
  tested with `requests` mocks.
