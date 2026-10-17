# 0023. Evidence, claims and provenance

- **Status:** Accepted
- **Date:** 2026-10-17
- **Supersedes:** [0009](0009-provenance-and-staleness.md)

## Context

ADR-0009 gives a record one list of sources, and detects staleness only
when a raw item is superseded. A record's properties can come from
different sources; evidence can't point to where in a source a fact
appears; a converter change leaves curated records unflagged; and
`session: directed` is a constant that records nothing.

## Decision

Every curated node and edge has a `provenance` block:

- `evidence`: a list of evidence items, each with
  - `key`: a short local label (e.g. `e1`), unique within the record
  - `rawItem` and `rawHash`: the exact source file
  - `convertedHash`: the exact conversion it was read from, when it came
    through conversion
  - `locator` (optional): any of `page`, `section`, `table`, and a
    `quote` of up to 300 characters
- `claims` (optional): per-property overrides, keyed by property name.
  A claim names its supporting `evidence` keys and may override
  `origin`. Without a claim, a property is supported by all of the
  record's evidence. Identity and trust fields (`id`, `type`, `from`,
  `to`, `provenance`, verification fields) can't be claimed.
- `extractionRun`: the run the proposal came from, if any (read-only).
- `curatedBy` and `sessionId`: who and which session last changed the
  record.
- `createdAt` (read-only) and `updatedAt`.

Evidence is required for `documented` and `observed` records, optional
for `asserted`, and empty for `synthetic` (ADR-0019).

An edge is itself one assertion: its evidence is the record-level list.
Edges use `claims` only for their own type-specific properties.

A record is stale when a cited raw item has been superseded, or when a
newer conversion of a cited raw item has a different hash than its
`convertedHash`. The build publishes stale records with a `stale` flag
and lists them in a report, naming the newer source or conversion. It
never edits curated records; a directed session updates the evidence.

## Consequences

- Each property can be traced to the exact source, conversion and
  location it came from.
- Most records need no `claims`; per-property evidence is used only
  where sources differ.
- Converter changes now lead to review.
- One value per property: conflicting source values are resolved by the
  curator, and the rejected value is not recorded. Recording disputes
  is deferred until a real conflict appears (#38).
- Some rules need the build, not the schema: evidence keys are unique,
  claims reference existing keys, and claim names are real properties.

## Alternatives considered

- **Evidence on every property:** the fullest traceability, but far more
  work for one curator.
- **Keep record-level sources only:** cheap, but can't say which source
  supports which fact.
