#!/usr/bin/env python3
"""Summarize local research behavior fixture coverage and captured outputs."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from check_research_behavior_fixtures import (
    fixture_identifier,
    fixture_list,
    is_compact_fixture,
    output_path_for_fixture,
    read_json_object,
    validate_fixture_document,
    validate_output_for_fixture,
)


def sorted_counts(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def fixture_identifiers(fixtures: list[dict[str, Any]]) -> list[str]:
    return [fixture_identifier(fixture) for fixture in fixtures]


def present_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def missing_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if not output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def output_validation_errors(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        error
        for fixture in fixtures
        for error in validate_output_for_fixture(outputs_dir, fixture)
    ]


def fixture_summary(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(fixtures),
        "ids": fixture_identifiers(fixtures),
        "compact_total": sum(1 for fixture in fixtures if is_compact_fixture(fixture)),
        "expected_route_counts": sorted_counts(
            [
                str(fixture.get("expected_route", ""))
                for fixture in fixtures
                if fixture.get("expected_route")
            ]
        ),
        "covered_risks": sorted(
            {
                str(fixture.get("risk_covered", ""))
                for fixture in fixtures
                if fixture.get("risk_covered")
            }
        ),
    }


def output_summary(outputs_dir: Path | None, fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    if outputs_dir is None:
        return {
            "checked": False,
            "present": [],
            "missing": [],
            "validation_errors": [],
        }

    return {
        "checked": True,
        "directory": str(outputs_dir),
        "present": present_output_identifiers(outputs_dir, fixtures),
        "missing": missing_output_identifiers(outputs_dir, fixtures),
        "validation_errors": output_validation_errors(outputs_dir, fixtures),
    }


def build_calibration_report(fixture_path: Path, outputs_dir: Path | None = None) -> dict[str, Any]:
    document_errors = validate_fixture_document(fixture_path)
    document = read_json_object(fixture_path) if not document_errors else {"fixtures": []}
    fixtures = fixture_list(document)
    return {
        "schema_version": "research-skill-behavior-calibration-v1",
        "source": {
            "fixtures": str(fixture_path),
            "outputs_dir": str(outputs_dir) if outputs_dir else None,
        },
        "fixtures": {
            **fixture_summary(fixtures),
            "validation_errors": document_errors,
        },
        "outputs": output_summary(outputs_dir, fixtures),
        "limits": [
            "This report checks local fixture coverage and captured output markers only.",
            "It does not run a model, verify source truth, or certify scholarly correctness.",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Fixture JSON file to summarize.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Optional directory containing one captured output markdown file per fixture id.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_calibration_report(args.fixtures, args.outputs_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    print(json.dumps(report, indent=2))
    has_errors = bool(report["fixtures"]["validation_errors"] or report["outputs"]["validation_errors"])
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
