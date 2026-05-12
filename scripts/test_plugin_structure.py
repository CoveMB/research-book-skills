"""Structure tests for plugin skill routing and naming."""
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
REQUIRED_SKILL_HEADINGS = [
    "## Purpose",
    "## When to use",
    "## Inputs expected",
    "## Procedure",
    "## Output format",
    "## Quality checks",
    "## Failure modes",
    "## Files/folders it may read",
    "## Files/folders it may write",
    "## What it must not do",
]
REQUIRED_README_HEADINGS = [
    "## Procedure",
    "## Quality checks",
    "## Failure modes",
    "## Files/folders it may read",
    "## Files/folders it may write",
    "## What it must not do",
    "## Best next steps",
]


def read_text_files() -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix in {".md", ".json", ".yaml", ".yml", ".sh", ".py"}:
            files.append((path, path.read_text(encoding="utf-8")))
    return files


def frontmatter_name(skill_markdown: str) -> str:
    match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", skill_markdown, re.MULTILINE)
    return match.group(1) if match else ""


class TestPluginStructure(unittest.TestCase):
    def skill_dirs(self) -> list[Path]:
        return sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())

    def test_research_book_orchestrator_replaces_old_skill_name(self) -> None:
        old_skill_name = "-".join(["scholar" + "ly", "book", "orchestrator"])
        skill_path = SKILLS_DIR / "research-book-orchestrator" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertFalse((SKILLS_DIR / old_skill_name).exists())
        self.assertEqual(frontmatter_name(skill_path.read_text(encoding="utf-8")), "research-book-orchestrator")

        stale_references = [
            str(path.relative_to(ROOT))
            for path, text in read_text_files()
            if old_skill_name in text
        ]
        self.assertEqual(stale_references, [])

    def test_each_skill_has_operational_sections(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            for heading in REQUIRED_SKILL_HEADINGS:
                if heading not in text:
                    missing.append(f"{skill_dir.name}: {heading}")
        self.assertEqual(missing, [])

    def test_each_skill_readme_documents_operational_boundaries(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            text = (skill_dir / "README.md").read_text(encoding="utf-8")
            for heading in REQUIRED_README_HEADINGS:
                if heading not in text:
                    missing.append(f"{skill_dir.name}: {heading}")
        self.assertEqual(missing, [])

    def test_each_skill_has_ai_safety_rules(self) -> None:
        missing: list[str] = []
        required_phrases = [
            "source access level",
            "What I can verify",
            "What remains uncertain",
            "User verification needed",
            "Do not invent citations",
        ]
        for skill_dir in self.skill_dirs():
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            for phrase in required_phrases:
                if phrase not in text:
                    missing.append(f"{skill_dir.name}: {phrase}")
        self.assertEqual(missing, [])

    def test_each_skill_documents_next_step_routing(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            readme = (skill_dir / "README.md").read_text(encoding="utf-8")
            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            if "## Best next steps" not in readme and "## Next best skill" not in skill_text:
                missing.append(skill_dir.name)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
