#!/usr/bin/env python3
"""Validate a Codex/Agent Skills plugin package.

Checks:
- .codex-plugin/plugin.json exists and points to skills
- every skills/<name>/SKILL.md has valid frontmatter
- skill name matches folder name
- required name/description fields are present
- names satisfy Agent Skills naming constraints
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
LOCAL_REFERENCE_PREFIXES = ("assets/", "references/", "scripts/")


def load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"{path.name} parse error: {exc}"
    if not isinstance(payload, dict):
        return None, f"{path.name} root must be an object"
    return payload, None


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.startswith("  "):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    raise ValueError("missing closing YAML frontmatter delimiter")


def field_value(text: str, field: str) -> str:
    match = re.search(rf"^\s*{re.escape(field)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def is_external_reference(reference: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", reference))


def broken_local_references(skill_dir: Path, path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for reference in MARKDOWN_LINK_RE.findall(text):
        normalized = reference.strip()
        if not normalized or normalized.startswith("#") or is_external_reference(normalized):
            continue
        if normalized.startswith(LOCAL_REFERENCE_PREFIXES):
            target = (skill_dir / normalized).resolve()
            try:
                target.relative_to(skill_dir.resolve())
            except ValueError:
                errors.append(f"{path.name}: local reference escapes skill directory: {normalized}")
                continue
            if not target.exists():
                errors.append(f"{path.name}: broken local reference: {normalized}")
    return errors


def manifest_errors(root: Path) -> tuple[dict | None, Path, list[str]]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return None, root / "skills", ["Missing .codex-plugin/plugin.json"]

    manifest, error = load_json(manifest_path)
    if error is not None:
        return None, root / "skills", [error]
    assert manifest is not None

    for field in ["name", "version", "description", "skills"]:
        if field not in manifest:
            errors.append(f"plugin.json missing required/recommended field: {field}")
    if not NAME_RE.match(str(manifest.get("name", ""))):
        errors.append("plugin.json name should be kebab-case lowercase")

    skills_value = manifest.get("skills", "skills")
    if not isinstance(skills_value, str) or not skills_value.strip():
        errors.append("plugin.json skills must be a non-empty relative path")
        return manifest, root / "skills", errors
    skills_path = Path(skills_value)
    if skills_path.is_absolute():
        errors.append("plugin.json skills must be a relative path")
        return manifest, root / "skills", errors

    skills_dir = (root / skills_path).resolve()
    try:
        skills_dir.relative_to(root)
    except ValueError:
        errors.append("plugin.json skills path must stay inside plugin root")
    if not skills_dir.exists():
        errors.append(f"plugin.json skills path does not exist: {skills_value}")
    return manifest, skills_dir, errors


def validate_agent_metadata(skill_dir: Path, skill_name: str) -> tuple[str, list[str]]:
    errors: list[str] = []
    agent_path = skill_dir / "agents" / "openai.yaml"
    if not agent_path.exists():
        return "", [f"{skill_name}: missing agents/openai.yaml"]
    text = agent_path.read_text(encoding="utf-8")
    short_description = field_value(text, "short_description")
    default_prompt = field_value(text, "default_prompt")
    if not short_description:
        errors.append(f"{skill_name}: agents/openai.yaml missing short_description")
    if not default_prompt:
        errors.append(f"{skill_name}: agents/openai.yaml missing default_prompt")
    return default_prompt, errors


def validate_skill_dir(skill_dir: Path, seen_names: set[str]) -> tuple[str, str, list[str]]:
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    readme_path = skill_dir / "README.md"

    if not skill_path.exists():
        return skill_name, "", [f"{skill_name}: missing SKILL.md"]

    if not readme_path.exists():
        errors.append(f"{skill_name}: missing README.md")

    try:
        frontmatter = parse_frontmatter(skill_path)
    except Exception as exc:
        return skill_name, "", [*errors, f"{skill_name}: frontmatter error: {exc}"]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        errors.append(f"{skill_name}: missing name")
    if not description:
        errors.append(f"{skill_name}: missing description")
    if len(description) > 1024:
        errors.append(f"{skill_name}: description exceeds 1024 characters")
    if name != skill_name:
        errors.append(f"{skill_name}: frontmatter name '{name}' does not match folder")
    if not NAME_RE.match(name):
        errors.append(f"{skill_name}: invalid skill name '{name}'")
    if name in seen_names:
        errors.append(f"duplicate skill name: {name}")
    seen_names.add(name)

    default_prompt, agent_errors = validate_agent_metadata(skill_dir, skill_name)
    errors.extend(agent_errors)
    for path in [skill_path, readme_path]:
        if path.exists():
            errors.extend(f"{skill_name}: {error}" for error in broken_local_references(skill_dir, path))
    return skill_name, default_prompt, errors


def validate_skills(skills_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skills_dir.exists():
        return ["Missing skills/ directory"]

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        return ["skills/ directory contains no skill folders"]

    seen_names: set[str] = set()
    seen_prompts: dict[str, str] = {}
    for skill_dir in skill_dirs:
        skill_name, default_prompt, skill_errors = validate_skill_dir(skill_dir, seen_names)
        errors.extend(skill_errors)
        if default_prompt:
            previous_skill = seen_prompts.get(default_prompt)
            if previous_skill is not None:
                errors.append(f"duplicate default_prompt in {previous_skill} and {skill_name}")
            seen_prompts[default_prompt] = skill_name
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    _, skills_dir, errors = manifest_errors(root)
    errors.extend(validate_skills(skills_dir))

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
