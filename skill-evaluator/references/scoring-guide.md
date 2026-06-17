# Scoring Guide

Load this guide before assigning final category scores, classifying P0/P1/P2 recommendations, resolving scores above 90, or evaluating this skill against itself.

## Calibration

- Use about `50%` when the skill works for a simple local `SKILL.md` but leaves diffs, resource folders, or failure cases underspecified.
- Use about `75%` when the skill is reliable for common cases but one realistic branch still requires agent judgment.
- Use `90-100%` only when instructions cover common cases, edge cases, and reporting expectations with direct evidence.
- Choose an integer between anchor scores only when inspected evidence supports the nuance.
- Do not award `100%` in a category merely because the skill mentions the topic. Full credit requires concise, actionable instructions that are resilient to realistic edge cases and supported by inspected structure or behavior.
- Score each category from its own evidence before assigning the final score. A P0/P1 finding or catastrophic flaw can zero or cap the directly affected category, and may reduce related categories when the evidence supports spillover, but it does not automatically erase unrelated strengths such as clear trigger boundaries, lean context, or aligned metadata.
- Do not double-count the same defect across many categories unless it independently harms each category. For example, overbroad trigger text primarily limits Trigger Accuracy and Goal Fit; unsafe destructive commands primarily limit Failure Handling And Safety and Tool And Resource Design; embedded low-frequency examples primarily limit Context Management and Output Quality.
- Preserve partial credit for simple but real structure. A vague or unsafe fixture may still earn credit for existing frontmatter, an ordered workflow, concise files, or non-stale metadata, while a bloated fixture may still score well on trigger accuracy, goal fit, or safety if those parts are directly supported.
- Treat a category as `not applicable` only when the skill's actual scope gives the agent no meaningful opportunity to exercise that category. For example, a narrow single-purpose skill with no parallelizable work should usually redistribute Subagent And Parallel Work Design instead of receiving `0/8`; a judgment-only skill should not lose Tool And Resource Design points merely because it has no scripts.
- Before opening a calibration answer key, record a category table and check these anchors:
  - Trigger Accuracy: a specific frontmatter description with a non-use boundary is usually `75-100%`; a description that matches ordinary project work or nearly every task is usually `0-25%`.
  - Goal Fit And Scope Control: a bounded domain purpose is usually `75-100%`; a universal helper or workflow that invites adjacent unrelated tasks is usually `0-25%`.
  - Workflow Executability: ordered but vague steps are usually `25-50%`; concrete ordered steps with one missing gate are usually `50-75%`; absent or contradictory steps are `0-25%`.
  - Context Management: a concise single `SKILL.md` with no resource bloat is usually `100%`; inline low-frequency examples or template-heavy material are usually `50-75%`, not `0%`, unless they dominate the artifact.
  - Tool And Resource Design: absence of scripts is neutral or not applicable for simple judgment skills; unsafe destructive commands, external uploads, or unnecessary tools are usually `0-25%`.
  - Verification And Completion Criteria: no validation, checks, done condition, or reporting of unverified work is usually `0-25%`; lightweight but incomplete verification is usually `25-50%`.
  - Failure Handling And Safety: harmless simple skills with limited risk can still earn `50-75%` even if safety is sparse; explicit destructive actions, secret exposure, or confirmation bypasses are `0%`.
  - Maintainability And Metadata: valid frontmatter and a clean concise file are usually `75-100%` when optional metadata is absent; stale metadata, broken references, or hidden/generated files lower this category directly.
  - Output Quality And Collaboration: concise useful output is usually `75-100%`; mandatory exhaustive reports, unrelated suggestions, or hard-to-scan output are usually `0-50%` depending on severity.

## Additional Score-Limiting Review Lenses

Use these lenses to prevent inflated scores, especially for self-evaluation. Do not award full credit merely because the skill states desired behavior; look for evidence that the behavior is structurally enabled, tested, or safely bounded.

### Behavioral Efficacy

