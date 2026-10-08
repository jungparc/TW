# task-guide

트러블슈팅·How-to 가이드 원본을 두는 디렉터리입니다. GitBook Git Sync로 사이트에 게시됩니다.

## 디렉터리 구조

```
task-guide/
├── gitbook-docs.yaml   # GitBook 사이트 구조 설정 (GitBook이 관리)
├── README.md           # 이 파일. 게시되지 않습니다
└── ko/                 # 동기화 대상. 이 아래만 사이트에 올라갑니다
    ├── README.md       # 사이트 랜딩 페이지
    ├── SUMMARY.md      # 사이드바 목록
    ├── *.md            # 가이드 문서
    └── images/         # 문서에 쓰는 이미지
```

언어별로 디렉터리를 나눕니다. 번역본은 **원문과 같은 파일명**으로 해당 언어 디렉터리에 둡니다. 당분간 `ko`만 채워집니다.

## GitBook Git Sync 설정

GitBook의 **Project directory**가 `task-guide`로 지정되어 있습니다. 그래서 설정 파일이 저장소 루트가 아니라 이 디렉터리에 있고, `content.directory`의 `./ko`도 `task-guide` 기준 상대 경로입니다.

```yaml
$schema: https://api.gitbook.com/gitbook-docs.yaml
site:
  title: NHN Cloud Task Guides
  structure:
    - type: space
      key: space-task-guide-ko
      title: Task Guide
      path: task-guide
      content:
        directory: ./ko
        language: ko
```

### 주의할 점

- **`gitbook-docs.yaml`에 주석을 달지 않습니다.** GitBook이 동기화할 때마다 자기 상태에서 이 파일을 다시 생성하면서 주석을 전부 지웁니다. 설정에 관한 메모는 이 파일(`task-guide/README.md`)에 적습니다.
- **`key` 값은 동기화 이후에 바꾸지 않습니다.** GitBook이 스페이스를 식별하는 값이라, 바꾸면 기존 스페이스가 아니라 새 스페이스가 만들어집니다.
- **`default: true`는 파일 전체에서 하나만 둡니다.**
- **랜딩 페이지와 사이드바는 이 파일이 결정하지 않습니다.** 각각 `ko/README.md`와 `ko/SUMMARY.md`가 결정합니다. 문서를 추가하면 `ko/SUMMARY.md`에 항목을 넣어야 사이드바에 나타납니다.
- **GitBook 쪽에서 편집하면 저장소로 커밋이 되돌아옵니다**(`GITBOOK-SITE: ...`). 푸시가 거부되면 원격 커밋을 먼저 확인하세요.

### 언어별 스페이스 추가

번역본이 생기면 `structure` 아래에 스페이스를 추가합니다. `key`는 파일 전체에서 유일해야 합니다.

```yaml
    - type: space
      key: space-task-guide-en
      title: Task Guide
      path: task-guide-en
      content:
        directory: ./en
        language: en
```

## 문서 작성

- 파일명은 영소문자 kebab-case로 씁니다. 예: `instance-creation-failed.md`
- **번호 접두사(`01-`, `03_`)를 쓰지 않습니다.** 문서가 늘거나 순서가 바뀔 때마다 전체를 리네임해야 하고, 링크가 깨집니다. 순서는 `ko/SUMMARY.md`가 정합니다.
- **`_final`, `_latest`, `_draft` 같은 상태 접미사를 쓰지 않습니다.** 버전은 Git이 관리합니다. 검토 중이라는 사실은 PR로 나타냅니다.
- 문서 간 링크는 상대 경로를 씁니다.

### 이미지

- `ko/images/`에 두고 상대 경로로 참조합니다.

  ```markdown
  ![인스턴스 생성 실패 원인 판단 흐름](images/instance-creation-failed-flow.svg)
  ```

- 파일명은 `<문서 파일명>-<역할>` 형식을 씁니다. 예: `instance-creation-failed-flow.svg`
- **다이어그램은 SVG로 만듭니다.** 확대해도 깨지지 않고, 텍스트가 diff에 남아 문구 수정 이력을 추적할 수 있습니다.
- **콘솔 화면을 찍은 스크린숏은 PNG를 씁니다.** 스크린숏은 SVG로 만들 수 없습니다.
- 다이어그램을 **PNG로 내보내 써야 하는 경우에도 SVG 원본을 함께 커밋합니다.** PNG만 남기면 나중에 규격이 달라졌을 때 처음부터 다시 그려야 합니다.
- 다이어그램 색상은 [NHN Cloud 브랜드 가이드](https://www.nhncloud.com/kr/intro/brand-guide)를 따릅니다. BLUE `#125DE6`, NAVY `#003087`, GRAY `#586F81`, LIGHT GRAY `#BED0DE`.
- 폰트는 배포 대상 PC에 없을 수 있으므로 범용 폰트(NanumSquare, Noto Sans KR)를 지정합니다.

## 여러 명이 함께 쓰는 규칙

- **한 PR에는 문서 하나만** 담습니다. 기술 검토 담당자가 달라지므로 섞으면 리뷰가 지연됩니다.
- 제작 계획의 작업 단계와 다음과 같이 맞춥니다.

  | 작업 단계 | 어떻게 |
  | --- | --- |
  | 1. 초안 작성 | master에 바로 커밋합니다. 여러 번 고쳐 쓰는 단계라 PR을 열지 않습니다 |
  | 2. 기술 검토 요청 | PR을 올립니다. 검토 자체는 사내 두레이 태스크에서 진행하고, PR은 원본과 이력을 보관합니다 |
  | 3. 최종본 작성 | 검토 의견 반영 커밋 추가 + 반영 내역 요약을 PR 코멘트로 |
  | 4. 완료·배포 대기 | 머지 |

### 기술 검토는 두레이 프로젝트에서

유관 부서와의 기술 검토는 별도의 두레이 프로젝트에서 진행합니다. 검토 과정에서 고객 문의 사례, 리소스 ID, 내부 로그처럼 공개할 수 없는 자료를 주고받아야 하고, 유관 부서의 업무 채널도 그쪽이기 때문입니다.

저장소에는 **결론만 남깁니다.**

- 검토가 끝나면 **무엇이 지적되어 무엇을 고쳤는지** 요약을 PR 코멘트로 남깁니다. 문서 변경과 그 이유가 함께 남아야 나중에 이관하거나 재검토할 때 근거를 다시 찾지 않습니다.
- **공개 저장소이므로 PR 코멘트에도 고객사명, 리소스 ID, 두레이 링크를 쓰지 않습니다.** 요약은 사내 정보를 빼고 판단과 결과만 적습니다.
- 작성자는 **GitHub 핸들**로 적습니다. 공개 저장소이므로 실명을 새로 노출하지 않고, 리뷰 요청 시 그대로 멘션할 수 있습니다.

## 브랜치와 커밋

저장소 공통 규칙을 따릅니다. [루트 README](../README.md#브랜치와-커밋)를 참고하세요.

- 브랜치 예: `docs/task-guide/instance-creation-failed`
- 커밋 예: `docs(task-guide): 인스턴스 생성 실패 트러블슈팅 가이드 추가`

## Pull Request

기술 검토를 요청하는 PR은 **검토가 필요한 항목을 명시적으로 적습니다.** 그래야 리뷰어가 담당 범위만 보면 됩니다.

```markdown
## 문서 목적
문서 주제를 포함하여 어떤 목적을 위한 문서인지

## 검토 요청 범위
기술 정확성 / 용어 / 절차 재현성 등 무엇을 봐 주셨으면 하는지
```
