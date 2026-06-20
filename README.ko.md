# Skill Evaluator

[English](README.md)

Skill Evaluator는 기존 Codex skill 구현을 평가하기 위한 Codex skill입니다. 스킬이 적절한 상황에서 호출되는지, 지침이 실행 가능한지, 컨텍스트를 낭비하지 않는지, 검증 가능한 결과를 내는지 점수와 개선 제안으로 정리합니다.

## 주요 기능

- 기존 Codex skill 디렉터리, 단일 `SKILL.md`, diff, commit, PR, 실행 trace를 평가합니다.
- 100점 만점의 rubric으로 점수를 산출합니다.
- P0/P1/P2/P3 우선순위로 개선점을 정리합니다.
- 기본적으로 평가 대상 파일은 수정하지 않습니다.
- 사용자가 명시적으로 요청한 경우에만 patch나 개선 사항을 적용합니다.
- `/goal` 목표 점수 루프를 지원해 평가, 패치, 검증을 반복하고 목표 점수에 도달하거나 blocker를 만나면 멈춥니다.
- patch mode에서 로컬 skill artifact를 수정하기 전에 timestamp가 포함된 백업을 만듭니다.

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

이후 Codex를 새로 시작하거나 skill 목록을 다시 로드한 뒤 `$skill-evaluator`를 호출합니다.

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

특정 점수에 도달할 때까지 검증-개선 루프를 반복하려면 Codex의 `/goal`을 사용합니다. Goal loop에서는 `$skill-evaluator`가 시작 점수를 기록하고, patch가 허용된 경우 scoped P0/P1/P2 수정 사항을 적용한 뒤 다시 검증합니다. 목표 점수에 도달하거나, 더 이상 안전한 scoped fix가 없거나, direction-level change에 사용자 승인이 필요하거나, 검증을 실행할 수 없거나, 다른 blocker가 발견될 때까지 반복합니다.

Subagent를 사용할 수 있는 환경이라면 매 검증 pass마다 fresh read-only evaluator subagent를 사용합니다. Subagent는 evidence, score, recommendation만 반환하고, main agent가 파일 수정, 최종 점수 판단, 충돌 해결을 맡습니다.

```text
/goal Use $skill-evaluator to evaluate ./my-skill and improve it until it reaches at least {원하는 점수}/100. For every validation pass, launch a fresh read-only subagent, apply the recommended fixes, and repeat the loop until the target score is reached or a blocker is found.
```

간단한 compact form도 지원합니다.

```text
/goal $skill-evaluator target: ./my-skill objective: 95
/goal $skill-evaluator path: ./my-skill score: 99
/goal Use $skill-evaluator to improve ./my-skill until 95/100
```

숫자만 제공된 경우에는 local skill path, pasted skill, 또는 최근 대화에서 평가하던 skill이 정확히 하나로 명확할 때만 평가 범위를 추론합니다. 범위가 모호하면 Codex가 target path나 content를 한 번 물어봅니다.

## 패치 백업

`$skill-evaluator`가 로컬 skill artifact를 수정할 때는 첫 편집 전에 timestamp가 포함된 백업을 만듭니다. 백업은 평가 대상 skill 디렉터리 밖에 저장하며, 가능한 경우 다음 위치를 사용합니다.

```text
$CODEX_HOME/skill-backups/<skill-name>/<timestamp>/
```

`$CODEX_HOME`을 사용할 수 없으면 다음 위치로 fallback합니다.

```text
~/.codex/skill-backups/<skill-name>/<timestamp>/
```

백업은 수정되는 파일의 relative path를 보존합니다. 수정 범위가 넓거나 불확실하면 전체 skill 디렉터리를 백업할 수 있습니다. 백업 생성이 실패하면 pasted content, remote-only artifact, local source file이 없는 diff, 또는 사용자가 명시적으로 백업 없이 진행을 승인한 경우가 아닌 한 로컬 artifact를 수정하지 않습니다. 최종 patch summary에는 백업 경로, 백업 생략 사유, 또는 백업 실패가 보고됩니다.

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

## 보정(Calibration)

보정은 선택 기능입니다. `skill-evaluator` 자체가 스킬을 일관되게 채점하는지 확인하고 싶을 때 사용합니다. 일반적인 스킬 평가나 개선 작업에서는 보통 필요하지 않습니다.

다음 상황에서는 사용자가 명시적으로 보정을 요청하는 것이 좋습니다.

- 평가기 자체 점검이 필요할 때
- 평가기 변경 사항을 배포하기 전에 배포 준비 상태를 확인할 때
- 100/100처럼 높은 점수를 주장하기 전에 평가 신뢰도를 함께 확인하고 싶을 때

요청할 때는 다음처럼 적을 수 있습니다.

