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
- Curated records use record schemas; extraction output uses proposal
  schemas in `schemas/proposals/`, which have no IDs or trust fields.
  ([0020](decisions/0020-proposal-and-record-schemas.md))
- One curated record per file, named by its ID, in `nodes/` or `edges/`.
  ([0006](decisions/0006-one-file-per-record.md)) One extraction run per
  file in `data/extracted/runs/`.
  ([0022](decisions/0022-one-file-per-extraction-run.md))
- Every record validates against its type schema; unknown fields are
  rejected. Nodes carry a read-only `type` matching their ID prefix.
  ([0016](decisions/0016-schema-conventions.md))
- Every node and edge has `origin`, `verification`, `states` and
  `provenance`. ([0023](decisions/0023-evidence-claims-and-provenance.md),
  [0019](decisions/0019-origin-with-asserted-facts.md),
  [0018](decisions/0018-current-means-known-to-exist.md))
- `origin` is `documented`, `observed`, `asserted` or `synthetic`.
  Documented and observed records cite evidence; asserted records may.
  ([0019](decisions/0019-origin-with-asserted-facts.md))
- `states` is a non-empty list of `current` and `target`, or `past` on
  its own. `["current"]` means known to exist now, with target state not
  asserted. ([0018](decisions/0018-current-means-known-to-exist.md))

## IDs

- Node IDs are `<type>.<name>`: lowercase letters, digits and single
  hyphens. ([0007](decisions/0007-readable-permanent-ids.md))
- IDs are created once, never changed and never reused. Merged records
  become tombstones. ([0007](decisions/0007-readable-permanent-ids.md))
- Pipelines never create IDs. An extracted ID links automatically only
  when its name agrees; uncertain matches go to the curator.
  ([0021](decisions/0021-name-agreement-before-linking.md))

## Edges

- Each edge is its own record with ID `<from>--<type>--<to>`, at most
  one per combination. ([0011](decisions/0011-edges-as-records.md))
- Every edge has a `basis`: `stated` or `inferred`.
  ([0011](decisions/0011-edges-as-records.md))
- Ad hoc relationships use `related-to` with a `label`, never tags.
  ([0013](decisions/0013-tags-and-related-to.md))

## Provenance and change

- Every curated record cites its evidence: the exact raw item and
  conversion, by hash, optionally with a page, section, table or quote.
  Properties from different sources name their evidence in `claims`.
  ([0023](decisions/0023-evidence-claims-and-provenance.md))
- Records citing a superseded source, or an outdated conversion, are
  flagged stale. ([0023](decisions/0023-evidence-claims-and-provenance.md))
- A verified record stores `verifiedHash`; if its content changes, it is
  published as unverified until re-verified.
  ([0024](decisions/0024-verification-bound-to-content.md))
- Extraction runs are keyed on input, prompt, model and schema, and are
  kept. Unchanged keys are not re-run.
  ([0012](decisions/0012-extraction-runs.md))