- Cap `Verification And Completion Criteria` at about `75%` when the skill has no test prompts, expected outcomes, execution traces, deterministic graders, or before/after comparison strategy.
- Treat behavioral evaluation as confidence evidence, not an automatic prerequisite for a perfect score.
- Limit the score only when the evaluation relies on unverified behavior-level claims that are not otherwise supported by inspected workflow, structure, validation output, or direct evidence.
- For behavior-level claims, prefer evidence from no-skill baselines, previous-version comparisons, competing-skill comparisons, blind comparisons, or multi-model/tier runs.
- For this evaluator, a completed run of `examples/calibration/problems.json` plus delayed comparison against `examples/calibration/answer-key.json` counts as behavioral confidence evidence only when every fixture is evaluated read-only before answer-key inspection, the main evaluator owns final observed scores and findings, subagents are limited to evidence extraction or second-pass review, observed scores land inside the expected bands or a stronger evidence-based rationale is given, and all required findings are found or explicitly resolved.

### Novelty And Value Add

- Cap `Goal Fit And Scope Control` at about `85%` when the skill mostly restates generic model knowledge, common best practices, or instructions that would work equally well as a one-off prompt.
- Award higher scores when the skill encodes non-obvious domain procedure, team-specific preference, deterministic workflow knowledge, reusable scripts, templates, or validation logic that measurably improves outcomes.
- Treat negative or unmeasured skill impact as an explicit evaluation risk, not as unknown-neutral evidence.

### Semantic Coherence And Tradeoff Fit

Use this lens to evaluate whether the skill's instructions, resources, tools, and verification steps actually serve the skill's stated purpose. The evaluator may identify purpose-level or direction-level changes when evidence shows they are needed, but must not apply or require those changes without explicit user approval.

- Check purpose-means fit: each required step should support the stated goal, verification need, safety boundary, context strategy, or collaboration outcome.
- Flag instructions that technically satisfy a rule but undermine the reason the rule exists, such as delegating away the behavior being calibrated or validating an output with evidence that cannot test the claimed behavior.
- Evaluate cost/benefit tradeoffs for expensive steps, including context load, subagent overhead, external tool use, latency, and repeated validation. Treat cost as a defect when the skill does not justify it, when it does not materially improve confidence or safety, or when a cheaper scoped alternative would preserve the same evidence.
- Separate implementation-level fixes from direction-level changes. Implementation-level fixes can be recommended normally; direction-level changes should be framed as approval-gated recommendations.
- Treat these as direction-level changes: changing the target user, primary use case, trigger scope, output artifact type, success criteria, or core workflow ownership.
- If a direction-level change appears necessary because the stated purpose is unsafe, impossible, internally contradictory, or misaligned with the user's explicit goal, report it as a P0/P1/P2 finding but ask for user approval before patching it.

### Trigger Ecosystem Fit

- Cap `Trigger Accuracy` at about `90%` when the description is clear in isolation but was not checked against adjacent installed skills, likely user phrasing, or description truncation.
- Cap `Trigger Accuracy` at about `80%` when neighboring skills have overlapping descriptions that could cause wrong activation or hesitation.
- Give full credit only when the trigger is concise, front-loaded with key use cases, resilient to shortened descriptions, and clearly separated from nearby skills.

### Context Budget And Resource Hygiene

- Cap `Context Management` at about `85%` when `SKILL.md` is large, template-heavy, example-heavy, or contains low-frequency reference material that could move to `references/`, `assets/`, or `examples/`.
- Cap `Context Management` at about `80%` when references are deeply nested, resource files are not clearly routed, or important behavior depends on uninspected resources.
- Check for nonstandard files, duplicated content, unused assets, build artifacts, lockfiles, large schemas, and other context-window waste.
- Use this rule of thumb: under 500 lines is usually acceptable, 500-650 lines deserves review, and over 650 lines is a strong refactor signal unless the scope is unusually constrained.

### Hidden Contamination And Cross-Modal Safety

- Cap `Failure Handling And Safety` at about `75%` when scripts, references, assets, or examples are not checked for hidden instructions, prompt injection, credential access, file exfiltration, unsafe shell commands, or behavior that contradicts `SKILL.md`.
- Do not treat a benign-looking `SKILL.md` as sufficient safety evidence when executable scripts or external resources are present.
- Check consistency across natural-language instructions and executable/resource content: body, scripts, references, assets, metadata, and validation commands should support the same bounded behavior.
- For third-party or marketplace skills, report provenance, license, dependency, and registry trust assumptions when available.

### Deterministic Baseline Signals