```text
Use $skill-evaluator to run a calibrated self-test for this evaluator.
```

보정을 실행할 때는 정답 키를 먼저 열지 않아야 합니다. 먼저 fixture 평가 결과를 확정한 뒤 `skill-evaluator/examples/calibration/answer-key.json`과 비교해야 합니다.

## 평가 결과 예시

최종 report에는 보통 score, confidence, breakdown, validation result, calibration result, findings, strengths, recommended changes, approval-gated direction changes, assumptions가 포함됩니다. 한국어 report에서도 이런 구조 heading은 영어로 유지하고, 판단과 설명은 한국어로 작성됩니다.

### Score

84/100 - 전반적으로 실전형 workflow가 잘 잡혀 있지만, 최신 repository 구조와 검증 진입점을 더 정확히 반영해야 합니다.

### Confidence

Medium - `SKILL.md`, `agents/openai.yaml`, 인접 skill metadata, 대표 repository 구조를 확인했고 local validator는 통과했습니다. runtime trace와 전체 behavioral calibration은 요청 범위가 아니라 실행하지 않았습니다.

### Breakdown

| Category | Score | Notes |
|---|---:|---|
| Trigger Accuracy | 9/12 | trigger 범위는 명확하지만 frontmatter의 non-use 경계가 더 분명하면 좋습니다. |
| Goal Fit And Scope Control | 9/10 | 목적이 구체적이고 실무 흐름에 맞습니다. |
| Workflow Executability | 11/14 | 주요 단계는 구체적이지만 repository 선택과 capture 진입점 fallback이 더 명확해야 합니다. |
| Context Management | 13/14 | skill이 lean하고 bundled resource bloat가 없습니다. |
| Tool And Resource Design | 8/10 | tool 지침은 유용하지만 일부 검증 경로가 충분히 deterministic하지 않습니다. |
| Subagent And Parallel Work Design | 6/8 | reviewer 역할은 분리했지만 사용 가능 여부와 권한 fallback이 더 명확해야 합니다. |
| Verification And Completion Criteria | 10/12 | 검증 명령과 완료 기준이 대부분 명확합니다. |
| Failure Handling And Safety | 7/8 | fallback은 문서화되어 있지만 working directory fallback 하나가 위험합니다. |
| Maintainability And Metadata | 7/8 | metadata는 유효하지만 일부 구조 참조를 target repo와 계속 맞춰야 합니다. |
| Output Quality And Collaboration | 4/4 | 최종 report 구조가 명확하고 읽기 쉽습니다. |

### Validation Result

- 통과: `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/skill`
- `agents/openai.yaml` 파싱 성공
- 대상 구성: `SKILL.md`, `agents/openai.yaml`; bundled references/scripts 없음

### Calibration Result

- 실행하지 않음. 일반적인 단일 skill artifact 평가였고, calibrated scoring이나 release-readiness 검증 요청은 아니었습니다.

### Findings

- [P2] `SKILL.md:107` implementation ownership을 target repository의 일부 layer로만 좁히고 있습니다.

  Impact: agent가 UI 코드나 test를 잘못된 layer에 배치할 수 있습니다.

  Improvement: target repository의 실제 layer map과 test-placement convention을 반영하세요.

- [P2] `SKILL.md:60` repository detection이 실패했을 때 current directory로 fallback합니다.

  Impact: log나 validation command가 잘못된 디렉터리에서 실행될 수 있습니다.

  Improvement: implementation task에는 유효한 worktree를 요구하거나 사용자에게 선택을 요청하세요.

- [P2] `SKILL.md:134` screenshot capture는 설명하지만 stable target-screen entry 전략이 없습니다.

  Impact: agent가 화면에 일관되게 진입하지 못하고 약한 검증으로 너무 빨리 fallback할 수 있습니다.

  Improvement: deterministic route, dev screen, user-assisted navigation, coordinate input 순서의 짧은 decision tree를 추가하세요.

### Strengths

- artifact log 구조와 comparison template이 명확합니다.
- blank 또는 non-hydrated screenshot 처리 지침이 좋습니다.
- 검증 명령이 명시적이고 다시 실행하기 쉽습니다.

### Recommended Changes

1. ownership과 test-placement 지침을 현재 target repository 구조에 맞추세요.
2. implementation 또는 log 생성 전에 worktree guard를 추가하세요.
3. deterministic screenshot target-entry 지침을 추가하세요.
4. subagent 사용 가능 여부와 권한 fallback 표현을 명확히 하세요.

### Approval-Gated Direction Changes

- 없음.

### Assumptions / Unknowns

- 대표 repository 구조는 확인했지만 모든 branch나 runtime path를 확인하지는 않았습니다.
- live UI loop나 runtime trace는 실행하지 않았습니다.
