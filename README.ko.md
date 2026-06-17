# Skill Evaluator

[English](README.md)

Skill Evaluator는 기존 Codex skill 구현을 평가하기 위한 Codex skill입니다. 스킬이 적절한 상황에서 호출되는지, 지침이 실행 가능한지, 컨텍스트를 낭비하지 않는지, 검증 가능한 결과를 내는지 점수와 개선 제안으로 정리합니다.

## 주요 기능

- 기존 Codex skill 디렉터리, 단일 `SKILL.md`, diff, commit, PR, 실행 trace를 평가합니다.
- 100점 만점의 rubric으로 점수를 산출합니다.
- P0/P1/P2/P3 우선순위로 개선점을 정리합니다.
- 기본적으로 평가 대상 파일은 수정하지 않습니다.
- 사용자가 명시적으로 요청한 경우에만 patch나 개선 사항을 적용합니다.

## 사용하면 좋은 경우

- 새로 만든 Codex skill을 공유하거나 배포하기 전에 품질을 점검할 때
- 기존 skill의 trigger, workflow, references, metadata가 적절한지 확인할 때
- 여러 skill을 같은 rubric으로 비교할 때
- 리뷰 코멘트, diff, 실행 trace를 바탕으로 skill 동작 문제를 분석할 때
- 명시적으로 요청한 개선 사항을 안전하게 반영하고 싶을 때

## 사용하지 않는 경우

- 새로운 skill을 처음부터 설계하거나 작성하는 작업
- 일반적인 코드 리뷰, 문서 리뷰, 제품 기획 리뷰
- skill이 아닌 일반 애플리케이션 코드 평가
- 사용자가 요청하지 않은 방향 전환이나 대규모 리팩터링

## 구성

- `README.md`: 영어 프로젝트 문서
- `README.ko.md`: 한국어 프로젝트 문서
- `skill-evaluator/`: 설치 가능한 Codex skill package
- `skill-evaluator/SKILL.md`: 스킬의 핵심 지침과 평가 기준
- `skill-evaluator/agents/openai.yaml`: Codex에서 보이는 표시 정보
- `skill-evaluator/references/`: report 형식, scoring guide, patch mode, checklist
- `skill-evaluator/scripts/validate_skill.py`: 읽기 전용 구조 검증 스크립트
- `skill-evaluator/examples/calibration/`: evaluator 자체 점검용 예시

## 설치

이 저장소를 임시 디렉터리에 clone한 뒤, 실제 skill package 디렉터리만 Codex skills 디렉터리에 복사하고 임시 clone은 삭제합니다.

```bash
tmpdir=$(mktemp -d)
git clone https://github.com/dioo1461/skill-evaluator.git "$tmpdir"
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/skill-evaluator
cp -R "$tmpdir/skill-evaluator" ~/.codex/skills/skill-evaluator
rm -rf "$tmpdir"
```

이미 설치한 경우에도 같은 설치 명령을 다시 실행하면 됩니다.

이후 Codex를 새로 시작하거나 skill 목록을 다시 로드한 뒤 `$skill-evaluator`를 호출합니다. 설치된 skill 디렉터리에는 `~/.codex/skills/skill-evaluator/SKILL.md`가 직접 있어야 합니다.

## 사용 예시

단일 skill 디렉터리를 평가합니다.

```text
Use $skill-evaluator to score /path/to/my-skill.
```

여러 skill을 비교합니다.

```text
Use $skill-evaluator to compare ./skill-a and ./skill-b.
```

평가 후 개선 사항까지 적용합니다.

```text
Use $skill-evaluator to evaluate ./my-skill and apply the P1/P2 fixes.
```

PR이나 diff를 평가합니다.

```text
Use $skill-evaluator to review this skill diff and report validation status.
```

## 목표 점수까지 반복 개선

특정 점수에 도달할 때까지 검증-개선 루프를 반복하려면 Codex의 `/goal`을 사용합니다. 검증은 매번 fresh read-only subagent가 맡고, main agent는 개선 사항 적용과 결과 통합을 담당하게 요청하세요.

