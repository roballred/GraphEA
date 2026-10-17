# 0013. Tags for classification, related-to for ad hoc relationships

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Curation needs room for informal grouping and for relationships that
don't yet fit a defined edge type. Tags are convenient for both, but
tags have no direction or provenance and aren't edges, so graph
traversal ignores them. Using tags for relationships would bypass the
trust model.

## Decision

- **Tags** classify records. Nodes and edges may carry an optional
  `tags` list, e.g. `cloud-migration`, `pilot`, `legacy`. Tags are
  lowercase kebab-case and are normalized on write.
- Tags are not registered in advance. The build reports every tag in
  use and flags near-duplicates (e.g. `cloud` and `clouds`).
- **Ad hoc relationships** use the generic edge type `related-to`,
  which requires a free-text `label` describing the relationship, e.g.
  "shares a vendor contract with". It is a full edge, with direction and
  provenance (ADR-0011).
- **Promotion:** when a `related-to` label recurs, a new edge type with
  its own schema is defined. Existing `related-to` edges of that kind
  are retired and recreated with the new type, since an edge's type is
  read-only.

## Consequences

- Informal relationships stay inside the trust model.
- The set of edge types grows from real use, not from guessing ahead.
- Tags stay flexible; the build's tag report is what keeps sprawl in
  check.
- Too many `related-to` edges is a signal that edge types are missing.

## Alternatives considered

- **Tags for both classification and relationships:** simple, but
  relationships lose direction and provenance and aren't traversable.
- **A fixed tag vocabulary:** prevents sprawl, but adds friction to the
  informal use tags exist for.
- **Only typed edges:** strict, but forces premature edge-type design.
