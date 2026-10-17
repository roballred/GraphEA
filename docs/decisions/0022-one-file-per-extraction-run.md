# 0022. One file per extraction run

- **Status:** Accepted
- **Date:** 2026-10-17
- **Partly supersedes:** [0006](0006-one-file-per-record.md)

## Context

ADR-0006 stores one record per file in every layer. In
`data/extracted/` the unit of work is the run (ADR-0012), and runs are
kept to be compared. Spreading a run across many files makes that
harder.

## Decision

- Each extraction run is one JSON document in `data/extracted/runs/`,
  named `run-<first 16 hex digits of the run key hash>.json`.
- It contains the run key components, the prompt text, the creation
  time, and all proposed nodes and edges.
- It is validated by `schemas/proposals/run.schema.json`. Each proposal
  is also validated against its proposal type schema by the build.
- `data/curated/` stays one file per record (ADR-0006).

This replaces ADR-0006 for `data/extracted/`. The rest of ADR-0006
stands.

## Consequences

- A run can be compared with another as a single file diff.
- Proposals have no files of their own; they are referred to by run and
  position.

## Alternatives considered

- **One file per proposal:** consistent with curated records, but hard
  to compare as runs.
