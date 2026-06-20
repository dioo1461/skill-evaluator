#!/usr/bin/env python3
"""Read-only structural validator for Codex skill directories.

The script performs no filesystem writes. It uses PyYAML for full YAML parsing
when available, with a small dependency-free fallback for simple packaged skill
metadata. It is designed as the deterministic baseline check for this skill-
evaluator package and skill directories that intentionally use the same
evaluator resource contract.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml as _yaml
except ImportError:  # pragma: no cover - exercised only in minimal runtimes.
    _yaml = None

ALLOWED_TOP_LEVEL = {
    "SKILL.md",
    "LICENSE",
    "LICENSE.txt",
    "license.txt",
    "agents",
    "assets",
    "examples",
    "references",
    "resources",
    "scripts",
    "templates",
}
REQUIRED_REFERENCES = {
    "references/scoring-guide.md",
    "references/report-format.md",
    "references/patch-mode.md",
    "references/evaluation-checklist.md",
}
KNOWN_CATEGORIES = {
    "Trigger Accuracy",
    "Goal Fit And Scope Control",
    "Workflow Executability",
    "Context Management",
    "Tool And Resource Design",
    "Subagent And Parallel Work Design",
    "Verification And Completion Criteria",
    "Failure Handling And Safety",
    "Maintainability And Metadata",
    "Output Quality And Collaboration",
}
KNOWN_PRIORITIES = {"P0", "P1", "P2", "P3"}
PATH_TOKEN_RE = re.compile(r"`((?:agents|assets|examples|references|resources|scripts|templates)/[^`]+)`")
CALIBRATION_ID_RE = re.compile(r"^fixture-\d{3}$")
CALIBRATION_ANSWER_FIELDS = {"expected_score_band", "required_findings", "expected_strengths"}
SECTION_HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
SCRIPT_WRITE_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"\.write_text\s*\(",
        r"\.write_bytes\s*\(",
        r"\.unlink\s*\(",
        r"\brmtree\s*\(",
        r"\bos\.remove\s*\(",
        r"\bos\.unlink\s*\(",
        r"\bos\.rmdir\s*\(",
        r"\bopen\s*\([^)]*,\s*['\"][wa+]",
        r"\bsubprocess\.[^(]+\([^)]*(?:rm\s+-rf|git\s+push|gh\s+pr\s+create)",
    )
]
TARGET_SCORE_CONTRACT_TERMS = {
    "section": "## Target-Score Goal Loops",
    "compact invocation without space": "/goal $skill-evaluator objective: 95",
    "compact invocation with space": "/goal $ skill-evaluator objective: 95",
    "explicit target example": "target: ./my-skill objective: 95",
    "target score objective field": "objective",
    "target score score field": "score",
    "target score target_score field": "target_score",
    "target scope fields": "target`, `path`, `scope",
    "ambiguous scope clarification": "ask one concise question",
    "patch mode": "references/patch-mode.md",
    "backup requirement": "backup",
    "fresh read-only subagent": "fresh read-only evaluator subagent",
    "main owns edits": "main agent owns edits",
    "stop conditions": "Repeat until",
    "goal completion": "mark the goal complete",
    "blocked lifecycle": "blocked criteria",
    "anti score chasing": "Do not weaken the rubric",
}


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{path}: not valid UTF-8 text: {exc}")
    except OSError as exc:
        errors.append(f"{path}: cannot read: {exc}")
    return ""


def section_text(markdown: str, heading: str) -> str:
    start = markdown.find(heading)
    if start == -1:
        return ""
    next_heading = SECTION_HEADING_RE.search(markdown, start + len(heading))
    end = next_heading.start() if next_heading else len(markdown)
    return markdown[start:end]


def parse_simple_yaml_mapping(source_name: str, text: str, errors: list[str]) -> dict[str, object]:
    """Parse the limited key/value YAML subset used by simple skill metadata."""

    fields: dict[str, object] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            errors.append(f"{source_name}: nested YAML requires PyYAML")
            continue
        if ":" not in line:
            errors.append(f"{source_name}: unsupported YAML line {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        fields[key] = value
    return fields


def parse_yaml_mapping(source_name: str, text: str, errors: list[str]) -> dict[str, object]:
    if _yaml is not None:
        try:
            parsed = _yaml.safe_load(text) or {}
        except Exception as exc:  # PyYAML exposes several parser exception types.
            errors.append(f"{source_name}: invalid YAML: {exc}")
            return {}
        if not isinstance(parsed, dict):
            errors.append(f"{source_name}: YAML document must be a mapping")
            return {}
        return parsed

    return parse_simple_yaml_mapping(source_name, text, errors)


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, object]:
    if not text.startswith("---\n"):
        errors.append("SKILL.md: missing opening YAML frontmatter fence")
        return {}

    end = text.find("\n---", 4)
    if end == -1:
        errors.append("SKILL.md: missing closing YAML frontmatter fence")
        return {}

    return parse_yaml_mapping("SKILL.md frontmatter", text[4:end], errors)


def parse_interface_yaml(path: Path, errors: list[str]) -> dict[str, object]:
    text = read_text(path, errors)
    if _yaml is None:
        values: dict[str, object] = {}
        in_interface = False
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped == "interface:":
                in_interface = True
                continue
            if in_interface:
                match = re.match(r"^\s{2}([A-Za-z_][A-Za-z0-9_]*):\s*(.+?)\s*$", line)
                if match:
                    values[match.group(1)] = match.group(2).strip().strip("\"'")
                elif not line.startswith(" "):
                    in_interface = False
        return values

    parsed = parse_yaml_mapping("agents/openai.yaml", text, errors)
    interface = parsed.get("interface")
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml: interface must be a mapping")
        return {}
    return interface


def check_frontmatter(root: Path, errors: list[str]) -> None:
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        errors.append("SKILL.md: missing")
        return

    fields = parse_frontmatter(read_text(skill_path, errors), errors)
    for key in ("name", "description"):
        value = fields.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"SKILL.md frontmatter: {key!r} must be a non-empty string")

    description = fields.get("description", "")
    if isinstance(description, str) and "Do not use" not in description and "not use" not in description.lower():
        errors.append("SKILL.md frontmatter: description should include a non-use boundary")


def check_top_level(root: Path, errors: list[str]) -> None:
    for child in sorted(root.iterdir()):
        name = child.name
        if name.startswith("."):
            errors.append(f"{child.relative_to(root)}: hidden files are not allowed in packaged skills")
        elif name not in ALLOWED_TOP_LEVEL:
            errors.append(f"{child.relative_to(root)}: unexpected top-level entry")


def check_hidden_files(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            errors.append(f"{rel}: hidden files are not allowed in packaged skills")


def check_metadata(root: Path, errors: list[str]) -> None:
    metadata = root / "agents" / "openai.yaml"
    if not metadata.exists():
        return
    values = parse_interface_yaml(metadata, errors)
    for key in ("display_name", "short_description", "default_prompt"):
        value = values.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"agents/openai.yaml: interface.{key} must be a non-empty string")
    prompt = values.get("default_prompt", "")
    if isinstance(prompt, str) and "$skill-evaluator" not in prompt and "skill" not in prompt.lower():
        errors.append("agents/openai.yaml: default_prompt appears stale for a skill evaluator")


def check_target_score_goal_loop(root: Path, errors: list[str]) -> None:
    text = read_text(root / "SKILL.md", errors)
    target_section = section_text(text, "## Target-Score Goal Loops")
    if not target_section:
        errors.append("SKILL.md: missing Target-Score Goal Loops section")
        return

    for label, required_text in TARGET_SCORE_CONTRACT_TERMS.items():
        if required_text not in target_section:
            errors.append(f"SKILL.md Target-Score Goal Loops: missing {label}: {required_text!r}")


def check_referenced_paths(root: Path, errors: list[str]) -> None:
    text_files = [root / "SKILL.md"]
    references = root / "references"
    if references.exists():
        text_files.extend(sorted(references.glob("*.md")))

    referenced: set[str] = set()
    for path in text_files:
        if not path.exists():
            continue
        text = read_text(path, errors)
        for match in PATH_TOKEN_RE.finditer(text):
            token = match.group(1).strip()
            token = token.split("#", 1)[0].rstrip(".,;:")
            referenced.add(token)

    for required in REQUIRED_REFERENCES:
        if (root / required).exists():
            referenced.add(required)
        else:
            errors.append(f"{required}: required evaluator reference is missing")

    for token in sorted(referenced):
        if not (root / token).exists():
            errors.append(f"{token}: referenced resource does not exist")


def check_script_safety(root: Path, errors: list[str]) -> None:
    scripts = root / "scripts"
    if not scripts.exists():
        return
    for path in sorted(scripts.glob("*.py")):
        text = read_text(path, errors)
        for pattern in SCRIPT_WRITE_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(root)}: script contains write/destructive pattern {pattern.pattern!r}")


def check_size_hygiene(root: Path, errors: list[str], warnings: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}:
            errors.append(f"{rel}: generated Python bytecode artifacts are not allowed in packaged skills")
            continue
        if not path.is_file():
            continue
        if path.stat().st_size > 512_000:
            errors.append(f"{rel}: file is larger than 512 KiB")
            continue
        if path.suffix in {".md", ".py", ".json", ".yaml", ".yml"}:
            text = read_text(path, errors)
            line_count = len(text.splitlines())
            if line_count > 650:
                warnings.append(f"{rel}: {line_count} lines; inspect for context bloat")


def load_json_file(path: Path, rel_path: str, errors: list[str]) -> object | None:
    try:
        return json.loads(read_text(path, errors))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel_path}: invalid JSON: {exc}")
    return None


def check_calibration_files(root: Path, errors: list[str], *, validate_answer_key: bool) -> None:
    calibration_root = root / "examples" / "calibration"
    problems_rel = "examples/calibration/problems.json"
    answer_key_rel = "examples/calibration/answer-key.json"
    problems_path = root / problems_rel
    answer_key_path = root / answer_key_rel
    deprecated_manifest = calibration_root / "manifest.json"

    if deprecated_manifest.exists():
        errors.append("examples/calibration/manifest.json: deprecated combined problem/answer manifest must be removed")
    if not problems_path.exists():
        errors.append(f"{problems_rel}: missing behavioral calibration problem list")
        return
    if not answer_key_path.exists():
        errors.append(f"{answer_key_rel}: missing behavioral calibration answer key")
        return

    problems = load_json_file(problems_path, problems_rel, errors)
    if not isinstance(problems, dict):
        return
    answer_key = load_json_file(answer_key_path, answer_key_rel, errors) if validate_answer_key else None
    if validate_answer_key and not isinstance(answer_key, dict):
        return

    problem_fixtures = problems.get("fixtures")
    if not isinstance(problem_fixtures, list) or len(problem_fixtures) < 5:
        errors.append(f"{problems_rel}: expected at least five fixtures")
        return
    answer_fixtures = None
    if validate_answer_key:
        assert isinstance(answer_key, dict)
        answer_fixtures = answer_key.get("fixtures")
        if not isinstance(answer_fixtures, list) or len(answer_fixtures) < 5:
            errors.append(f"{answer_key_rel}: expected at least five answer entries")
            return

    problem_ids: set[str] = set()
    for index, fixture in enumerate(problem_fixtures):
        prefix = f"{problems_rel} fixture {index}"
        if not isinstance(fixture, dict):
            errors.append(f"{prefix}: fixture must be an object")
            continue

        leaked_answer_fields = sorted(CALIBRATION_ANSWER_FIELDS.intersection(fixture))
        if leaked_answer_fields:
            errors.append(f"{prefix}: answer-only fields must not appear in problems.json: {', '.join(leaked_answer_fields)}")

        fixture_id = fixture.get("id")
        target_path = fixture.get("target_path")
        scope = fixture.get("scope")
        if not isinstance(fixture_id, str) or not CALIBRATION_ID_RE.match(fixture_id):
            errors.append(f"{prefix}: id must use neutral fixture-NNN format")
            continue
        if fixture_id in problem_ids:
            errors.append(f"{prefix}: duplicate fixture id {fixture_id!r}")
        problem_ids.add(fixture_id)

        expected_target_path = f"examples/calibration/fixtures/{fixture_id}"
        if target_path != expected_target_path:
            errors.append(f"{prefix}: target_path must be {expected_target_path!r} to avoid answer leakage")
            continue
        if scope != "directory":
            errors.append(f"{prefix}: scope must be 'directory'")

        target = root / target_path
        if not target.exists():
            errors.append(f"{prefix}: target_path {target_path!r} does not exist")
        elif not target.is_dir():
            errors.append(f"{prefix}: target_path {target_path!r} must be a directory")
        elif not (target / "SKILL.md").is_file():
            errors.append(f"{prefix}: target directory must contain SKILL.md")

    fixtures_root = calibration_root / "fixtures"
    if not fixtures_root.is_dir():
        errors.append("examples/calibration/fixtures: missing neutral fixture directory")
    else:
        for child in sorted(fixtures_root.iterdir()):
            if child.is_dir() and child.name not in problem_ids:
                errors.append(f"examples/calibration/fixtures/{child.name}: fixture directory is not listed in problems.json")

    if not validate_answer_key:
        return

    assert isinstance(answer_fixtures, list)
    answer_ids: set[str] = set()
    categories_seen: set[str] = set()
    high_quality_seen = False
    for index, fixture in enumerate(answer_fixtures):
        prefix = f"{answer_key_rel} fixture {index}"
        if not isinstance(fixture, dict):
            errors.append(f"{prefix}: fixture must be an object")
            continue

        fixture_id = fixture.get("id")
        band = fixture.get("expected_score_band")
        findings = fixture.get("required_findings", [])

        if "target_path" in fixture or "scope" in fixture:
            errors.append(f"{prefix}: answer key must not include problem-only target_path or scope")
        if not isinstance(fixture_id, str) or not CALIBRATION_ID_RE.match(fixture_id):
            errors.append(f"{prefix}: id must use neutral fixture-NNN format")
            continue
        if fixture_id in answer_ids:
            errors.append(f"{prefix}: duplicate fixture id {fixture_id!r}")
        answer_ids.add(fixture_id)

        if (
            not isinstance(band, list)
            or len(band) != 2
            or not all(isinstance(item, int) for item in band)
            or band[0] < 0
            or band[1] > 100
            or band[0] > band[1]
        ):
            errors.append(f"{prefix}: expected_score_band must be [min, max] within 0..100")
        elif band[0] >= 90:
            high_quality_seen = True

        if not isinstance(findings, list):
            errors.append(f"{prefix}: required_findings must be a list")
            continue

        for finding_index, finding in enumerate(findings):
            finding_prefix = f"{prefix} required_findings {finding_index}"
            if not isinstance(finding, dict):
                errors.append(f"{finding_prefix}: finding must be an object")
                continue
            priority = finding.get("priority")
            category = finding.get("category")
            if priority not in KNOWN_PRIORITIES:
                errors.append(f"{finding_prefix}: unknown priority {priority!r}")
            if category not in KNOWN_CATEGORIES:
                errors.append(f"{finding_prefix}: unknown category {category!r}")
            else:
                categories_seen.add(category)
            terms = finding.get("must_include", [])
            if not isinstance(terms, list) or not all(isinstance(term, str) and term for term in terms):
                errors.append(f"{finding_prefix}: must_include must be a list of non-empty strings")

    if not high_quality_seen:
        errors.append(f"{answer_key_rel}: expected at least one high-quality fixture")
    if len(categories_seen) < 4:
        errors.append(f"{answer_key_rel}: expected required findings across at least four categories")
    if problem_ids != answer_ids:
        missing_answers = sorted(problem_ids - answer_ids)
        extra_answers = sorted(answer_ids - problem_ids)
        if missing_answers:
            errors.append(f"{answer_key_rel}: missing answer entries for {', '.join(missing_answers)}")
        if extra_answers:
            errors.append(f"{answer_key_rel}: answer entries without problems: {', '.join(extra_answers)}")


def validate(root: Path, *, validate_answer_key: bool = True) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.exists() or not root.is_dir():
        return [f"{root}: not a directory"], warnings

    check_frontmatter(root, errors)
    check_top_level(root, errors)
    check_hidden_files(root, errors)
    check_metadata(root, errors)
    check_target_score_goal_loop(root, errors)
    check_referenced_paths(root, errors)
    check_script_safety(root, errors)
    check_size_hygiene(root, errors, warnings)
    check_calibration_files(root, errors, validate_answer_key=validate_answer_key)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the skill-evaluator package structure without modifying files."
    )
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    parser.add_argument(
        "--skip-answer-key",
        action="store_true",
        help=(
            "Validate structure and calibration problems without reading "
            "examples/calibration/answer-key.json. Use before observed "
            "calibration results have been drafted."
        ),
    )
    args = parser.parse_args()

    root = args.skill_dir.expanduser().resolve()
    errors, warnings = validate(root, validate_answer_key=not args.skip_answer_key)

    if errors:
        print(f"Skill structural validation failed for {root}")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1

    print(f"Skill structural validation passed for {root}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