- Cap `Tool And Resource Design` at about `90%` when repeated structural checks are described but not backed by a reusable script, checklist, or deterministic command.
- Prefer deterministic baseline checks for frontmatter validity, generic names, missing `SKILL.md`, unreferenced resources, broken resource links, oversized files, nonstandard directories, stale metadata, and unsafe validation commands.
- Deterministic checks should support qualitative judgment, not replace it.
- For this evaluator, `scripts/validate_skill.py` is the deterministic baseline for local structure, referenced resources, metadata, hidden files, and calibration problem/answer-key hygiene. Use `--skip-answer-key` before observed calibration results are drafted; use the full validator after answer-key inspection is allowed. A passed answer-key-safe run counts as structural validation evidence and should not be treated as a skipped validator, but it does not prove answer-key content hygiene unless the full validator or equivalent direct evidence also covers that content.

### Local Fit And Adoption Friction

- Cap relevant categories at about `90%` when the skill was not checked against real user phrasing, recurring task patterns, local project instructions, available CLIs/MCP tools, expected paths, aliases, or verification commands.
- Penalize unnecessary clarification loops, undertriggering, overtriggering, stale environment assumptions, and workflow steps that do not match the user's actual toolchain.

## Score Ceilings

Use these ceilings unless direct evidence supports a higher score.

### Trigger Accuracy

- Cap at about `90%` when the frontmatter description is accurate but long, dense, or likely to match too many adjacent review tasks.
- Cap at about `75%` when use cases are clear but non-use cases are missing or weak.

### Context Management

- Cap at about `85%` when `SKILL.md` contains long report templates, examples, or calibration details that are not always needed at trigger time.
- Cap at about `75%` when the skill repeatedly loads reference-like material instead of using progressive disclosure.
- Award `100%` only when the main file stays focused on always-needed behavior and optional details are moved to references or loaded on demand.

### Tool And Resource Design

- Cap at about `90%` when useful repeated checks are described but not supported by a script, checklist resource, or clearly reusable command.
- Cap at about `75%` when the skill relies on tools or validators but does not define safe execution constraints.
- Do not penalize the absence of scripts when the task is genuinely judgment-only and scripts would add little value.

### Subagent And Parallel Work Design

- Give high credit when the skill explicitly identifies independent work that can run in parallel, routes suitable branches to separate read-only subagents when available, and defines result aggregation, conflict resolution, and fallback behavior.
- Cap at about `80%` when the skill has clearly parallelizable work but keeps it serial without explaining why.
- Cap at about `90%` when subagent usage is well scoped but the fallback for unavailable subagents or reduced confidence is not explicit.
- Cap at about `75%` when the skill suggests independent review but does not define role boundaries, evidence handling, or disagreement resolution.

### Maintainability And Metadata

- Cap at about `90%` when the skill is clean as a single file but optional metadata, references, or resource organization cannot be inspected.
- Cap at about `85%` when the skill's frontmatter, UI metadata, examples, and resource layout would require duplicated updates.
- Award `100%` only when naming, metadata, references, scripts or justified script absence, and update burden are all inspected or explicitly not applicable.

## Self-Evaluation Guardrail

When a skill evaluates itself:

- Actively look for score-limiting evidence before assigning full credit.
- Do not award a final score of `100/100` if any P1 or P2 recommendation remains.
- Do not use the skill's own claims as the only evidence for a perfect category score; require inspected structure, resources, validation output, or observed behavior.
- Treat missing optional artifacts as `unknown`, but do not let unknowns support full credit.
- For a perfect final score, any P3 issue must be demonstrably non-scoring polish; otherwise it limits the relevant category.
- For this evaluator, do not use skipped calibration alone to deny `100/100`. A perfect score still requires the deterministic validator to pass or equivalent direct structural evidence, and any calibration mismatch must be resolved by stronger direct evidence when calibration was run.

## Improvement Priority

Classify improvements separately from score:

- `P0`: The skill is likely to trigger incorrectly, cause unsafe behavior, or block its core task.
- `P1`: Major reliability, verification, context, or workflow gap that should be fixed before relying on the skill.
- `P2`: Meaningful quality issue that reduces repeatability or maintainability.
- `P3`: Minor clarity, polish, or optional enhancement.

Tie every P0/P1/P2 recommendation to the rubric category it improves.
