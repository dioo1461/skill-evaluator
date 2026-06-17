# Report Format

Load this before writing the final evaluation report unless the user asks for another format.

Match the final report language to the user's language unless the user requests a specific language. If the user writes in Korean, localize report headings, table headers, category labels, and finding labels into Korean instead of emitting English-only headings. Keep paths, commands, file names, priority labels such as `P1`, and product names verbatim.

Use the English template below for English reports:

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

Use the Korean template below for Korean reports:

```markdown
**점수**
<N>/100 - <짧은 평가>

**신뢰도**
- <높음|중간|낮음> - <근거 요약. 행동 보정 실행 여부, 생략 여부, 해당 없음 여부 포함>

**세부 점수**
| 항목 | 점수 | 메모 |
|---|---:|---|
| 호출 정확도 | <x>/12 | <근거가 있는 짧은 메모> |
| 목표 적합성 및 범위 제어 | <x>/10 | <메모> |
| 워크플로 실행 가능성 | <x>/14 | <메모> |
| 컨텍스트 관리 | <x>/14 | <메모> |
| 도구 및 리소스 설계 | <x>/10 | <메모> |
| 서브에이전트 및 병렬 작업 설계 | <x>/8 | <메모> |
| 검증 및 완료 기준 | <x>/12 | <메모> |
| 실패 처리 및 안전성 | <x>/8 | <메모> |
| 유지보수성 및 메타데이터 | <x>/8 | <메모> |
| 출력 품질 및 협업 | <x>/4 | <메모> |

**검증 결과**
- <검증기/수동 확인 상태, 실행한 명령, 핵심 출력, 대체 확인>
- <큰 참조 문서나 리소스 폴더를 일부만 확인했다면 표본 확인 또는 미확인 항목>

**보정 결과**
- <보정이 필요 없었는지, 생략했는지, 실행하지 않았는지, 완료했는지 명시. 실행했다면 fixture ID, 서브에이전트 사용 방식, 주 평가자의 최종 관찰 점수/발견 사항 소유 여부, 정답 키 확인 지연 여부, 예상 점수 범위, 관찰 점수 범위, 필수 발견 사항 일치 여부, 생략 및 불일치 포함>

**발견 사항**
- [P1] <file:line> <문제 요약>
  영향: <왜 중요한지>
  개선: <구체적인 변경>

**강점**
- <근거가 있는 구체적인 강점>

**추천 변경 사항**
1. <가장 효과가 큰 변경>
2. <다음 변경>
3. <다음 변경>

**승인 필요한 방향 변경**
- <사용자의 명시적 승인 없이 적용하면 안 되는 방향 변경. 없으면 없음이라고 명시>

**가정 / 확인하지 못한 부분**
- <누락된 artifact, 미검증 동작, scope 제한>
```

Keep findings concrete. Do not list low-value suggestions just to fill the report. If there are no P0/P1/P2 findings, say so directly. For Korean reports, localize that no-findings sentence as well, for example: `P0/P1/P2 발견 사항은 없습니다.`

## Comparative Evaluation

When comparing multiple skills:

- Score each skill independently using the same rubric.
- Add a compact comparison table with final score, strongest area, weakest area, and top fix. For Korean reports, use Korean table headers such as `스킬`, `최종 점수`, `가장 강한 영역`, `가장 약한 영역`, and `최우선 수정`.
- Avoid normalizing scores to make the set look evenly distributed; absolute quality matters.
