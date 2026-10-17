# 0012. Key and keep every extraction run

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

LLM output varies between runs on the same input. Re-running extraction
on unchanged documents produces different proposals, creates diff noise,
makes the curator re-review settled material, and costs money for
nothing new.

## Decision

Each extraction run on a document is identified by a run key built from
everything that can change its output:

- the content hash of the converted input
- the hash of the prompt text
- the model ID
- the schema version

Before extracting, the pipeline checks `data/extracted/` for a run with
the same key. If one exists, extraction is skipped. If not, extraction
runs and its output is stored with the key and its components.

Each run stores the prompt text it used. For a scheduled agent this is
its task definition; for a directed session it is the instruction the
curator gave.

Past runs are kept, not overwritten, so runs with different prompts or
models can be compared.

When extraction is run during a directed session, its output still goes
to `data/extracted/` as a pipeline step. Only the curation that follows
writes to `data/curated/` (ADR-0004).

## Consequences

- Re-running extraction on unchanged inputs costs nothing and changes
  nothing.
- New extraction happens only when something meaningful changes: a new
  source, a new converter output, a new prompt, model or schema.
- Prompt changes need no manual version numbers; changing the wording
  changes the hash.
- In directed sessions the conversation shapes the extraction, so the
  stored prompt is a partial record. The curation decision itself is
  recorded in provenance (ADR-0009).
- Retired models can't reproduce old runs; the stored output is the
  record.
- `data/extracted/` grows over time. Pruning old runs is a deliberate,
  separate decision.

## Alternatives considered

- **Always re-extract:** simplest, but noisy, costly and unrepeatable.
- **Overwrite the previous run:** saves space, but loses the ability to
  compare prompt or model changes.
- **Versioned prompt files:** clear for scheduled agents, but directed
  sessions have no stable prompt to version, and manual version numbers
  are easy to forget to update.
