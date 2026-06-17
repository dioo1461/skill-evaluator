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

Restart Codex or reload your skills, then invoke `$skill-evaluator`.

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

Final reports usually include score, confidence, category breakdown, validation status, calibration status, prioritized findings, strengths, recommended changes, approval-gated direction changes, and assumptions.

### Score

84/100 - Strong practical workflow, with a few gaps around current repository structure and validation entry points.

### Confidence

Medium - `SKILL.md`, `agents/openai.yaml`, adjacent skill metadata, and representative repository structure were inspected. Local validators passed. Runtime traces and full behavioral calibration were not requested.

### Breakdown

| Category | Score | Notes |
|---|---:|---|
| Trigger Accuracy | 9/12 | The trigger scope is clear, but the frontmatter could state non-use boundaries more explicitly. |
| Goal Fit And Scope Control | 9/10 | The purpose is focused and practical. |
| Workflow Executability | 11/14 | The main steps are concrete, but repository selection and capture entry points need clearer fallback behavior. |
| Context Management | 13/14 | The skill is lean and avoids bundled resource bloat. |
| Tool And Resource Design | 8/10 | Tool guidance is useful, but one verification path is not deterministic enough. |
| Subagent And Parallel Work Design | 6/8 | Reviewer responsibility is separated, but availability and permission fallbacks should be clearer. |
| Verification And Completion Criteria | 10/12 | Validation commands and completion criteria are mostly clear. |
| Failure Handling And Safety | 7/8 | Fallbacks are documented, but one working-directory fallback is risky. |
| Maintainability And Metadata | 7/8 | Metadata is valid; a few structure references need to stay aligned with the target repo. |
| Output Quality And Collaboration | 4/4 | The final report shape is clear and easy to scan. |

### Validation Result

- Passed: `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/skill`
- `agents/openai.yaml` parsed successfully.
- Target inventory: `SKILL.md`, `agents/openai.yaml`; no bundled references or scripts.

### Calibration Result

- Not run. This was a normal single-skill artifact evaluation, not calibrated scoring or release-readiness verification.

### Findings

- [P2] `SKILL.md:107` narrows implementation ownership to only a subset of the target repository layers.

  Impact: Agents may place UI code or tests in the wrong layer.

  Improvement: Mirror the target repository's actual layer map and test-placement convention.

- [P2] `SKILL.md:60` falls back to the current directory when repository detection fails.

  Impact: Logs or validation commands may run in the wrong directory.

  Improvement: Require a valid worktree for implementation tasks, or ask the user to select one.

- [P2] `SKILL.md:134` describes screenshot capture, but does not define a stable target-screen entry strategy.

  Impact: Agents may reach screens inconsistently and fall back to weaker validation too early.

  Improvement: Add a short decision tree for deterministic routes, dev screens, user-assisted navigation, and coordinate input.

### Strengths

- Clear artifact log structure and comparison template.
- Good handling for blank or non-hydrated screenshots.
- Verification commands are explicit and easy to rerun.

### Recommended Changes

1. Update ownership and test-placement guidance to match the current target repository.
2. Add a worktree guard before implementation or log creation.
3. Add deterministic screenshot target-entry guidance.
4. Clarify subagent availability and permission fallback behavior.

### Approval-Gated Direction Changes

- None.

### Assumptions / Unknowns

- Representative repository structure was inspected, but not every branch or runtime path.
- No live UI loop or runtime trace was executed.
