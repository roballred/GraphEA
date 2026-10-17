# 0005. JSON for structured data, markdown for narrative

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

The knowledge base holds two kinds of content: structured records
(entities, edges and their properties) and narrative text (descriptions,
explanations, notes). Storing relationships inside prose makes them hard
to validate, merge or query. Storing narrative inside data fields makes
it hard to read and write.

The structured records will also be used directly by a future user
interface, including generated forms.

## Decision

- Structured records (nodes, edges, manifests) are stored as JSON.
- Each record type has a JSON Schema in `schemas/`, and every record is
  validated against its schema.
- Fields that must never change after creation are marked `readOnly` in
  their schema. The build enforces this by rejecting changes to
  read-only fields in existing records.
- Narrative content is stored as markdown and linked to the records it
  describes by ID.
- `data/converted/` is markdown, since it is text converted from sources.

## Consequences

- Schemas do three jobs: validating records in the build, generating UI
  forms, and acting as the output contract given to the LLM during
  extraction.
- Forms generated from schemas show read-only fields as non-editable, so
  the UI knows what users may change.
- `readOnly` is only an annotation in JSON Schema; validators don't
  enforce it. Enforcement depends on the build comparing each record
  with its previous version.
- JSON is a neutral format that can be loaded into any graph database,
  vector store or application, which keeps consumer choices open.
- JSON has no comments. Explanations belong in narrative markdown or in
  schema descriptions, not inside records.
- A schema change may require migrating existing records. Fields should
  start optional where possible, since tightening a schema later is
  easier than loosening it.

## Alternatives considered

- **Markdown with YAML frontmatter for everything:** readable, but
  relationships split between frontmatter and prose, and frontmatter is
  less directly usable by a UI.
- **YAML:** allows comments and is easier to write by hand, but is less
  directly usable by front-end tools and parses ambiguously in edge cases.
- **A database as the primary store:** queryable, but not diffable in
  git, and it commits to a consumer early.
