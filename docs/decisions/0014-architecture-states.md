# 0014. Record architecture state on every record

- **Status:** Superseded by [0018](0018-current-means-known-to-exist.md)
- **Date:** 2026-10-17

## Context

Enterprise architecture distinguishes what exists now from what is
planned, and from what used to exist. A query for the current-state
architecture must reliably leave out planned and retired systems and
relationships. Sources make this harder: strategic plans describe future
state in present-tense language, and older documents describe systems
that have since been retired.

## Decision

Every node and edge has a required `states` field: a non-empty list
drawn from `current`, `target` and `past`.

| `states` | Meaning |
|---|---|
| `["current"]` | Exists now; not part of the target state (e.g. being retired) |
| `["current", "target"]` | Exists now and continues |
| `["target"]` | Planned; doesn't exist yet |
| `["past"]` | Existed before; no longer exists (retired, decommissioned, repealed) |

`past` cannot be combined with other values.

The LLM proposes states during extraction; the curator verifies them.

## Consequences

- Current-state, target-state and historical views can be built
  reliably by filtering on `states`.
- Planned items extracted from strategy documents must be explicitly
  marked, which surfaces the present-tense trap during review.
- Retired things keep their records and relationships, so history isn't
  lost.
- Dates and multiple target horizons (e.g. 2027 vs. 2030) are not
  covered. If needed, they will extend `states` in a later ADR.

## Alternatives considered

- **Namespaced tags (`state:current`):** flexible, but optional by
  nature, harder for schemas to enforce and for forms to present.
- **Validity dates (`validFrom`/`validTo`):** more precise, but adds
  curation cost before there is a demonstrated need.
- **Deleting retired records:** simpler, but loses history.
- **No state:** simplest, but makes current and target views
  unreliable.
