"""Loading schemas and building validators (ADR-0016)."""

import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"


def load_schemas(root: Path = SCHEMAS) -> list[dict]:
    """Every schema under `root`, in a stable order."""
    return [json.loads(p.read_text()) for p in sorted(root.rglob("*.schema.json"))]


@cache
def _index() -> tuple[Registry, dict]:
    schemas = load_schemas()
    registry = Registry().with_resources(
        (s["$id"], Resource.from_contents(s)) for s in schemas
    )
    return registry, {s["$id"]: s for s in schemas}


def has_schema(schema_id: str) -> bool:
    return schema_id in _index()[1]


def validator_for(schema_id: str) -> Draft202012Validator:
    """A validator for one schema, resolving URN references to the others."""
    registry, by_id = _index()
    return Draft202012Validator(
        by_id[schema_id], registry=registry, format_checker=FormatChecker()
    )
