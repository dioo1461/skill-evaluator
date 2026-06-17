# Evaluation Checklist

Use this checklist before finalizing an evaluation report, and again after edits in patch mode.

- Scope is resolved, including whether the target is a directory, single file, diff/PR, comparison set, pasted content, or runtime trace.
- `SKILL.md` frontmatter and body were inspected; `agents/openai.yaml` and top-level resources were inspected or explicitly marked unavailable/not applicable.
- Required references from the evaluated skill were loaded only when needed, and any sampled or skipped resources are named in the report.
- Safe validation was run when available, or manual structural checks were performed and reported.
- For this evaluator or any target with a bundled validator, the read-only local validator was run with a timeout or a skip reason and equivalent manual evidence were reported. For this evaluator, `--skip-answer-key` was used before observed calibration results were drafted, and the full validator was used only after answer-key inspection was allowed.
- Calibration status is explicit: not run, skipped by design, not applicable, or completed. If completed, `examples/calibration/problems.json` was inspected first; the main evaluator owned final observed fixture scores/findings; subagents, when used, were limited to read-only evidence extraction or second-pass review; observed fixture scores/findings were drafted before `examples/calibration/answer-key.json` was opened; and each fixture's score band and required findings were checked or any skip/mismatch was reported.
- Every material finding has file/line, command output, trace, or other direct evidence.
- Assumptions, unknowns, unavailable resources, and tool failures are separated from confirmed defects.
- Category scores add up to the final score, not-applicable category weight was redistributed instead of scored as zero, and each score respects the scoring guide ceilings and category anchors.
- A score-limiting pass checked for missing behavioral evidence, absent baseline comparison, generic low-novelty guidance, trigger overlap, oversized or under-split context, uninspected resources, hidden contamination, cross-modal safety gaps, missing deterministic checks, and local-environment mismatch.
- Semantic coherence was checked: purpose-means fit, cost/benefit tradeoffs, and whether any recommendation changes the target user, primary use case, trigger scope, output artifact type, success criteria, or core workflow ownership.
- Direction-level changes were separated from implementation-level fixes and were reported as approval-gated recommendations unless the user explicitly approved that direction change.
- Every P0/P1/P2 recommendation maps to a rubric category.
- For self-evaluation, an independent subagent pass was used when available, or the current run was explicitly identified as the delegated independent subagent pass; if not, a non-independent second pass and residual risk are reported.
- A final `100/100` has no unresolved P1/P2 recommendation, no scoring-relevant P3 issue, no unaccounted validation gap, and no unknown artifact needed to support full credit.
- A final `100/100` for this evaluator has no unexplained deterministic validator failure, calibration mismatch when calibration was run, hidden file, stale metadata, broken resource reference, or other score-limiting evidence.
