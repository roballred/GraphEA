# 0010. Record origin and verification on every record

- **Status:** Superseded by [0019](0019-origin-with-asserted-facts.md)
- **Date:** 2026-10-17

## Context

GraphEA mixes information from human-authored documents, machine
sources, and deliberately invented data. It also mixes records a human
has checked with records an LLM proposed and nobody has reviewed yet.
These are separate questions. A record from a real document can still be
wrong if extraction made an error.

## Decision

Every node and edge has two required fields.

`origin`: what kind of source it came from.

| Value | Meaning |
|---|---|
| `documented` | Human-authored: documents, web pages, written notes |
| `observed` | Produced by non-human sources: datasets, APIs, inventories, logs |
| `synthetic` | Invented on purpose, for demonstration, testing or teaching |

`verification`: whether a human has confirmed the record.

| Value | Meaning |
|---|---|
| `unverified` | Not yet confirmed. Every record starts here. |
| `verified` | A human confirmed it against its sources, or for `synthetic` records, reviewed it as intended. |

When `verification` is `verified`, the record also has `verifiedAt`
and `verifiedBy`.

Both fields are carried unchanged into `data/published/`.

## Consequences

- Consumers can filter by trust, e.g. only verified, non-synthetic
  records.
- Synthetic data is always identifiable, even in demos.
- Verifying a record is an explicit act, done in a directed session.
- A stale record keeps its verification status but is also flagged
  stale (ADR-0009); consumers should treat stale-and-verified with
  caution.

## Alternatives considered

- **One combined trust field:** loses the difference between "real but
  unchecked" and "invented".
- **Verification by source only:** treats every record from a reputable
  document as correct, including extraction errors.
