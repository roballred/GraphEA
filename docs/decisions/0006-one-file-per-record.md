# 0006. One file per record

- **Status:** Accepted, partly superseded by [0022](0022-one-file-per-extraction-run.md)
- **Date:** 2026-10-17

## Context

Curated records change one at a time, through reviewed diffs. If many
records share one large file, every change touches that file, diffs are
hard to read, and concurrent edits conflict.

## Decision

- Each node and each edge is stored in its own JSON file.
- The filename is the record's ID: `org.watech.json`.
- Nodes and edges are kept in separate folders within each layer that
  holds them, e.g. `data/curated/nodes/` and `data/curated/edges/`.
- Folders are not subdivided by entity type. The type is already part
  of the ID.

## Consequences

- A diff shows exactly which records changed.
- A record's file can be found from its ID without searching.
- A layer may hold thousands of small files. That is well within what
  git and file systems handle; if browsing becomes impractical, an
  index can be generated in `data/published/`.
- Renaming an ID would mean renaming a file. That is never done
  (ADR-0007).

## Alternatives considered

- **One file per entity type** (all systems in `systems.json`): fewer
  files, but large diffs and frequent conflicts.
- **Subfolders by type** (`nodes/system/`): easier to browse, but
  duplicates the ID prefix and ties the folder structure to the domain
  model.
