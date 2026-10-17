# 0011. Edges are first-class records

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Relationships are the core of the knowledge base and the main subject
of curation. They need the same trust metadata as nodes, and often their
own properties (e.g. how two systems integrate). Embedding edges inside
node files would duplicate them on both ends, or place them arbitrarily
on one end.

## Decision

Each edge is its own JSON record, stored per ADR-0006 and validated by
a JSON Schema for its edge type. This follows the property graph model.

- Edge ID: `<from>--<type>--<to>`, e.g.
  `org.watech--operates--system.one-washington`.
- At most one edge exists per combination of from, type and to. Changes
  over time are expressed through properties and `states` (ADR-0014),
  not duplicate edges.
- Required fields: `id`, `type`, `from`, `to`, `origin`, `verification`,
  `basis`, `states`, `provenance`.
- `basis`: `stated` (the source says it) or `inferred` (concluded from
  context).
- Optional fields: `tags` (ADR-0013) and properties specific to the
  edge type.
- `id`, `type`, `from` and `to` are read-only (ADR-0005). To change one,
  retire the edge and create a new one.
- Edge types are registered, each with a schema. The generic
  `related-to` type requires a free-text `label` (ADR-0013).

## Consequences

- Edges can be curated, verified and traced exactly like nodes.
- Edge IDs can be worked out from their parts and read in diffs.
- Edges convert directly to property-graph databases.
- Merging two nodes (ADR-0007) means retiring their edges and recreating
  them on the surviving node, since edge IDs contain node IDs.

## Alternatives considered

- **Edges embedded in node files:** duplicated or arbitrarily placed,
  and awkward to give provenance.
- **Opaque edge IDs:** avoid the merge cost, but can't be read or worked
  out from their parts.
- **RDF triples:** a standard model, but properties on edges are
  awkward to express.
