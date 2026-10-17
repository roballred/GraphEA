# 0007. Readable, permanent IDs

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Curated overrides, edges and recorded non-matches all point at records
by ID. If IDs change when a pipeline re-runs or a name changes, those
references break. IDs also appear in diffs, filenames and AI-assisted
curation sessions, so they must be easy to read and copy.

## Decision

- IDs have the form `<type>.<name>`: `org.watech`,
  `system.one-washington`, `policy.ocio-141`.
- IDs use lowercase letters, digits and hyphens only, with a single dot
  separating type and name. Names never contain two hyphens in a row,
  since `--` separates the parts of an edge ID (ADR-0011).
- The type prefix must be a registered node type with a schema.
- Name collisions are resolved with a qualifier: `system.portal-doh`.
- An ID is created once, when a record is accepted into `data/curated/`,
  and never changed or reused.
- IDs carry no timestamps. Creation time is recorded in provenance as
  `createdAt` (ADR-0009). A date or version appears in a name only when
  it is part of what the thing is, e.g. `policy.ocio-141-v3`.
- The display name is a separate `name` field and may change freely.
- Each record keeps an `aliases` list of other names it is known by.
- If two records turn out to be the same thing, one is kept, and the
  other becomes a tombstone that records `mergedInto` and keeps its ID
  reserved.
- The set of curated records, including tombstones, is the ID registry.

## Consequences

- References never break; old IDs resolve through tombstones.
- IDs may drift from current names (e.g. after a rebrand). This is
  expected; the `name` field shows the current name.
- Lowercase-only IDs avoid collisions on case-insensitive file systems,
  where `System.Portal.json` and `system.portal.json` are the same file.
- Edge types follow the same lowercase kebab-case style, since they
  appear in edge IDs. JSON field names use camelCase.
- Naming takes judgment each time a record is created.

## Alternatives considered

- **UUIDs/GUIDs:** never collide, but are unreadable in diffs and easy
  for an AI to miscopy.
- **IDs derived from names automatically:** convenient, but change
  whenever the name or the extraction wording changes.
- **Timestamps in IDs:** add no uniqueness the rules above don't already
  give, and make IDs and edge IDs long and hard to read.
- **A separate registry file:** one more file to keep in sync with the
  records it lists.
