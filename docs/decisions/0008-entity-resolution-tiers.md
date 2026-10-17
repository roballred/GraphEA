# 0008. Match extracted entities to existing records in tiers

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

The same real-world thing appears under different names across sources
("WaTech", "Washington Technology Solutions"). Without a matching rule,
each extraction run creates duplicates. Matching too eagerly is also
harmful: related but distinct things (WaTech and the OCIO, an office
within it) get merged.

## Decision

Extracted entities are matched to curated records in four tiers:

| Tier | Match | Result |
|---|---|---|
| 1 | The extracted entity names an existing ID | Linked |
| 2 | Its name exactly matches one record's `name` or alias, after normalization | Linked |
| 3 | A likely match by fuzzy or LLM judgment, or a name shared by more than one record | Candidate match with a confidence score, for the curator to decide |
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

- Duplicates are prevented without merging distinct things
  automatically.
- The quality of the alias lists drives how much matching is automatic.
  Careless aliases cause wrong merges.
- Tier 3 volume depends on how varied the source naming is; it is the
  main cost of curation.

## Alternatives considered

- **Fully automatic matching:** fast, but wrong merges are hard to
  notice and undo.
- **Match on IDs only:** every new source spelling becomes a duplicate.
