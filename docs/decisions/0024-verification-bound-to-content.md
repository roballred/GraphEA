# 0024. Verification bound to reviewed content

- **Status:** Accepted
- **Date:** 2026-10-17
- **Partly supersedes:** [0019](0019-origin-with-asserted-facts.md)

## Context

Under ADR-0019 a verified record that is later edited stays `verified`,
although the reviewed content no longer exists.

## Decision

- A verified record also has `verifiedHash`: the SHA-256 hash of its
  content when verified.
- Content is the record with `verification`, `verifiedAt`, `verifiedBy`,
  `verifiedHash`, and `provenance.updatedAt`, `curatedBy` and
  `sessionId` removed, serialized as canonical JSON (RFC 8785).
  Evidence is included, so changed evidence also invalidates
  verification.
- The build recomputes the hash. If it differs, the record is published
  as `unverified` with `verificationOutdated: true` and listed in a
  report. The curated file is not changed (ADR-0004); the curator
  re-verifies in a directed session.
- Earlier verifications are kept in git history, not in the record.

This replaces ADR-0019's rule that verification is recorded only by
`verifiedAt` and `verifiedBy`. The origin values in ADR-0019 stand.

## Consequences

- Editing verified content can't silently keep its verification.
- Re-verifying is a deliberate act, since it rewrites `verifiedHash`.
- Bookkeeping fields are excluded, so verifying doesn't itself make a
  record outdated.

## Alternatives considered

- **Reset verification by hand when editing:** easy to forget.
- **A verification history inside each record:** duplicates git.
