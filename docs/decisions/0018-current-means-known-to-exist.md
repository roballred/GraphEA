# 0018. Current means known to exist now

- **Status:** Accepted
- **Date:** 2026-10-17
- **Supersedes:** [0014](0014-architecture-states.md)

## Context

ADR-0014 defined `["current"]` as "exists now; not part of the target
state". Most sources only establish that something exists. Silence
about the target state is not a statement that something is leaving,
but under ADR-0014 every live system taken from an inventory would read
as being retired.

## Decision

Every node and edge has a required `states` field: a non-empty list
drawn from `current`, `target` and `past`.

| `states` | Meaning |
|---|---|
| `["current"]` | Known to exist now. Target state not asserted. |
| `["current", "target"]` | Exists now, and is explicitly part of the target state |
| `["target"]` | Planned; doesn't exist yet |
| `["past"]` | Existed before; no longer exists |

`past` cannot be combined with other values. Absence from the target
state, including planned retirement, requires an explicit signal from a
source and is not expressed through `states`. The LLM proposes states;
the curator verifies them.

## Consequences

- Inventories and policy documents map safely to `["current"]`.
- A target-state view includes only things explicitly placed in the
  target; unknown target status is left out, not guessed.
- "Exists now but is being retired" can't be expressed yet. Target
  contexts (#19) are the intended place for it.

## Alternatives considered

- **Keep ADR-0014's meaning:** marks live things as leaving.
- **Add a `retiring` value now:** premature before target contexts are
  designed.
