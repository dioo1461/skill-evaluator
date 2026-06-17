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

최종 report에는 보통 총점, 신뢰도, 세부 점수, 검증 상태, 보정 상태, 우선순위별 발견 사항, 강점, 추천 변경 사항, 승인 필요한 방향 변경, 가정과 미확인 항목이 포함됩니다.

### 점수

84/100 - 전반적으로 실전형 워크플로가 잘 잡혀 있지만, 최신 저장소 구조와 검증 진입점을 더 정확히 반영해야 합니다.

### 신뢰도

중간 - `SKILL.md`, `agents/openai.yaml`, 인접 스킬 메타데이터, 대표 저장소 구조를 확인했고 로컬 검증기는 통과했습니다. 실행 추적과 전체 행동 보정은 요청 범위가 아니라 실행하지 않았습니다.

### 세부 점수

| 항목 | 점수 | 메모 |
|---|---:|---|
| 호출 정확도 | 9/12 | 호출 범위는 명확하지만 frontmatter의 비사용 경계가 더 분명하면 좋습니다. |
| 목표 적합성 및 범위 제어 | 9/10 | 목적이 구체적이고 실무 흐름에 맞습니다. |
| 워크플로 실행 가능성 | 11/14 | 주요 단계는 구체적이지만 저장소 선택과 캡처 진입점의 대체 동작이 더 명확해야 합니다. |
| 컨텍스트 관리 | 13/14 | 스킬이 간결하고 번들 리소스 비대화가 없습니다. |
| 도구 및 리소스 설계 | 8/10 | 도구 지침은 유용하지만 일부 검증 경로가 충분히 결정적이지 않습니다. |
| 서브에이전트 및 병렬 작업 설계 | 6/8 | 검토자 역할은 분리했지만 사용 가능 여부와 권한 대체 동작이 더 명확해야 합니다. |
| 검증 및 완료 기준 | 10/12 | 검증 명령과 완료 기준이 대부분 명확합니다. |
| 실패 처리 및 안전성 | 7/8 | 대체 동작은 문서화되어 있지만 작업 디렉터리 대체 동작 하나가 위험합니다. |
| 유지보수성 및 메타데이터 | 7/8 | 메타데이터는 유효하지만 일부 구조 참조를 대상 저장소와 계속 맞춰야 합니다. |
| 출력 품질 및 협업 | 4/4 | 최종 report 구조가 명확하고 읽기 쉽습니다. |

### 검증 결과

- 통과: `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/skill`
- `agents/openai.yaml` 파싱 성공
- 대상 구성: `SKILL.md`, `agents/openai.yaml`; 번들 참조 문서나 스크립트 없음

### 보정 결과

- 실행하지 않음. 일반적인 단일 스킬 산출물 평가였고, 보정된 채점이나 배포 준비 검증 요청은 아니었습니다.

### 발견 사항

- [P2] `SKILL.md:107` 구현 책임 범위를 대상 저장소의 일부 계층으로만 좁히고 있습니다.

  영향: agent가 UI 코드나 test를 잘못된 계층에 배치할 수 있습니다.

  개선: 대상 저장소의 실제 계층 구조와 테스트 배치 규칙을 반영하세요.

- [P2] `SKILL.md:60` 저장소 감지가 실패했을 때 현재 디렉터리로 대체합니다.

  영향: log나 검증 명령이 잘못된 디렉터리에서 실행될 수 있습니다.

  개선: 구현 작업에는 유효한 작업트리를 요구하거나 사용자에게 선택을 요청하세요.

- [P2] `SKILL.md:134` 스크린샷 캡처는 설명하지만 안정적인 대상 화면 진입 전략이 없습니다.

  영향: agent가 화면에 일관되게 진입하지 못하고 약한 검증으로 너무 빨리 대체할 수 있습니다.

  개선: 결정적 route, 개발 화면, 사용자 보조 navigation, 좌표 입력 순서의 짧은 decision tree를 추가하세요.

### 강점

- 산출물 log 구조와 비교 template이 명확합니다.
- blank 또는 non-hydrated screenshot 처리 지침이 좋습니다.
- 검증 명령이 명시적이고 다시 실행하기 쉽습니다.

### 추천 변경 사항

1. ownership과 테스트 배치 지침을 현재 대상 저장소 구조에 맞추세요.
2. 구현 또는 log 생성 전에 작업트리 guard를 추가하세요.
3. 결정적인 스크린샷 대상 화면 진입 지침을 추가하세요.
4. 서브에이전트 사용 가능 여부와 권한 대체 동작 표현을 명확히 하세요.

### 승인 필요한 방향 변경

- 없음.

### 가정 / 확인하지 못한 부분

- 대표 저장소 구조는 확인했지만 모든 branch나 runtime path를 확인하지는 않았습니다.
- live UI loop나 runtime trace는 실행하지 않았습니다.
