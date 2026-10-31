# Working in this repository

Instructions for humans and AI agents working on GraphEA. Read
[principles](docs/principles.md), [design rules](docs/design-rules.md)
and [architecture](docs/architecture.md) first.

## Every session

- Before starting any work, fetch and sync with `origin/main`. Never
  assume the local copy is current; commits happen outside any one
  session.
- Work only within this repository.

## Interactive sessions

The curator designs; agents work as pair programmers.

- Challenge ideas and assumptions; give honest critique and a
  recommendation.
- Ask when something is unclear. Never guess.
- Create or change files only when the curator says "go".
- Propose documentation changes in conversation first.
- Explain every step taken.
- End with clear recommended next steps.

## Unattended agents

Scheduled or unattended agents can't receive approval during a run, so
they are bounded by their write boundary:

- Write only to `data/silver/extract/`.
- Never create IDs, and never write to `data/silver/reviewed/`.
- Do only the task they were given.
- Push only branches named `auto/<task>`. CI fails any `auto/` or bot
  pull request that changes `data/silver/reviewed/` or `data/bronze/`. This
  enforces the convention; it can't tell sessions apart on the same
  account.

## Write boundaries (all sessions)

- Never edit `data/bronze/` files; only add new items with manifests.
- Never hand-edit `data/silver/text/` or `data/silver/extract/`.
  Change the pipeline or the upstream data instead.
- Only directed sessions write to `data/silver/reviewed/`.
- Never edit the Neo4j graph by hand; change silver and reload.
- Every Neo4j query must be scoped to `:GraphEA` nodes and
  `graphea_*` indexes; the database is shared with another
  knowledge base (ADR-0025).
- Neo4j credentials live in a git-ignored `.env` file, never in the
  repository.

## GitHub

- Every pull request links to an issue, including documentation changes.
- Code changes require an issue and a pull request.
- Documentation changes are grouped into issues and pull requests when
  the curator decides.
- Ask before creating issues or pull requests, or changing anything on
  GitHub.
- Agents never approve or merge pull requests. The curator reviews and
  merges.
- Issues get the `backlog` label only when the curator grooms them,
  not when they are created.

## Testing

- Run `python3 -m pytest` before committing. Don't commit changes
  that break tests.
- CI runs the tests on every pull request and push to `main`.

## Decisions

Record knowledge base design decisions as ADRs in `docs/decisions/`,
using the [template](docs/decisions/template.md). Working conventions
belong in this file, not in ADRs.
