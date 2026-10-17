# 0020. Separate proposal and record schemas

- **Status:** Accepted
- **Date:** 2026-10-17
- **Partly supersedes:** [0005](0005-json-and-json-schema.md)

## Context

ADR-0005 says a record's schema is also the output contract given to
the LLM. But curated record schemas require `id`, verification fields
and `provenance`, which pipelines must never create (ADR-0004,
ADR-0021).

## Decision

- There are two schema families:
  - **Record schemas** (`schemas/node`, `schemas/edge`, `schemas/nodes/`,
    `schemas/edges/`) validate curated records.
  - **Proposal schemas** (`schemas/proposals/node`,
    `schemas/proposals/edge`, `schemas/proposals/nodes/`,
    `schemas/proposals/edges/`) validate what extraction produces.
- Proposal schemas omit `id`, `verification`, `verifiedAt`,
  `verifiedBy`, `verifiedHash` and `provenance`.
- Extraction is given proposal schemas. The build validates curated
  records against record schemas.
- Proposal type schemas mirror record type names.
- Proposal URNs: `urn:graphea:schema:proposal:node`,
  `urn:graphea:schema:proposal:edge`,
  `urn:graphea:schema:proposal:edge:<type>`.
- Proposed edges name endpoints with loose `from`/`to` strings until
  entity resolution defines scoped references (#20).

This replaces ADR-0005's statement that record schemas are the LLM's
output contract. The rest of ADR-0005 stands.

## Consequences

- The LLM is never asked to invent IDs or trust metadata.
- Each type has two schemas to keep consistent; tests check that every
  proposal field also exists in the record schema.
- UI forms keep using record schemas.

## Alternatives considered

- **One schema with fields made optional for proposals:** curated
  records would lose their required trust fields.
