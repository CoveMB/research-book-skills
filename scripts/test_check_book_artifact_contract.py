"""Unit tests for the book artifact contract checker."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parent / "check_book_artifact_contract.py"


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--path", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def write_schema(root: Path) -> None:
    schema_dir = root / "shared" / "contracts" / "book"
    schema_dir.mkdir(parents=True, exist_ok=True)
    (schema_dir / "book_artifact.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["schema_version", "artifact_type", "project_title"],
                "properties": {
                    "schema_version": {"const": "book-artifact-v1"},
                    "artifact_type": {
                        "enum": [
                            "claim_evidence_ledger",
                            "chapter_brief",
                            "book_proposal",
                            "source_discovery_log",
                        ]
                    },
                    "project_title": {"type": "string", "minLength": 1},
                    "claims": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["claim", "evidence_status", "safer_wording"],
                            "properties": {
                                "claim": {"type": "string", "minLength": 1},
                                "evidence_status": {"type": "string", "minLength": 1},
                                "safer_wording": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "section_outline": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["section", "function", "key_claim"],
                            "properties": {
                                "section": {"type": "string", "minLength": 1},
                                "function": {"type": "string", "minLength": 1},
                                "key_claim": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "comparable_titles": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["title", "verification_status"],
                            "properties": {
                                "title": {"type": "string", "minLength": 1},
                                "verification_status": {
                                    "enum": ["verified", "unverified", "needed"]
                                },
                                "source_pointer": {"type": "string", "minLength": 1},
                            },
                            "allOf": [
                                {
                                    "if": {
                                        "properties": {
                                            "verification_status": {"const": "verified"}
                                        }
                                    },
                                    "then": {"required": ["source_pointer"]},
                                }
                            ],
                        },
                    },
                    "search_log": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["useful_results"],
                            "properties": {
                                "useful_results": {"type": "integer", "minimum": 0},
                            },
                        },
                    },
                },
                "allOf": [
                    {
                        "if": {"properties": {"artifact_type": {"const": "claim_evidence_ledger"}}},
                        "then": {"required": ["claims"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "chapter_brief"}}},
                        "then": {"required": ["section_outline"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "book_proposal"}}},
                        "then": {"required": ["comparable_titles"]},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )


def write_example(root: Path, name: str, payload: dict) -> None:
    examples_dir = root / "examples" / "book_artifacts"
    examples_dir.mkdir(parents=True, exist_ok=True)
    (examples_dir / name).write_text(json.dumps(payload), encoding="utf-8")


def valid_claim_ledger() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "claim_evidence_ledger",
        "project_title": "Fixture Book",
        "claims": [
            {
                "claim": "The draft makes a causal claim.",
                "evidence_status": "needs_stronger_evidence",
                "safer_wording": "The draft can frame this as a plausible causal pathway.",
            }
        ],
    }


def valid_chapter_brief() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "chapter_brief",
        "project_title": "Fixture Book",
        "section_outline": [
            {
                "section": "Introduction",
                "function": "Frame the chapter problem.",
                "key_claim": "The chapter needs a clear opening claim.",
            }
        ],
    }


def valid_book_proposal() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "book_proposal",
        "project_title": "Fixture Book",
        "comparable_titles": [
            {
                "title": "Unverified Comparable",
                "verification_status": "unverified",
            }
        ],
    }


def valid_source_discovery_log() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "source_discovery_log",
        "project_title": "Fixture Book",
        "search_log": [
            {
                "useful_results": 0,
            }
        ],
    }


def write_valid_coverage_examples(root: Path, *, skip: set[str] | None = None) -> None:
    skipped = skip or set()
    examples = {
        "claim_evidence_ledger": ("claim-ledger.json", valid_claim_ledger()),
        "chapter_brief": ("chapter-brief.json", valid_chapter_brief()),
        "book_proposal": ("book-proposal.json", valid_book_proposal()),
        "source_discovery_log": ("source-discovery-log.json", valid_source_discovery_log()),
    }
    for artifact_type, (name, payload) in examples.items():
        if artifact_type not in skipped:
            write_example(root, name, payload)


class TestBookArtifactContract(unittest.TestCase):
    def test_valid_examples_pass(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root)

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_missing_schema_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("book_artifact.schema.json", result.stdout)

    def test_missing_claim_evidence_status_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            del payload["claims"][0]["evidence_status"]
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("evidence_status", result.stdout)

    def test_verified_comparable_title_requires_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(
                root,
                "book-proposal.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "book_proposal",
                    "project_title": "Fixture Book",
                    "comparable_titles": [
                        {
                            "title": "Known Comparable",
                            "verification_status": "verified",
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("source_pointer", result.stdout)

    def test_unverified_comparable_title_does_not_require_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root, skip={"book_proposal"})
            write_example(
                root,
                "book-proposal.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "book_proposal",
                    "project_title": "Fixture Book",
                    "comparable_titles": [
                        {
                            "title": "Unverified Comparable",
                            "verification_status": "unverified",
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_invalid_artifact_type_enum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            payload["artifact_type"] = "invented_artifact"
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("expected one of", result.stdout)

    def test_unexpected_property_fails_with_property_name(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            payload["unexpected_field"] = "not allowed"
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unexpected_field", result.stdout)

    def test_missing_example_for_schema_artifact_type_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing example for artifact_type", result.stdout)

    def test_unresolved_schema_reference_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"$ref": "#/$defs/missing"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unresolved schema reference", result.stdout)

    def test_unsupported_schema_keyword_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"type": "string", "pattern": "^Fixture"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported schema keyword", result.stdout)

    def test_missing_artifact_type_does_not_trigger_artifact_specific_requirements(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            del payload["artifact_type"]
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("artifact_type", result.stdout)
            self.assertNotIn("section_outline", result.stdout)
            self.assertNotIn("comparable_titles", result.stdout)

    def test_number_below_minimum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(
                root,
                "source-log.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "source_discovery_log",
                    "project_title": "Fixture Book",
                    "search_log": [
                        {
                            "useful_results": -1,
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("minimum", result.stdout)


if __name__ == "__main__":
    unittest.main()
