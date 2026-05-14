"""Coverage tests for skill evaluation fixtures."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
RESEARCH_FIXTURES = ROOT / "tests" / "skill_evals" / "research_behavior" / "fixtures.json"
SCHOLAR_GRADE_FIXTURES = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def fixture_list(path: Path) -> list[dict[str, Any]]:
    fixtures = read_json_object(path).get("fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def skill_names() -> set[str]:
    return {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}


def research_routes() -> set[str]:
    return {
        str(fixture.get("expected_route"))
        for fixture in fixture_list(RESEARCH_FIXTURES)
        if fixture.get("expected_route")
    }


def scholar_grade_skills() -> set[str]:
    return {
        str(fixture.get("skill"))
        for fixture in fixture_list(SCHOLAR_GRADE_FIXTURES)
        if fixture.get("skill")
    }


def sorted_difference(left: set[str], right: set[str]) -> list[str]:
    return sorted(left - right)


class TestSkillEvalCoverage(unittest.TestCase):
    def test_research_behavior_fixtures_cover_every_skill_route(self) -> None:
        self.assertEqual(sorted_difference(skill_names(), research_routes()), [])

    def test_scholar_grade_fixtures_cover_every_skill(self) -> None:
        self.assertEqual(sorted_difference(skill_names(), scholar_grade_skills()), [])

    def test_fixture_skill_references_match_existing_skills(self) -> None:
        known_skills = skill_names()

        self.assertEqual(sorted_difference(research_routes(), known_skills), [])
        self.assertEqual(sorted_difference(scholar_grade_skills(), known_skills), [])


if __name__ == "__main__":
    unittest.main()
