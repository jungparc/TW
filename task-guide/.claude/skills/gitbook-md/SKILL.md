---
name: gitbook-md
description: 초안 Markdown 문서를 GitBook 문법(hint, code, tabs, stepper, expandable, content-ref, figure)으로 변환하거나 GitBook용 문서를 새로 작성할 때 사용합니다.
---

# GitBook 문법 적용

초안 `.md`를 GitBook에 그대로 붙여 넣을 수 있는 GitBook-flavored Markdown으로 변환한다.

## 원칙

1. **본문 텍스트는 한 글자도 바꾸지 않는다.** 문법 래핑만 한다. 오탈자 수정·문장 다듬기는 사용자가 명시적으로 요청할 때만.
2. 표준 Markdown으로 충분한 것(제목, 목록, 표, 인라인 코드, 굵게/기울임)은 그대로 둔다. GitBook은 CommonMark를 지원한다.
3. 확신이 없는 블록은 변환하지 말고 원본을 유지한 뒤, 변환 후 보고에서 "판단이 필요한 블록"으로 따로 알린다.
4. 변환 결과는 원본과 같은 파일명으로 새 파일에 쓴다. 원본은 덮어쓰지 않는다(사용자가 in-place 수정을 요청한 경우 제외).

## 변환 규칙

### 1. 블록인용문 → hint

인용문(`>`)의 첫 줄 라벨로 스타일을 결정한다. 이모지(💡, ⚠️ 등)는 제거한다 — GitBook이 스타일별 아이콘을 자동으로 붙인다. 라벨 텍스트(**알아두기**, **주의**)는 유지한다.

| 초안 라벨 | GitBook 스타일 |
|---|---|
| 알아두기, 참고, 팁, Note, Tip | `info` |
| 주의, 경고, Warning, Caution | `warning` |
| 위험, 삭제, 복구 불가, Danger | `danger` |
| 완료, 성공, 권장 | `success` |
| 라벨 없는 일반 인용문 | `info` |

라벨이 없는 인용문을 `info`로 올리는 이유: GitBook의 `>`는 "인용"으로 렌더링되므로 보충 설명에는 어울리지 않는다. 단, 실제 남의 말·문서를 인용한 것이라면 `>`를 유지한다.

```
{% hint style="info" %}
**알아두기**

본문 내용.
{% endhint %}
```

```
{% hint style="warning" %}
**주의**

본문 내용.
{% endhint %}
```

hint 안에는 문단, 목록, 제목, 인라인 이미지를 넣을 수 있다. 여러 문단이면 원본의 문단 구분을 그대로 유지한다.

초안이 GitHub 전용 alert 문법(`> [!NOTE]`)으로 쓰여 있으면 라벨을 다음과 같이 매핑한다. GitHub alert는 GitBook에서 강조 박스로 렌더링되지 않고 `[!NOTE]` 문자열이 그대로 노출되므로 반드시 변환한다.

| GitHub alert | GitBook 스타일 |
|---|---|
| `[!NOTE]`, `[!IMPORTANT]` | `info` |
| `[!TIP]` | `success` |
| `[!WARNING]` | `warning` |
| `[!CAUTION]` | `danger` |

### 2. 코드 블록

기본은 일반 fenced code block을 그대로 둔다. 다음 경우에만 `{% code %}`로 감싼다.

- 파일명이나 캡션이 필요할 때 → `title="nginx.conf"`
- 한 줄이 매우 길어 가로 스크롤이 생길 때 → `overflow="wrap"`
- 줄 번호로 특정 줄을 지목해 설명할 때 → `lineNumbers="true"`

`{% code title="nginx.conf" overflow="wrap" lineNumbers="true" %}` … `{% endcode %}` 형태로, 여는 태그와 코드 펜스 사이에 빈 줄을 둔다.

### 3. 이미지 → figure

`alt` 텍스트가 설명형이면 캡션으로 승격한다.

```
<figure><img src="images/diagram.svg" alt="대체 텍스트"><figcaption><p>캡션</p></figcaption></figure>
```

장식용 이미지나 캡션이 불필요한 경우에는 `![alt](src)`를 그대로 둔다.

### 4. 탭 (선택)

OS·언어·콘솔/CLI처럼 **같은 목적의 대안 경로**가 나란히 있을 때만 쓴다.

```
{% tabs %}

{% tab title="콘솔" %} 콘솔 절차 {% endtab %}

{% tab title="CLI" %} CLI 절차 {% endtab %}

{% endtabs %}
```

### 5. 스테퍼 (선택, 기본 미적용)

순서 있는 목록은 기본적으로 그대로 둔다. 한 문서에 절차가 하나뿐이고 각 단계가 길 때(코드·스크린샷 포함)만 스테퍼를 제안한다. 사용자 확인 없이 일괄 변환하지 않는다.

```
{% stepper %}

{% step %}
### 단계 제목
단계 내용
{% endstep %}

{% endstepper %}
```

### 6. 접기 (선택)

FAQ, 긴 참고 표, 선택적 상세 설명에 쓴다. GitBook은 HTML `<details>`를 쓴다.

```
<details>

<summary>제목</summary>

내용

</details>
```

`<details open>`이면 펼친 상태가 기본. 내부에는 문단, 제목(h1~h3), 목록, 인라인 이미지만 허용된다.

### 7. 문서 간 링크 → content-ref (선택)

본문 흐름 속 링크는 일반 링크로 둔다. "관련 문서" 섹션처럼 독립적으로 문서를 가리킬 때만 카드로 만든다.

