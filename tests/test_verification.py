"""Tests for content hashing and verification (ADR-0024)."""

import copy

from graphea.verification import content_hash, verification_is_current

T = "2026-10-17T17:30:00Z"

RECORD = {
    "id": "org.example-agency--related-to--system.example-portal",
    "type": "related-to",
    "from": "org.example-agency",
    "to": "system.example-portal",
    "label": "sponsors the redesign of",
    "origin": "documented",
    "verification": "unverified",
    "basis": "stated",
    "states": ["target"],
    "provenance": {
        "evidence": [{"key": "e1", "rawItem": "example-raw-item", "rawHash": "sha256:" + "a" * 64}],
        "curatedBy": "roballred",
        "sessionId": "2026-10-17-test",
        "createdAt": T,
        "updatedAt": T,
    },
}


def verified(record):
    """Verify a record the way a directed session would."""
    record = copy.deepcopy(record)
    record.update(verification="verified", verifiedAt=T, verifiedBy="roballred")
    record["verifiedHash"] = content_hash(record)
    return record


def test_hash_has_algorithm_prefix():
    assert content_hash(RECORD).startswith("sha256:")


def test_key_order_does_not_change_hash():
    reordered = dict(reversed(list(RECORD.items())))
    assert content_hash(reordered) == content_hash(RECORD)


def test_changing_content_changes_hash():
    changed = copy.deepcopy(RECORD)
    changed["label"] = "funds the redesign of"
    assert content_hash(changed) != content_hash(RECORD)


def test_changing_evidence_changes_hash():
    changed = copy.deepcopy(RECORD)
    changed["provenance"]["evidence"][0]["rawHash"] = "sha256:" + "b" * 64
    assert content_hash(changed) != content_hash(RECORD)


def test_bookkeeping_and_trust_fields_do_not_change_hash():
    changed = copy.deepcopy(RECORD)
    changed["provenance"].update(updatedAt="2026-10-18T09:00:00Z", sessionId="other",
                                 curatedBy="someone-else")
    changed.update(verification="verified", verifiedAt=T, verifiedBy="roballred",
                   verifiedHash="sha256:" + "c" * 64)
    assert content_hash(changed) == content_hash(RECORD)


def test_content_hash_does_not_modify_record():
    original = copy.deepcopy(RECORD)
    content_hash(RECORD)
    assert RECORD == original


def test_verification_current_right_after_verifying():
    assert verification_is_current(verified(RECORD))


def test_verification_outdated_after_edit():
    record = verified(RECORD)
    record["label"] = "funds the redesign of"
    assert not verification_is_current(record)


def test_verification_survives_bookkeeping_update():
    record = verified(RECORD)
    record["provenance"]["updatedAt"] = "2026-10-18T09:00:00Z"
    record["provenance"]["sessionId"] = "2026-10-18-review"
    assert verification_is_current(record)


def test_unverified_record_is_not_current():
    assert not verification_is_current(RECORD)
