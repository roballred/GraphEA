# 0001. Record architecture decisions as ADRs

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

GraphEA is designed in conversation, and decisions are made faster than
they can be remembered. Without a record, the reasons behind the
structure are lost, decisions get reopened, and anyone new to the repo
(including AI agents working in it) has to guess why things are the way
they are.

## Decision

Each significant knowledge base design decision is recorded as an
Architecture Decision Record (ADR) in `docs/decisions/`. Working
conventions live in AGENTS.md, not in ADRs.

- One decision per file, named `NNNN-short-title.md`, numbered in order.
- Sections: Context, Decision, Consequences, Alternatives considered.
  New ADRs start from [template.md](template.md).
- Status is one of: Proposed, Accepted, Superseded by NNNN, Deprecated.
- Once accepted, an ADR is not edited except for its status line. To
  change a decision, write a new ADR that supersedes the old one.

## Consequences

- The reasons behind decisions survive, and git records when each
  changed.
- Superseded ADRs stay in the repo, so the history of thinking is kept.
- Writing an ADR adds a small cost to each decision. Minor choices
  don't need one.

## Alternatives considered

- **A single decisions log file:** simpler, but it grows without limit
  and makes it hard to link to or supersede a single decision.
- **Wiki or issue comments only:** these live outside the repo and
  drift from the content they describe.
