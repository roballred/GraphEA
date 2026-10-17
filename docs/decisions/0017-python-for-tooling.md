# 0017. Python for tooling

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

GraphEA needs code: tests for the schemas now, and later build checks,
converters and extraction pipelines. Choosing a language once keeps
tooling consistent and lets each piece reuse the others.

## Decision

- Tooling is written in Python, version 3.12 or later.
- Tests use pytest and live in `tests/` at the repository root.
  Application code, when it exists, lives in `src/`.
- Schemas are validated with the `jsonschema` library, which supports
  JSON Schema 2020-12 (ADR-0016).
- Dependencies are declared in `pyproject.toml`.

## Consequences

- One language across tests, build, converters and pipelines.
- Python has mature libraries for the work ahead: JSON Schema
  validation, document conversion (PDF, HTML, spreadsheets) and LLM
  APIs.
- A future front end (ADR-0005) is likely to be JavaScript. It shares
  the schemas, not the code, so the two can differ.
- Contributors need Python 3.12+ installed.

## Alternatives considered

- **JavaScript/TypeScript:** would match a likely front end, but has
  weaker tooling for document conversion and data work.
- **Choosing per tool:** flexible, but splits the codebase and
  duplicates shared logic such as loading schemas.
