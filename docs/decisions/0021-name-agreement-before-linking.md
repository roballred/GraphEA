# 0021. Require name agreement before auto-linking

- **Status:** Accepted
- **Date:** 2026-10-17
- **Supersedes:** [0008](0008-entity-resolution-tiers.md)

## Context

ADR-0008 tier 1 links an extracted entity whenever it names an existing
ID. Readable IDs are easy for a model to produce; an ID in model output
is not evidence that the text is about that record.

## Decision

Extracted entities are matched to curated records in four tiers:

| Tier | Match | Result |
|---|---|---|
| 1 | Names an existing ID, and its normalized name matches that record's `name` or an alias | Linked |
| 2 | Its normalized name exactly matches one record's `name` or alias | Linked |
| 3 | Names an existing ID whose name doesn't agree; a likely match by fuzzy or LLM judgment; or a name shared by more than one record | Candidate match, for the curator to decide |
| 4 | No match | Proposed new entity, for the curator to decide |

- Normalization: lowercase, collapse whitespace, remove punctuation.
- Pipelines never create IDs. IDs are created only when the curator
  accepts a proposed entity in a directed session (ADR-0004, ADR-0007).
- All tiers write their results to `data/extracted/`. Links made in
  tiers 1–2 are still proposals until the curated layer uses them.
- When the curator rejects a candidate match, the rejection is recorded
  on the curated record as `distinctFrom`, and that pair is not proposed
  again.

## Consequences

- A hallucinated ID becomes a candidate for review, not a confident link.
- Slightly more tier 3 work for the curator.
- Alias quality still drives how much matching is automatic.

## Alternatives considered

- **Keep ADR-0008 tier 1:** trusts IDs that a model produced.
- **Fully automatic matching:** fast, but wrong merges are hard to
  notice and undo.
