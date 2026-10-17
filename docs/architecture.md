# Architecture

How GraphEA's pieces fit together. For why each choice was made, see
[decisions](decisions/).

## Data flow

```mermaid
flowchart LR
  raw[data/raw] -->|convert| converted[data/converted]
  converted -->|extract| extracted[data/extracted]
  extracted -->|curate| curated[data/curated]
  converted --> build((build))
  curated --> build
  build --> published[data/published]
```

| Layer | Holds | Written by | Rebuildable |
|---|---|---|---|
| `raw/` | Sources + manifests, add-only | Curator | No |
| `converted/` | Markdown from sources | Conversion pipelines | Yes |
| `extracted/` | Proposed entities, edges and matches | Extraction (unattended or in a session) | Re-runnable; runs are kept |
| `curated/` | Accepted nodes, edges and narrative | Directed sessions only | No |
| `published/` | Combined output for consumers | The build | Yes |

## Records

Nodes and edges are JSON files named by ID, one record per file, in
`nodes/` and `edges/` folders.

| Field | Nodes | Edges | Notes |
|---|---|---|---|
| `id` | ✓ | ✓ | Read-only. Nodes: `type.name`; edges: `from--type--to` |
| `type`, `from`, `to` | | ✓ | Read-only |
| `name`, `aliases` | ✓ | | Display name may change; aliases drive matching |
| `origin` | ✓ | ✓ | `documented`, `observed`, `synthetic` |
| `verification` | ✓ | ✓ | `unverified`, `verified` |
| `states` | ✓ | ✓ | `current`, `target`, `past` |
| `basis` | | ✓ | `stated`, `inferred` |
| `provenance` | ✓ | ✓ | Sources + hashes, extraction run, timestamps |
| `tags` | optional | optional | Lowercase kebab-case |
| `distinctFrom` | ✓ | | Rejected matches |

Merged records become tombstones (`mergedInto`), which keep their IDs
reserved. Narrative markdown is linked to records by ID.

## Matching

Extracted entities are matched to curated records in tiers: exact ID,
exact alias, candidate match for review, or proposed new entity.
Pipelines never create IDs.

## Change detection

- **Extraction runs** are keyed on input hash, prompt hash, model and
  schema version; unchanged keys are skipped.
- **Staleness:** when a raw source is superseded, records citing it are
  published with a stale flag and listed in a report.
