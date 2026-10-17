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


@pytest.mark.parametrize("sources", [[], SOURCE], ids=["no sources", "with sources"])
def test_asserted_origin_sources_optional(validator_for, sources):
    """Asserted facts may cite sources but don't have to (ADR-0019)."""
    record = edit(origin="asserted", provenance__sources=sources)
    assert validator_for(RELATED_TO).is_valid(record)


# Proposal schemas (ADR-0020) and extraction runs (ADR-0022)

PROPOSED_RELATED_TO = "urn:graphea:schema:proposal:edge:related-to"
RUN = "urn:graphea:schema:proposal:run"

BASE_PROPOSAL = {
    "type": "related-to",
    "from": "Example Agency",
    "to": "Example Portal",
    "label": "sponsors the redesign of",
    "basis": "stated",
    "states": ["target"],
}

PROPOSAL_CASES = [
    ("proposed related-to edge", True, {}),
    ("proposal with an id", False, {"id": BASE_EDGE["id"]}),
    ("proposal with verification", False, {"verification": "unverified"}),
    ("proposal with provenance", False, {"provenance": BASE_EDGE["provenance"]}),
    ("proposal missing label", False, {"label": None}),
]


@pytest.mark.parametrize("record_valid, changes", [(v, c) for _, v, c in PROPOSAL_CASES],
                         ids=[name for name, _, _ in PROPOSAL_CASES])
def test_proposed_related_to_edge(validator_for, record_valid, changes):
    proposal = {**BASE_PROPOSAL, **changes}
    proposal = {k: v for k, v in proposal.items() if v is not None}
    errors = list(validator_for(PROPOSED_RELATED_TO).iter_errors(proposal))
    assert (not errors) == record_valid, errors[:1]


def run_document(**changes):
    run = {
        "runKey": {
            "inputHash": "sha256:" + "b" * 64,
            "promptHash": "sha256:" + "c" * 64,
            "model": "example-model",
            "schemaVersion": "0.2.0",
        },
        "prompt": "Extract organizations and systems.",
        "createdAt": T,
        "proposals": {"nodes": [], "edges": [BASE_PROPOSAL]},
    }
    run.update(changes)
    return run


RUN_CASES = [
    ("valid run", True, run_document()),
    ("hash without algorithm prefix", False,
     run_document(runKey={**run_document()["runKey"], "inputHash": "b" * 64})),
    ("extra top-level field", False, run_document(notes="x")),
]


@pytest.mark.parametrize("record_valid, run", [(v, r) for _, v, r in RUN_CASES],
                         ids=[name for name, _, _ in RUN_CASES])
def test_extraction_run(validator_for, record_valid, run):
    errors = list(validator_for(RUN).iter_errors(run))
    assert (not errors) == record_valid, errors[:1]


def field_names(schema, by_id):
    """Property names a schema defines itself or through allOf references."""
    names = set(schema.get("properties", {}))
    for part in schema.get("allOf", []):
        ref = part.get("$ref", "")
        if ref in by_id:
            names |= field_names(by_id[ref], by_id)
    return names


def proposal_schema_pairs():
    by_id = {s["$id"]: s for s in load_schemas()}
    return [
        (sid, sid.replace(":proposal", ""), by_id)
        for sid in by_id
        if sid.startswith("urn:graphea:schema:proposal:") and sid != RUN
    ]


PAIRS = proposal_schema_pairs()


@pytest.mark.parametrize("proposal_id, record_id, by_id", PAIRS,
                         ids=[proposal_id for proposal_id, _, _ in PAIRS])
def test_proposal_fields_exist_in_record_schema(proposal_id, record_id, by_id):
    """Every proposal field must also exist in the record schema (ADR-0020)."""
    assert record_id in by_id, f"no record schema for {proposal_id}"
    missing = field_names(by_id[proposal_id], by_id) - field_names(by_id[record_id], by_id)
    assert not missing, f"{proposal_id} has fields the record schema lacks: {missing}"
