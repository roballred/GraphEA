# 0002. Build the knowledge base as a curated GraphRAG

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

GraphEA is a knowledge base for Washington State enterprise architecture.
EA knowledge is mostly about how things relate (who operates which
system, which policy governs what, which systems exchange data), and
those relationships are what users need to reason over.

Plain retrieval-augmented generation (RAG) splits documents into text
chunks and retrieves them by similarity. It can find a passage but can't
reliably follow relationships across documents.

Automated GraphRAG has an LLM extract a graph from documents with no
human involvement. That is fast, but the graph contains whatever the LLM
inferred, including errors and duplicates, with no way to tell trusted
relationships from guesses.

## Decision

GraphEA is a curated GraphRAG: a knowledge graph of entities and
relationships, plus narrative text, built for retrieval by people and AI.

- An LLM proposes entities and relationships, when and how the curator
  directs.
- A human curator decides what enters the curated graph.
- Every node and edge carries its source, origin and verification status,
  so trust is visible on each record.

## Consequences

- Graph quality is limited by curation capacity, not by extraction speed.
  This is intentional.
- Relationships are deliberate, which makes the graph suitable for
  reasoning and for EA analysis, not just search.
- The design must support efficient human review: proposals are separate
  from accepted records, and changes are reviewable as small diffs.
- No graph database, vector store or retrieval method is chosen yet.
  The knowledge base stays in neutral formats so these can be chosen
  later.

## Alternatives considered

- **Plain RAG over documents:** simplest, but it can't answer
  relationship questions and has no curated structure.
- **Fully automated GraphRAG:** scales, but produces a graph of unknown
  accuracy and doesn't fit an EA knowledge base meant to be trusted.
- **Hand-built graph without LLM assistance:** most accurate, but too
  slow to cover the scope of state enterprise architecture.
