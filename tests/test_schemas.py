"""Validation tests for the schemas in schemas/ (ADR-0016)."""

import copy

import pytest
from jsonschema import Draft202012Validator

from graphea.schemas import load_schemas, validator_for as schema_validator

RELATED_TO = "urn:graphea:schema:edge:related-to"
EDGE = "urn:graphea:schema:edge"
T = "2026-10-17T17:30:00Z"
EVIDENCE = [{"key": "e1", "rawItem": "example-raw-item", "rawHash": "sha256:" + "a" * 64}]

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
    "provenance": {
        "evidence": [],
        "curatedBy": "roballred",
        "sessionId": "2026-10-17-test",
        "createdAt": T,
        "updatedAt": T,
    },
}


@pytest.fixture(scope="module")
def validator_for():
    return schema_validator


@pytest.mark.parametrize("schema", load_schemas(), ids=lambda s: s["$id"])
def test_schema_is_valid_2020_12(schema):
    Draft202012Validator.check_schema(schema)


def edit(**changes):
    """Copy BASE_EDGE and apply changes; a value of None deletes the key.
    Keys like provenance__evidence edit nested fields."""
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


VERIFIED = dict(verification="verified", verifiedAt=T, verifiedBy="roballred",
                verifiedHash="sha256:" + "d" * 64)

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
    ("verified without verifiedHash", False,
     edit(verification="verified", verifiedAt=T, verifiedBy="roballred")),
    ("unverified with verifiedHash", False, edit(verifiedHash="sha256:" + "d" * 64)),
    ("unverified with stamp", False, edit(verifiedBy="roballred")),
    ("documented without evidence", False, edit(origin="documented")),
    ("documented with evidence", True, edit(origin="documented", provenance__evidence=EVIDENCE)),
    ("synthetic with evidence", False, edit(provenance__evidence=EVIDENCE)),
    ("hash without algorithm prefix", False,
     edit(origin="documented", provenance__evidence=[{"key": "e1", "rawItem": "x", "rawHash": "a" * 64}])),
    ("invalid date-time", False, edit(provenance__createdAt="yesterday")),
    ("missing curatedBy", False, edit(provenance__curatedBy=None)),
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


@pytest.mark.parametrize("evidence", [[], EVIDENCE], ids=["no evidence", "with evidence"])
def test_asserted_origin_evidence_optional(validator_for, evidence):
    """Asserted facts may cite evidence but don't have to (ADR-0019)."""
    record = edit(origin="asserted", provenance__evidence=evidence)
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


# Evidence and claims (ADR-0023)

def documented(**changes):
    """A documented edge with one evidence item, then changes applied."""
    return edit(**{"origin": "documented", "provenance__evidence": copy.deepcopy(EVIDENCE),
                   **changes})


def with_evidence_item(**fields):
    return documented(provenance__evidence=[{**EVIDENCE[0], **fields}])


EVIDENCE_CASES = [
    ("evidence without convertedHash", True, documented()),
    ("evidence with convertedHash and locator", True,
     with_evidence_item(convertedHash="sha256:" + "e" * 64,
                        locator={"page": 4, "quote": "The Example Portal provides"})),
    ("locator quote over 300 characters", False, with_evidence_item(locator={"quote": "x" * 301})),
    ("empty locator", False, with_evidence_item(locator={})),
    ("claim naming a property with evidence", True,
     documented(provenance__claims={"label": {"evidence": ["e1"]}})),
    ("claim overriding origin", True,
     documented(provenance__claims={"label": {"origin": "asserted"}})),
    ("claim on id", False, documented(provenance__claims={"id": {"evidence": ["e1"]}})),
    ("empty claim", False, documented(provenance__claims={"label": {}})),
]


@pytest.mark.parametrize("record_valid, record", [(v, r) for _, v, r in EVIDENCE_CASES],
                         ids=[name for name, _, _ in EVIDENCE_CASES])
def test_evidence_and_claims(validator_for, record_valid, record):
    errors = list(validator_for(RELATED_TO).iter_errors(record))
    assert (not errors) == record_valid, errors[:1]
