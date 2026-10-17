# 0004. Every file has exactly one owner

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

When a pipeline and a person both write to the same file, the next
pipeline run overwrites the person's edits. Workarounds that keep them in
one file (protected regions, merging regenerated output with edits) are
fragile and fail silently.

GraphEA has two kinds of writers: unattended pipelines and agents running
on a schedule, and directed sessions where the curator works with an AI.

## Decision

Each layer has exactly one kind of writer:

| Layer | Owner |
|---|---|
| `data/raw/` | The curator, adding new material only |
| `data/converted/` | Conversion pipelines |
| `data/extracted/` | Extraction pipelines and agents |
| `data/curated/` | Directed sessions only |
| `data/published/` | The build |

Ownership is defined by how the work happens, not by who or what does it.
An AI working in a directed session may write to `data/curated/`; the
same AI running unattended may not.

No pipeline ever writes to `data/curated/`. No directed session
hand-edits `data/converted/`, `data/extracted/` or `data/published/`; to
change those, change the pipeline or the upstream data.

## Consequences

- Re-running any pipeline is always safe for curated work.
- Corrections to LLM output are recorded in `data/curated/`, not made in
  `data/extracted/`, so the original proposal stays visible.
- Every pipeline and agent must be configured to know its write
  boundary. That boundary is stated in AGENTS.md.
- Whether a session is directed or unattended must be clear and recorded
  in each curated record's provenance.

## Alternatives considered

- **Protected regions inside generated files:** break when the generated
  structure changes, and edits outside the markers are silently lost.
- **Generate once, then hand over to humans:** curated content drifts
  from its sources with no way to detect it.
- **Three-way merging of regenerated output with edits:** workable for
  code, but LLM output changes on every run, so conflicts never end.
