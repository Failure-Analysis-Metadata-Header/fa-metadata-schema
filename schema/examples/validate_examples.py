#!/usr/bin/env python3
"""
Validate example JSON files against their corresponding schema files.

This script checks that all example files in schema/v2/examples/ are valid
according to the v2.0 schema definitions.

Requirements:
    pip install jsonschema
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
    from jsonschema import ValidationError, validate
except ImportError:
    print("Error: jsonschema module not found. Install it with: pip install jsonschema")
    sys.exit(1)


def load_json_file(path: Path) -> dict:
    """Load and parse a JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error in {path.name}: {e}")
        return None
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return None


def get_schemas_for_example(example_data: dict) -> dict:
    """Extract schema files needed for validating an example."""
    schema_dir = Path(__file__).parent.parent  # v2 directory
    required_schemas = {}

    # Map example sections to schema files
    section_mapping = {
        "generalSection": "generalSection.json",
        "methodSpecific": "methodSpecific.json",
        "dataEvaluation": "dataEvaluation.json",
        "customerSpecific": "customerSection.json",
        "toolSpecific": "toolSpecific.json",
        "history": "historySection.json",
    }

    for section, schema_file in section_mapping.items():
        if section in example_data:
            schema_path = schema_dir / schema_file
            schema = load_json_file(schema_path)
            if schema:
                required_schemas[section] = schema
            else:
                return None

    return required_schemas


def validate_example(example_path: Path) -> Tuple[bool, str]:
    """
    Validate a single example file against schemas.

    Returns:
        Tuple of (is_valid, message)
    """
    # Load example
    example_data = load_json_file(example_path)
    if example_data is None:
        return False, "Failed to parse JSON"

    # Get required schemas
    schemas = get_schemas_for_example(example_data)
    if schemas is None:
        return False, "Failed to load schema files"

    # Validate each section
    errors = []
    for section, schema in schemas.items():
        if section not in example_data:
            continue

        try:
            # Validate against the schema
            validate(instance=example_data, schema=schema)
        except ValidationError as e:
            errors.append(f"  Section '{section}': {e.message}")
        except Exception as e:
            errors.append(f"  Section '{section}': Unexpected error: {e}")

    if errors:
        return False, "\n".join(errors)
    return True, "Valid"


def main():
    """Main validation routine."""
    examples_dir = Path(__file__).parent  # Current directory (examples)

    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        sys.exit(1)

    # Find all example JSON files
    example_files = sorted(examples_dir.glob("*.json"))

    if not example_files:
        print(f"❌ No example files found in {examples_dir}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Validating {len(example_files)} example file(s) against schemas")
    print(f"{'='*70}\n")

    results = []
    for example_file in example_files:
        is_valid, message = validate_example(example_file)
        results.append((example_file.name, is_valid, message))

        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{status}  {example_file.name}")
        if not is_valid:
            print(f"     {message}")

    # Summary
    passed = sum(1 for _, is_valid, _ in results if is_valid)
    total = len(results)

    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} files valid")
    print(f"{'='*70}\n")

    # Exit with error code if any validation failed
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
