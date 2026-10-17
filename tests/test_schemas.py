"""Validation tests for the schemas in schemas/ (ADR-0016)."""

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"
RELATED_TO = "urn:graphea:schema:edge:related-to"
EDGE = "urn:graphea:schema:edge"
T = "2026-10-17T17:30:00Z"
SOURCE = [{"rawItem": "example-raw-item", "hash": "sha256:" + "a" * 64}]

BASE_EDGE = {
    "id": "org.example-agency--related-to--system.example-portal",
    "type": "related-to",
    "from": "org.example-agency",
    "to": "system.example-portal",
    "label": "sponsors the redesign of",
    "origin": "synthetic",
    "verification": "unverified",
    "basis": "stated",
    "states": ["target"],
    "provenance": {"sources": [], "session": "directed", "createdAt": T, "updatedAt": T},
}


def load_schemas():
    return [json.loads(p.read_text()) for p in SCHEMAS.rglob("*.schema.json")]


@pytest.fixture(scope="module")
def validator_for():
    schemas = load_schemas()
    registry = Registry().with_resources(
        (s["$id"], Resource.from_contents(s)) for s in schemas
    )
    by_id = {s["$id"]: s for s in schemas}
    return lambda schema_id: Draft202012Validator(
        by_id[schema_id], registry=registry, format_checker=FormatChecker()
    )


@pytest.mark.parametrize("schema", load_schemas(), ids=lambda s: s["$id"])
def test_schema_is_valid_2020_12(schema):
    Draft202012Validator.check_schema(schema)


def edit(**changes):
    """Copy BASE_EDGE and apply changes; a value of None deletes the key.
    Keys like provenance__sources edit nested fields."""
    record = copy.deepcopy(BASE_EDGE)
    for key, value in changes.items():
        *parents, leaf = key.split("__")
        target = record
        for p in parents:
            target = target[p]
        if value is None:
            target.pop(leaf)
        else:
            target[leaf] = value
    return record


VERIFIED = dict(verification="verified", verifiedAt=T, verifiedBy="roballred")

CASES = [
    ("baseline related-to edge", True, edit()),
    ("unknown field (typo)", False, edit(lable="x")),
    ("misspelled required field", False, edit(verification=None, verfication="unverified")),
    ("missing label", False, edit(label=None)),
    ("type is not related-to", False, edit(type="operates")),
    ("states past alone", True, edit(states=["past"])),
    ("states current and target", True, edit(states=["current", "target"])),
    ("states past combined", False, edit(states=["past", "current"])),
    ("states empty", False, edit(states=[])),
    ("states duplicated", False, edit(states=["current", "current"])),
    ("verified with stamp", True, edit(**VERIFIED)),
    ("verified without stamp", False, edit(verification="verified")),
    ("unverified with stamp", False, edit(verifiedBy="roballred")),
    ("documented without sources", False, edit(origin="documented")),
    ("documented with sources", True, edit(origin="documented", provenance__sources=SOURCE)),
    ("synthetic with sources", False, edit(provenance__sources=SOURCE)),
    ("hash without algorithm prefix", False,
     edit(origin="documented", provenance__sources=[{"rawItem": "x", "hash": "a" * 64}])),
    ("invalid date-time", False, edit(provenance__createdAt="yesterday")),
    ("unattended session", False, edit(provenance__session="unattended")),
    ("extra field in provenance", False, edit(provenance__note="x")),
    ("uppercase edge id", False, edit(id="Org.A--related-to--system.b")),
]


@pytest.mark.parametrize("record_valid, record", [(v, r) for _, v, r in CASES],
                         ids=[name for name, _, _ in CASES])
def test_related_to_edge(validator_for, record_valid, record):
    errors = list(validator_for(RELATED_TO).iter_errors(record))
    assert (not errors) == record_valid, errors[:1]


def test_abstract_edge_base_is_open(validator_for):
    """Bases stay open so type schemas can add fields (ADR-0016)."""
    assert validator_for(EDGE).is_valid(edit(anything=1))
