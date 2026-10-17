# 0003. Organize data into lifecycle layers

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Source material arrives in many formats (PDF, HTML, spreadsheets, notes)
and is refined in stages: converted to text, mined by an LLM for proposed
entities and relationships, then reviewed by a human. If those stages
share files or folders, generated output and human decisions become
mixed, and re-running a pipeline can overwrite curated work.

The folder structure should also stay generic. It describes how data
moves, not what the data is about, so it doesn't need restructuring as
the domain model changes. The repository will also hold code, so data
should be kept apart from it.

## Decision

Data moves through five layers, each a folder under `data/`:

| Layer | Contents | Rebuildable? |
|---|---|---|
| `data/raw/` | Source material as received, with a manifest per item. Never modified; only added to. | No: it is the record of what arrived |
| `data/converted/` | Raw material converted to markdown by deterministic pipelines. No LLM. | Yes, from `raw/` |
| `data/extracted/` | LLM proposals: candidate entities, edges and matches. | Re-runnable, but outputs are kept (ADR-0012) |
| `data/curated/` | Accepted entities and edges, corrections and authored content. | No: it is the record of human decisions |
| `data/published/` | Built by combining the layers above. What consumers read. | Yes, from the layers above |

Data flows one way: raw → converted → extracted → curated → published.
No layer writes to a layer upstream of it.

Schemas live in a separate top-level `schemas/` folder, since every
layer and the code use them.

## Consequences

- Anything rebuildable can be deleted and regenerated without losing work.
- `raw/` and `curated/` are the two layers that must never be lost; they
  hold the only things that can't be regenerated.
- A change to a converter changes its output, and therefore the input
  hash, which triggers re-extraction (ADR-0012). Converters must be
  versioned.
- Fixes are always made upstream. A problem in `published/` is fixed in
  the layer that caused it, never in `published/` itself.
- What is committed to git is decided separately (ADR-0015).

## Alternatives considered

- **Source and output side by side** (e.g. `doc.pdf` next to `doc.md`):
  simple, but generated and curated content end up in the same place.
- **Folders by domain** (e.g. `systems/`, `agencies/`): intuitive, but it
  ties the structure to today's domain model and mixes lifecycle stages
  within each folder.
- **Fewer layers** (merging extracted and curated): simpler, but loses
  the record of what the LLM proposed versus what was accepted.
- **Layers at the repository root:** shorter paths, but mixes data
  folders with code as the repository grows.
