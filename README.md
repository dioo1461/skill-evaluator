# Skill Evaluator

[한국어](README.ko.md)

Skill Evaluator is a Codex skill for evaluating existing Codex skill implementations. It checks whether a skill triggers in the right situations, gives executable instructions, manages context well, and produces verifiable results.

## Features

- Evaluates a skill directory, a single `SKILL.md`, a diff, commit, PR, or execution trace.
- Scores the skill with a 100-point rubric.
- Reports prioritized P0/P1/P2/P3 findings.
- Keeps evaluation read-only by default.
- Applies fixes only when the user explicitly asks for patching or improvement.

## When To Use

- Before sharing or publishing a new Codex skill.
- When checking whether an existing skill has clear triggers, workflow, references, and metadata.
- When comparing multiple skills with the same rubric.
- When analyzing skill behavior from review comments, diffs, or execution traces.
- When you explicitly want Codex to apply the recommended fixes.

## When Not To Use

- Creating a brand-new skill from scratch.
- General code review, documentation review, or product planning.
- Evaluating non-skill application code.
- Applying direction changes or large refactors that the user did not request.

## Repository Layout

- `README.md`: English project documentation
- `README.ko.md`: Korean project documentation
- `skill-evaluator/`: installable Codex skill package
- `skill-evaluator/SKILL.md`: core skill instructions and evaluation rubric
- `skill-evaluator/agents/openai.yaml`: display metadata for Codex
- `skill-evaluator/references/`: report format, scoring guide, patch mode, and checklist
- `skill-evaluator/scripts/validate_skill.py`: read-only structure validator
- `skill-evaluator/examples/calibration/`: examples for evaluator self-checks

## Install

Clone this repository into a temporary directory, copy only the installable skill package into your Codex skills directory, then remove the temporary clone.

```bash
tmpdir=$(mktemp -d)
git clone https://github.com/dioo1461/skill-evaluator.git "$tmpdir"
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/skill-evaluator
cp -R "$tmpdir/skill-evaluator" ~/.codex/skills/skill-evaluator
rm -rf "$tmpdir"
```

To update an existing installation, run the same install commands again.

Restart Codex or reload your skills, then invoke `$skill-evaluator`. The installed skill directory should contain `SKILL.md` directly at `~/.codex/skills/skill-evaluator/SKILL.md`.

## Usage Examples

Evaluate one skill directory.

```text
Use $skill-evaluator to score /path/to/my-skill.
```

Compare multiple skills.

```text
Use $skill-evaluator to compare ./skill-a and ./skill-b.
```

Evaluate and apply fixes.

```text
Use $skill-evaluator to evaluate ./my-skill and apply the P1/P2 fixes.
```

Evaluate a PR or diff.

```text
Use $skill-evaluator to review this skill diff and report validation status.
```

## Improve Until A Target Score

Use Codex `/goal` when you want a validation-fix loop until the skill reaches a target score. Ask for every validation pass to use a fresh read-only subagent, while the main agent applies fixes and integrates results.

```text
/goal Use $skill-evaluator to evaluate ./my-skill and improve it until it reaches at least {target score}/100. For every validation pass, launch a fresh read-only subagent, apply the recommended fixes, and repeat the loop until the target score is reached or a blocker is found.
```

Example with a 90-point target:

```text
/goal Use $skill-evaluator to evaluate ./my-skill and improve it until it reaches at least 90/100. For every validation pass, launch a fresh read-only subagent, apply the recommended fixes, and repeat the loop until the target score is reached or a blocker is found.
```

## Validation

For ordinary structure validation, run:

```bash
python3 skill-evaluator/scripts/validate_skill.py skill-evaluator --skip-answer-key
```

Run the full validator only when you also need to check evaluator calibration files.

```bash
python3 skill-evaluator/scripts/validate_skill.py skill-evaluator
```

If the Codex system skill validator is installed, you can also run:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-evaluator
```

## Calibration

Calibration is optional. Use it when you want to check whether `skill-evaluator` itself is scoring skills consistently. It is usually not needed for ordinary skill evaluation or improvement.

Explicitly request calibration when:

- You want an evaluator self-test.
- You want release-readiness confidence before publishing evaluator changes.
- You want extra confidence before claiming a very high score, such as 100/100.

Example:

```text
Use $skill-evaluator to run a calibrated self-test for this evaluator.
```

When calibration runs, the answer key must not be opened first. Fixture results should be fixed before comparing them with `skill-evaluator/examples/calibration/answer-key.json`.

## Report Example

Final reports usually include score, confidence, category breakdown, validation status, prioritized findings, recommended changes, and assumptions.

```markdown
**Score**
86/100 - Strong skill with a few reliability gaps

**Confidence**
Medium - Local validation passed; behavioral calibration was not run.

**Breakdown**
| Category | Score | Notes |
|---|---:|---|
| Trigger Accuracy | 10/12 | Clear use cases and non-use boundary. |
| Workflow Executability | 11/14 | Main flow is concrete, but one decision point needs clearer fallback behavior. |
| Verification And Completion Criteria | 9/12 | Validation is documented, but completion criteria for patched skills could be more explicit. |

**Validation Result**
- `python3 skill-evaluator/scripts/validate_skill.py skill-evaluator --skip-answer-key`: passed
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-evaluator`: passed

**Findings**
- [P2] `SKILL.md:42` The workflow says to inspect referenced resources, but does not define what to do when a referenced file is missing.
  Impact: Evaluation reports may treat missing optional resources inconsistently.
  Improvement: Add a fallback rule that distinguishes optional missing resources from required missing resources.

**Recommended Changes**
1. Clarify fallback behavior for missing referenced files.
2. Add a short done-condition checklist for patch mode.

**Assumptions / Unknowns**
- Behavioral calibration was not requested for this run.
```
