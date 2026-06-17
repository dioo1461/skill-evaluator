# Report Format

Load this before writing the final evaluation report unless the user asks for another format.

```markdown
**Score**
<N>/100 - <short verdict>

**Confidence**
- <high|medium|low> - <short basis, including whether behavioral calibration was run, skipped by design, or not relevant>

**Breakdown**
| Category | Score | Notes |
|---|---:|---|
| Trigger Accuracy | <x>/12 | <short evidence-backed note> |
| Goal Fit And Scope Control | <x>/10 | <note> |
| Workflow Executability | <x>/14 | <note> |
| Context Management | <x>/14 | <note> |
| Tool And Resource Design | <x>/10 | <note> |
| Subagent And Parallel Work Design | <x>/8 | <note> |
| Verification And Completion Criteria | <x>/12 | <note> |
| Failure Handling And Safety | <x>/8 | <note> |
| Maintainability And Metadata | <x>/8 | <note> |
| Output Quality And Collaboration | <x>/4 | <note> |

**Validation Result**
- <validator/manual check status, command when run, key output, and any fallback checks>
- <sampled or uninspected resources, if large references or resource folders were only partially inspected>

**Calibration Result**
- <say not run/skipped by design/not applicable when calibration was not needed; when run, include fixture ids evaluated, how subagents were used, whether the main evaluator owned final observed scores/findings, whether answer-key inspection was delayed until observed results were drafted, expected score bands, observed score bands, required finding matches, skips, and mismatches>

**Findings**
- [P1] <file:line> <issue summary>
  Impact: <why it matters>
  Improvement: <specific change>

**Strengths**
- <specific strength with evidence>

**Recommended Changes**
1. <highest-leverage change>
2. <next change>
3. <next change>

**Approval-Gated Direction Changes**
- <direction-level change that should not be applied without explicit user approval; say none when not applicable>

**Assumptions / Unknowns**
- <missing artifact, unverified behavior, or scope limit>
```

Keep findings concrete. Do not list low-value suggestions just to fill the report. If there are no P0/P1/P2 findings, say so directly.

## Comparative Evaluation

When comparing multiple skills:

- Score each skill independently using the same rubric.
- Add a compact comparison table with final score, strongest area, weakest area, and top fix.
- Avoid normalizing scores to make the set look evenly distributed; absolute quality matters.
