# 0019. Origin and verification, with curator-asserted facts

- **Status:** Accepted
- **Date:** 2026-10-17
- **Supersedes:** [0010](0010-origin-and-verification.md)

## Context

ADR-0010's origins cover sourced facts and invented data, but not a
real fact the curator knows and no source states, such as which office
runs a system.

## Decision

Every node and edge has two required fields.

`origin`: what kind of source it came from.

| Value | Meaning | Sources |
|---|---|---|
| `documented` | Human-authored: documents, web pages, written notes | Required |
| `observed` | Non-human sources: datasets, APIs, inventories, logs | Required |
| `asserted` | Stated by the curator from their own knowledge; not written down as a source | Optional |
| `synthetic` | Invented on purpose, for demonstration, testing or teaching | None |

A curator's note written up and added to `data/raw/` is a source, and
records citing it are `documented`. `asserted` is for knowledge that
was never written down.

`verification`: whether a human has confirmed the record.

| Value | Meaning |
|---|---|
| `unverified` | Not yet confirmed. Every record starts here. |
| `verified` | A human confirmed it against its sources, or for `asserted` and `synthetic` records, reviewed it as intended. |

When `verification` is `verified`, the record also has `verifiedAt`
and `verifiedBy`.

Both fields are carried unchanged into `data/published/`.

## Consequences

- Curator knowledge gets an honest label instead of a fake source.
- A verified `asserted` record rests on the curator's word; consumers
  can filter on origin to tell it apart from sourced facts.
- Consumers can filter by trust, e.g. only verified, sourced records.
- A stale record keeps its verification status but is also flagged
  stale (ADR-0009).

## Alternatives considered

- **Write every curator fact up as a raw note:** keeps three origins,
  but turns quick knowledge into paperwork.
- **Use `documented` with no sources:** breaks the rule that documented
  facts are traceable.