```
{% content-ref url="../path/to/page.md" %}
[페이지 제목](../path/to/page.md)
{% endcontent-ref %}
```

### 8. 카드 표 (cards) — 아이콘 열

"응용하기", "관련 문서"처럼 여러 문서를 나란히 소개하는 블록은 `<table data-view="cards">`로 만든다. 카드 맨 앞에 주제를 알려 주는 아이콘 열을 둘 수 있다.

아이콘은 이모지가 아니라 **GitBook의 Font Awesome 문법**을 쓴다. `class`의 `fa-` 뒤 이름과 안쪽 `:이름:`이 같아야 한다.

```
<td><h4><i class="fa-clock">:clock:</i></h4></td>
```

`<h4>`로 감싸야 카드 안에서 아이콘이 제목 크기로 커진다. 감싸지 않으면 본문 크기로 작게 표시된다.

전체 형태는 다음과 같다. 마지막 열은 카드 전체를 링크로 만드는 숨은 열이다.

```
<table data-view="cards">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th data-hidden data-card-target data-type="content-ref"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><h4><i class="fa-clock">:clock:</i></h4></td>
      <td><strong>일정 주기로 실행</strong></td>
      <td>카드 설명.</td>
      <td><a href="https://example.com/">https://example.com/</a></td>
    </tr>
  </tbody>
</table>
```

**`<thead>`의 `<th>` 개수와 각 행의 `<td>` 개수가 반드시 같아야 한다.** 아이콘 열을 추가할 때 `<th></th>`를 빠뜨리면 열이 밀려 마지막 숨은 열이 드러나고 카드 링크가 깨진다. 숨은 열(`data-hidden data-card-target`)도 개수에 포함한다.

아이콘 이름은 한 레포 안에서 같은 뜻에 같은 이름을 쓴다. 이 레포의 기존 사용례는 `ko/README.md`의 "자주 찾는 트러블슈팅" 표를 참고한다.

## 반드시 지킬 것 (파싱 오류 방지)

- **`{% ... %}` 태그는 반드시 열의 맨 앞(들여쓰기 0)에서 시작한다.** 목록 항목 안에 들여쓴 hint·code 태그는 GitBook이 파싱하지 못한다. 목록 안 코드 블록은 일반 fenced block으로 두고, 꼭 필요하면 목록 밖으로 뺀다.
- **목록 안에 있던 블록을 0열로 내어쓸 때는 그 블록의 앞뒤에 반드시 빈 줄을 넣는다.** 이것이 내어쓰기보다 더 자주 놓치는 부분이다. 예를 들어 목록 항목 사이에 있던 hint를 0열로 내리면 `{% endhint %}` 바로 다음 줄이 `2. …`가 되는데, 사이에 빈 줄이 없으면 CommonMark가 그 항목을 앞 문단의 lazy continuation으로 흡수해 목록이 통째로 깨진다. 내어쓴 블록은 항상 이 형태가 되어야 한다.

  ```
  1. 첫 번째 항목.

  {% hint style="info" %}
  보충 설명.
  {% endhint %}

  2. 두 번째 항목.
  ```

- 여는 태그 다음 줄과 닫는 태그 앞 줄의 빈 줄은 선택이다. 한 문서 안에서는 한쪽으로 통일한다(이 레포는 빈 줄 없이 붙여 쓴다).
- 모든 태그는 짝을 맞춘다: `hint/endhint`, `code/endcode`, `tabs/endtabs`, `tab/endtab`, `stepper/endstepper`, `step/endstep`, `content-ref/endcontent-ref`.
- **블록은 중첩만 되고 교차하면 안 된다.** 안쪽에서 연 블록을 안쪽에서 닫는다. 아래는 `step`과 `hint`가 서로 걸쳐 있어 GitBook이 파싱하지 못하는 예다. 여는 태그와 닫는 태그 **개수는 맞기 때문에** 눈으로는 멀쩡해 보이고, 결과만 깨진다(hint가 빈 상자가 되고 태그 문자열이 본문에 노출된다). 스테퍼를 나중에 덧씌울 때 가장 자주 나온다.

  ```
  {% hint style="info" %}
  {% endstep %}   <- hint 바깥에서 연 step 을 hint 안에서 닫음

  {% step %}
  보충 설명.
  {% endhint %}   <- step 안에서 hint 를 닫음
  ```

  step 경계는 hint 블록 바깥에 둔다. 섹션 전체(안쪽 hint 포함)가 하나의 step이 되는 것이 보통 맞다.
- 코드 블록 안의 GitBook 태그 문자열은 변환 대상이 아니다. 예제 코드로 보호한다.

## 작업 순서

1. 원본을 읽고 변환 대상 블록을 훑는다(인용문, 코드, 이미지, 대안 절차, 문서 링크).
2. 위 규칙대로 변환해 새 파일에 쓴다.
3. 검증 스크립트를 반드시 실행한다.

   ```bash
   python3 scripts/validate_gitbook.py 변환본.md 원본.md
   ```

   `scripts/validate_gitbook.py`는 태그 짝, **태그 중첩(교차 여부)**, 들여쓴 태그, **태그 블록 앞뒤의 빈 줄**, 코드 펜스 짝, hint 스타일 값을 확인하고, 원본 경로를 함께 주면 본문 텍스트가 보존됐는지도 비교한다. 종료 코드가 0이 아니면 고친 뒤 다시 실행한다.

4. 사용자에게 **무엇을 몇 개 바꿨는지**와 **판단이 필요해 손대지 않은 블록**을 짧게 보고한다.
