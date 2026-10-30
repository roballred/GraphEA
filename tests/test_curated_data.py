"""Checks on the real data in data/raw/ and data/curated/.

Part of the build checks (#28), run as tests so CI enforces them on every
pull request.
"""

import hashlib
import json
from pathlib import Path

import pytest

from graphea.schemas import has_schema, validator_for
from graphea.verification import verification_is_current

DATA = Path(__file__).resolve().parent.parent / "data"
RAW = DATA / "raw"
CURATED = DATA / "curated"
GIT_SIZE_LIMIT = 10 * 1024 * 1024  # larger raw files use Git LFS

MANIFESTS = sorted(RAW.glob("*/manifest.json"))
NODES = sorted((CURATED / "nodes").glob("*.json"))
EDGES = sorted((CURATED / "edges").glob("*.json"))
NODE_IDS = {p.stem for p in NODES}


def load(path):
    return json.loads(path.read_text())


def assert_valid(schema_id, record):
    assert has_schema(schema_id), f"no schema registered: {schema_id}"
    errors = list(validator_for(schema_id).iter_errors(record))
    assert not errors, errors[0].message


def assert_evidence_and_verification(record):
    provenance = record["provenance"]
    keys = [item["key"] for item in provenance["evidence"]]
    assert len(keys) == len(set(keys)), "evidence keys must be unique"
    for item in provenance["evidence"]:
        manifest = RAW / item["rawItem"] / "manifest.json"
        assert manifest.exists(), f"cited raw item missing: {item['rawItem']}"
        assert load(manifest)["sha256"] == item["rawHash"], \
            f"rawHash doesn't match the manifest for {item['rawItem']}"
    for prop, claim in provenance.get("claims", {}).items():
        assert prop in record, f"claim names a property the record lacks: {prop}"
        assert set(claim.get("evidence", [])) <= set(keys), f"claim {prop} cites unknown evidence"
    if record["verification"] == "verified":
        assert verification_is_current(record), "content changed since verification"


@pytest.mark.parametrize("path", MANIFESTS, ids=[p.parent.name for p in MANIFESTS])
def test_raw_manifest(path):
    manifest = load(path)
    assert_valid("urn:graphea:schema:raw:manifest", manifest)
    assert manifest["id"] == path.parent.name, "manifest id must match its folder"
    if manifest["storage"] == "git":
        file = path.parent / manifest["fileName"]
        assert file.exists(), f"raw file missing: {file.name}"
        assert file.stat().st_size == manifest["bytes"]
        assert manifest["bytes"] <= GIT_SIZE_LIMIT, "files over 10 MB use Git LFS"
        assert "sha256:" + hashlib.sha256(file.read_bytes()).hexdigest() == manifest["sha256"]


@pytest.mark.parametrize("path", NODES, ids=[p.stem for p in NODES])
def test_curated_node(path):
    node = load(path)
    assert_valid(f"urn:graphea:schema:node:{node.get('type')}", node)
    assert path.stem == node["id"], "filename must be the record id"
    assert node["id"].split(".")[0] == node["type"], "id prefix must match type"
    assert_evidence_and_verification(node)


@pytest.mark.parametrize("path", EDGES, ids=[p.stem for p in EDGES])
def test_curated_edge(path):
    edge = load(path)
    assert_valid(f"urn:graphea:schema:edge:{edge.get('type')}", edge)
    assert path.stem == edge["id"], "filename must be the record id"
    assert edge["id"] == f"{edge['from']}--{edge['type']}--{edge['to']}"
    assert edge["from"] in NODE_IDS, f"from node missing: {edge['from']}"
    assert edge["to"] in NODE_IDS, f"to node missing: {edge['to']}"
    assert_evidence_and_verification(edge)
