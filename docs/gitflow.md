# Gitflow

Solo project with CI automation that also commits. Simple flow:

- Main branch: `main`. It is the published branch and the one the cron runs against.
- Substantial human work: short-lived `feat/<name>` branch → PR → merge into `main`.
  Small changes (content queue, docs) may go straight to `main`.
- The publish workflow commits to `main` (moves the post from `content/queue/` to
  `content/published/` and saves the image to `out/`). Message:
  `publish(<mode>): <id> <title>`.
- Never rewrite `main`'s history (the bot depends on fast-forward).
