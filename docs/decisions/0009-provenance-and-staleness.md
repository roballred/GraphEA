# 0009. Record provenance and detect stale records

- **Status:** Superseded by [0023](0023-evidence-claims-and-provenance.md)
- **Date:** 2026-10-17

## Context

A curated record is only as trustworthy as its source. When a source is
updated, records based on the old version may now be wrong. Applying
them blindly spreads errors; dropping them silently loses curated work.

Because `data/raw/` is add-only (ADR-0003), a source is never changed in
place. An updated source arrives as a new raw item that supersedes the
old one.

## Decision

Every curated node and edge has a `provenance` block containing:

- `sources`: the raw items it is based on, each with its content hash.
- `extractionRun`: the run key of the proposal it came from, if any
  (ADR-0012).
- `session`: `directed`, the only kind allowed to write curated records
  (ADR-0004).
- `createdAt`: when the record was created.
- `updatedAt`: when the record last changed.

`sources` is required for records with origin `documented` or
`observed`, and is empty for `synthetic` records (ADR-0010).

Pipeline-set provenance fields and `createdAt` are read-only (ADR-0005).

A record is stale when any raw item in its `sources` has been
superseded. The build does not drop or block stale records. It publishes
them marked `stale`, and it produces a report listing every stale record
and the newer source to review against.

## Consequences

- Every published fact can be traced back to an exact source file.
- Source updates lead to review instead of silent drift or silent loss.
- The build never edits curated records (ADR-0004). Clearing staleness
  means a directed session updates the record's sources.
- Raw manifests must record what each item supersedes.

## Alternatives considered

- **Block publishing of stale records:** safest, but one updated
  source could remove large parts of the graph.
- **Ignore source changes:** simplest, but curated content drifts from
  reality with no warning.
- **Track only source URLs, not hashes:** the content at a URL can change
  without warning.
