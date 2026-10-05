#!/usr/bin/env python3
"""Validate a FAMH connector and its optional unresolved sidecar."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:
    jsonschema = None


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def find_connector_schema(connector_path: Path) -> Path | None:
    for parent in connector_path.resolve().parents:
        candidate = parent / "connectors" / "connector-schema.json"
        if candidate.is_file():
            return candidate

    repository_root = Path(__file__).resolve().parents[3]
    candidate = repository_root / "connectors" / "connector-schema.json"
    return candidate if candidate.is_file() else None


def json_pointer(parts: list[Any]) -> str:
    escaped = (str(part).replace("~", "~0").replace("/", "~1") for part in parts)
    return "/" + "/".join(escaped)


def validate_file(document_path: Path, schema_path: Path, label: str) -> bool:
    try:
        document = load_json(document_path)
    except (OSError, json.JSONDecodeError) as error:
        print(f"INVALID {label}: cannot read JSON at {document_path}: {error}")
        return False

    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot read schema at {schema_path}: {error}")
        return False

    try:
        validator_type = jsonschema.validators.validator_for(schema)
        validator_type.check_schema(schema)
    except jsonschema.exceptions.SchemaError as error:
        print(f"ERROR: invalid {label} schema at {schema_path}: {error.message}")
        return False

    errors = sorted(
        validator_type(schema).iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        for error in errors:
            print(f"INVALID {label}: {json_pointer(list(error.absolute_path))}: {error.message}")
        return False

    print(f"VALID {label}: {document_path} conforms to {schema_path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a FAMH connector and an optional .unresolved.json sidecar."
    )
    parser.add_argument("connector", type=Path, help="Connector JSON file")
    parser.add_argument(
        "--unresolved",
        type=Path,
        help="Unresolved sidecar JSON; auto-detected beside the connector when omitted",
    )
    parser.add_argument(
        "--connector-schema",
        type=Path,
        help="Connector schema path (auto-detected in the repository by default)",
    )
    parser.add_argument(
        "--unresolved-schema",
        type=Path,
        help="Unresolved schema path (defaults beside the connector schema)",
    )
    args = parser.parse_args()

    if jsonschema is None:
        print(
            "ERROR: the 'jsonschema' package is required; install it with "
            "python -m pip install jsonschema",
            file=sys.stderr,
        )
        return 2

    connector_schema = args.connector_schema or find_connector_schema(args.connector)
    if connector_schema is None:
        print(
            "ERROR: connector schema not found; pass --connector-schema explicitly",
            file=sys.stderr,
        )
        return 2

    valid = validate_file(args.connector, connector_schema, "connector")

    sidecar = args.unresolved
    if sidecar is None:
        conventional_sidecar = args.connector.with_name(
            f"{args.connector.stem}.unresolved.json"
        )
        if conventional_sidecar.is_file():
            sidecar = conventional_sidecar

    if sidecar is not None:
        unresolved_schema = args.unresolved_schema or connector_schema.with_name(
            "unresolved-schema.json"
        )
        if not validate_file(sidecar, unresolved_schema, "unresolved sidecar"):
            valid = False

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())