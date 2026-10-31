# GraphEA

Curated GraphRAG knowledge base for Washington State enterprise
architecture, built from public sources.

> **Status:** early design. The structure below is planned; most folders
> don't exist yet.

## What this is

GraphEA is a knowledge graph of Washington State enterprise architecture
(organizations, systems, policies and how they relate), plus narrative
text, built for retrieval by people and AI. An LLM proposes entities and
relationships; a human curator decides what is accepted. Every record
shows its source, its origin and whether it has been verified.

## How it's organized

| Path | Purpose |
|---|---|
| `data/bronze/` | Source files exactly as fetched, with manifests |
| `data/silver/text/` | Parsed text and chunks (rebuilt, not committed) |
| `data/silver/extract/` | Extraction runs: proposed entities and relationships |
| `data/silver/reviewed/` | Reviewed records: accepted nodes and edges |
| Neo4j (gold) | The knowledge graph built from silver (not in the repo) |
| `schemas/` | JSON Schemas for every record type |
| `docs/` | Principles, rules, architecture and decisions |

## Read next

- [Principles](docs/principles.md): the beliefs that guide the design
- [Design rules](docs/design-rules.md): the rules every record and pipeline follows
- [Architecture](docs/architecture.md): how the pieces fit together
- [Decisions](docs/decisions/): why it's built this way (ADRs)
- [AGENTS.md](AGENTS.md): how humans and AI agents work in this repo

## License

[MIT](LICENSE). Source documents in `data/bronze/` remain under their
original terms, recorded in each item's manifest.
