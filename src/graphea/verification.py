"""Content hashing for verification (ADR-0024)."""

import copy
import hashlib

import rfc8785

TRUST_FIELDS = ("verification", "verifiedAt", "verifiedBy", "verifiedHash")
BOOKKEEPING_FIELDS = ("updatedAt", "curatedBy", "sessionId")


def content_hash(record: dict) -> str:
    """Hash of the record's reviewable content, as `sha256:<hex>`."""
    content = copy.deepcopy(record)
    for field in TRUST_FIELDS:
        content.pop(field, None)
    for field in BOOKKEEPING_FIELDS:
        content.get("provenance", {}).pop(field, None)
    return "sha256:" + hashlib.sha256(rfc8785.dumps(content)).hexdigest()


def verification_is_current(record: dict) -> bool:
    """True if the record is verified and unchanged since verification."""
    return (
        record.get("verification") == "verified"
        and record.get("verifiedHash") == content_hash(record)
    )