```text
/goal Use $skill-evaluator to evaluate ./my-skill and improve it until it reaches at least {원하는 점수}/100. For every validation pass, launch a fresh read-only subagent, apply the recommended fixes, and repeat the loop until the target score is reached or a blocker is found.
```

예를 들어 90점 이상을 목표로 할 수 있습니다.

```text
/goal Use $skill-evaluator to evaluate ./my-skill and improve it until it reaches at least 90/100. For every validation pass, launch a fresh read-only subagent, apply the recommended fixes, and repeat the loop until the target score is reached or a blocker is found.
```

## 검증

일반적인 구조 검증은 다음 명령으로 충분합니다.

```bash
python3 skill-evaluator/scripts/validate_skill.py skill-evaluator --skip-answer-key
```

Evaluator calibration 파일까지 확인해야 할 때만 전체 검증을 실행합니다.

```bash
python3 skill-evaluator/scripts/validate_skill.py skill-evaluator
```

Codex system skill validator가 설치되어 있다면 추가로 실행할 수 있습니다.

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-evaluator
```

## Calibration

Calibration은 선택 기능입니다. `skill-evaluator` 자체가 skill을 일관되게 채점하는지 확인하고 싶을 때 사용합니다. 일반적인 skill 평가나 개선 작업에서는 보통 필요하지 않습니다.

다음 상황에서는 사용자가 명시적으로 calibration을 요청하는 것이 좋습니다.

- evaluator self-test가 필요할 때
- evaluator 변경 사항을 배포하기 전에 release-readiness를 확인할 때
- 100/100처럼 높은 점수를 주장하기 전에 평가 신뢰도를 함께 확인하고 싶을 때

요청할 때는 다음처럼 적을 수 있습니다.

```text
Use $skill-evaluator to run a calibrated self-test for this evaluator.
```

Calibration을 실행할 때는 answer key를 먼저 열지 않아야 합니다. 먼저 fixture 평가 결과를 확정한 뒤 `skill-evaluator/examples/calibration/answer-key.json`과 비교해야 합니다.

## 평가 결과 예시

최종 report에는 보통 총점, confidence, category별 점수, validation 상태, 우선순위별 finding, 추천 변경 사항, assumptions가 포함됩니다.

```markdown
**점수**
86/100 - 전반적으로 강한 skill이지만 몇 가지 신뢰성 보완이 필요합니다.

**신뢰도**
중간 - 로컬 검증은 통과했지만 behavioral calibration은 실행하지 않았습니다.

**분류별 점수**
| 항목 | 점수 | 메모 |
|---|---:|---|
| Trigger Accuracy | 10/12 | 사용 조건과 비사용 조건이 명확합니다. |
| Workflow Executability | 11/14 | 주요 흐름은 구체적이지만 일부 분기에서 fallback 동작이 더 명확해야 합니다. |
| Verification And Completion Criteria | 9/12 | 검증 방법은 문서화되어 있지만 patch 후 완료 기준이 더 구체적이면 좋습니다. |

**검증 결과**
- `python3 skill-evaluator/scripts/validate_skill.py skill-evaluator --skip-answer-key`: 통과
- `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill-evaluator`: 통과

**Findings**
- [P2] `SKILL.md:42` workflow가 참조 파일을 확인하라고 안내하지만, 참조 파일이 없을 때 어떻게 처리할지 정의하지 않습니다.
  영향: 평가 report가 누락된 optional resource를 일관되지 않게 다룰 수 있습니다.
  개선: optional resource와 required resource가 없을 때의 fallback 규칙을 분리해 추가하세요.

**추천 변경 사항**
1. 누락된 참조 파일에 대한 fallback 동작을 명확히 하세요.
2. patch mode의 완료 조건 checklist를 짧게 추가하세요.

**가정 / 확인하지 못한 부분**
- 이번 실행에서는 behavioral calibration을 요청하지 않았습니다.
```
