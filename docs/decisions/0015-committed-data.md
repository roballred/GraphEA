# 0015. Which data is committed to git

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Some layers can be regenerated and some can't. Committing everything
bloats the repository with build output; committing too little loses
history or makes changes invisible. Some raw sources may be large binary
files.

Code, prompts and documentation are committed normally; this ADR covers
the data layers and schemas.

## Decision

| Path | Committed? | Why |
|---|---|---|
| `data/raw/` manifests | Always | The record of what arrived and from where |
| `data/raw/` source files | Decided per source: git, Git LFS, or external storage referenced by the manifest | Large binaries don't suit plain git |
| `data/converted/` | Yes | Rebuildable, but converter changes become reviewable diffs |
| `data/extracted/` | Yes | Runs can't be reproduced exactly (ADR-0012) |
| `data/curated/` | Yes | The record of human decisions |
| `data/published/` | No (gitignored) | Pure build output |
| `schemas/` | Yes | The contract for every record |

## Consequences

- Everything that can't be regenerated is in git history.
- Consumers must run the build to get `data/published/`; nothing
  published is in the repo.
- Raw files kept outside git must have a manifest with a location and
  hash, so the repo still records exactly what was used.

## Alternatives considered

- **Commit everything, including `data/published/`:** consumers could
  read the repo directly, but every build produces large, noisy diffs.
- **Commit only `data/raw/` and `data/curated/`:** smallest repository,
  but converter changes and extraction history become invisible.
