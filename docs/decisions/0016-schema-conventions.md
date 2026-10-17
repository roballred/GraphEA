# 0016. Schema conventions

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

ADR-0005 makes JSON Schema the contract for every record. That leaves
open how schemas are written, named, versioned and combined, and which
rules a schema can check at all. JSON Schema validates one record at a
time, so some rules need the build instead.

## Decision

- Schemas use JSON Schema draft 2020-12.
- Layout:
  - `schemas/common.schema.json`: shared definitions (ID patterns,
    enums, provenance, trust rules)
  - `schemas/node.schema.json`, `schemas/edge.schema.json`: abstract
    bases
  - `schemas/nodes/<type>.schema.json`,
    `schemas/edges/<type>.schema.json`: concrete types
- A type schema extends its base with `allOf` + `$ref` and closes itself
  with `unevaluatedProperties: false`. Bases stay open so that type
  schemas can add fields. Every record must validate against its type
  schema, and unknown fields are rejected.
- Nodes have an explicit, read-only `type` field, which must match their
  ID prefix.
- Schema IDs are URNs: `urn:graphea:schema:common`, `…:node`, `…:edge`,
  `…:node:<type>`, `…:edge:<type>`.
- The whole schema set has one semantic version, in `schemas/VERSION`.
  It is the schema version in the extraction run key (ADR-0012). Major:
  a breaking change (field removed, renamed or newly required). Minor:
  new optional fields or types. Patch: descriptions only.
- Hashes are written with their algorithm as a prefix: `sha256:…`.
- Schemas check single records. The build checks what needs other
  records or history: an edge ID equals `from--type--to`, `from` and
  `to` exist, a node's ID prefix matches its `type`, read-only fields
  are unchanged, and `date-time` formats are valid.

## Consequences

- Misspelled fields fail validation instead of passing silently.
- Adding a field means changing a schema and bumping the version: a
  small, deliberate step. "Start loose" applies to which fields are
  required, not to which fields exist.
- A record whose type has no schema can't pass, so new types must be
  registered before use (ADR-0007).
- URNs can't be fetched over the network, so the validator loads schemas
  from `schemas/` by ID. Moving the repository doesn't affect them.
- The validator must support 2020-12 and have format checking enabled.

## Alternatives considered

- **`additionalProperties: false`:** the common way to reject unknown
  fields, but it breaks when schemas are combined with `allOf`.
- **Open schemas:** looser, but typos pass silently.
- **URL schema IDs:** familiar, but tied to where the repository is
  hosted.
- **A version per schema:** finer-grained, but the run key would need
  many versions instead of one.
- **Node type only in the ID prefix:** no duplication, but harder to
  query and to pick the right schema.
