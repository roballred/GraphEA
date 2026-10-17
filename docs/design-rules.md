# Design rules

A one-page checklist of the rules every record, pipeline and agent
follows. Each rule links to the decision that explains it. For the
beliefs behind them, see [principles](principles.md).

## Layers and ownership

- Data moves one way: raw → converted → extracted → curated → published.
  No layer writes upstream. ([0003](decisions/0003-lifecycle-layers.md))
- Each layer has exactly one kind of writer. Unattended work writes only
  to `data/extracted/`; only directed sessions write to `data/curated/`.
  ([0004](decisions/0004-single-owner-files.md))
- `data/published/` is never committed; everything that can't be
  regenerated is. ([0015](decisions/0015-committed-data.md))

## Records

- Structured records are JSON, validated by a JSON Schema in `schemas/`.
  Narrative is markdown. ([0005](decisions/0005-json-and-json-schema.md))
- Fields that must never change are `readOnly` in their schema, and the
  build rejects changes to them. ([0005](decisions/0005-json-and-json-schema.md))
- One record per file, named by its ID, in `nodes/` or `edges/`.
  ([0006](decisions/0006-one-file-per-record.md))
- Every record validates against its type schema; unknown fields are
  rejected. Nodes carry a read-only `type` matching their ID prefix.
  ([0016](decisions/0016-schema-conventions.md))
- Every node and edge has `origin`, `verification`, `states` and
  `provenance`. ([0009](decisions/0009-provenance-and-staleness.md),
  [0010](decisions/0010-origin-and-verification.md),
  [0014](decisions/0014-architecture-states.md))
- `states` is a non-empty list of `current` and `target`, or `past` on
  its own. ([0014](decisions/0014-architecture-states.md))

## IDs

- Node IDs are `<type>.<name>`: lowercase letters, digits and single
  hyphens. ([0007](decisions/0007-readable-permanent-ids.md))
- IDs are created once, never changed and never reused. Merged records
  become tombstones. ([0007](decisions/0007-readable-permanent-ids.md))
- Pipelines never create IDs. Uncertain matches go to the curator.
  ([0008](decisions/0008-entity-resolution-tiers.md))

## Edges

- Each edge is its own record with ID `<from>--<type>--<to>`, at most
  one per combination. ([0011](decisions/0011-edges-as-records.md))
- Every edge has a `basis`: `stated` or `inferred`.
  ([0011](decisions/0011-edges-as-records.md))
- Ad hoc relationships use `related-to` with a `label`, never tags.
  ([0013](decisions/0013-tags-and-related-to.md))

## Provenance and change

- Every curated record cites the exact raw items it is based on, with
  their hashes. Records citing superseded sources are flagged stale.
  ([0009](decisions/0009-provenance-and-staleness.md))
- Extraction runs are keyed on input, prompt, model and schema, and are
  kept. Unchanged keys are not re-run.
  ([0012](decisions/0012-extraction-runs.md))
