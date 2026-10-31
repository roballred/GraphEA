# 0025. Medallion pipeline feeding a Neo4j knowledge graph

- **Status:** Proposed
- **Date:** 2026-10-30

## Context

GraphEA has a curated record design (ADRs 0003–0024) but no pipeline,
no text chunks, no embeddings and no store an AI can query. Issue #42
proposes building one Neo4j knowledge graph from raw sources, with a
medallion-style build.

## Decision

- Data moves through three layers:
  - **Bronze** (`data/bronze/`): files exactly as fetched, with
    manifests. Was `data/raw/`.
  - **Silver** (`data/silver/`): parsed text and chunks, extraction
    candidates, and reviewed records. Was `converted/`, `extracted/`
    and `curated/`.
  - **Gold**: a Neo4j graph. Was `data/published/`.
- Reviewed records stay one JSON file per node or edge in
  `data/silver/reviewed/`, with full provenance and verification
  (ADRs 0006, 0011, 0023, 0024). They are the source of truth; Neo4j
  is a view built from them.
- Extraction runs stay in git (ADR-0012), because LLM output can't be
  reproduced exactly. Parsed text and chunks are git-ignored, since
  they can be rebuilt deterministically.
- Gold is loaded into Neo4j. Every GraphEA node carries the
  `:GraphEA` label, and loads, wipes and indexes touch only
  `:GraphEA` data and `graphea_*` indexes.
- Connection settings come from environment variables in a
  git-ignored `.env` file, never from the repository.
- GraphEA starts in the existing shared Neo4j database and will move
  to a separate container hosted in Azure.
- Extraction starts rules-only; an LLM is added in a later slice.

## Consequences

- The graph can be rebuilt from git alone: bronze + reviewed records
  + extraction runs.
- Relationship evidence in Neo4j can be simple properties, because the
  full provenance stays in the silver records.
- Committing to Neo4j relaxes principle 7 for the gold layer only.
  Silver stays in neutral JSON, so another store remains possible.
- Moving to Azure is a configuration change and a reload.
- While the database is shared, a query that forgets `:GraphEA` could
  touch the other KB's data. Every loader query must be scoped.

## Alternatives considered

- **#42 as written** (candidates git-ignored, records as a decision
  log): smaller repo, but loses exact extraction history.
- **A neutral export with Neo4j as one consumer:** keeps every option
  open, but adds a layer nobody uses yet.
- **A separate container now:** safer isolation, but needs memory the
  local machine doesn't have.
