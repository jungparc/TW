#!/usr/bin/env python3
"""GitBook-flavored Markdown 검증기.

사용법:
    python3 scripts/validate_gitbook.py OUTPUT.md [ORIGINAL.md]

두 번째 인자를 주면 본문 텍스트가 보존됐는지도 비교한다.
문제가 있으면 stderr에 출력하고 종료 코드 1을 반환한다.
"""
import re
import sys

FENCE = "`" * 3

PAIRS = [
    ("hint", "endhint"),
    ("code", "endcode"),
    ("tabs", "endtabs"),
    ("tab", "endtab"),
    ("stepper", "endstepper"),
    ("step", "endstep"),
    ("content-ref", "endcontent-ref"),
    ("embed", None),
]


def strip_code_blocks(text):
    """코드 펜스 안의 내용을 빈 줄로 바꿔 예제 코드 속 태그를 오탐하지 않게 한다.

    줄을 지우지 않고 빈 줄로 남기므로 원본과 줄 번호가 그대로 맞는다.
    """
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(FENCE):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


TAG_LINE = re.compile(r"^\s*\{%.*%\}\s*$")
OPEN_TAG = re.compile(r"^\{%\s*(hint|code|tabs|tab|stepper|step|content-ref)(?=[\s%])")
CLOSE_TAG = re.compile(r"^\{%\s*end(hint|code|tabs|tab|stepper|step|content-ref)\s*%\}")


def check(path, original=None):
    raw = open(path, encoding="utf-8").read()
    body = strip_code_blocks(raw)
    problems = []

    # 1. 태그 짝 맞추기
    for open_tag, close_tag in PAIRS:
        if close_tag is None:
            continue
        n_open = len(re.findall(r"\{%%\s*%s(?=[\s%%])" % re.escape(open_tag), body))
        n_close = len(re.findall(r"\{%%\s*%s\s*%%\}" % re.escape(close_tag), body))
        # endtab 은 endtabs 에도 걸리므로 보정
        if open_tag == "tab":
            n_open -= len(re.findall(r"\{%\s*tabs(?=[\s%])", body))
        if close_tag == "endtab":
            n_close -= len(re.findall(r"\{%\s*endtabs\s*%\}", body))
        if open_tag == "step":
            n_open -= len(re.findall(r"\{%\s*stepper(?=[\s%])", body))
        if close_tag == "endstep":
            n_close -= len(re.findall(r"\{%\s*endstepper\s*%\}", body))
        if n_open != n_close:
            problems.append(
                "태그 불일치 %s: 여는 태그 %d개, 닫는 태그 %d개" % (open_tag, n_open, n_close)
            )

    # 2. 들여쓴 태그 (GitBook 이 파싱하지 못함)
    for i, line in enumerate(body.split("\n"), 1):
        if re.match(r"\s+\{%", line):
            problems.append("들여쓴 태그 (줄 %d): %s" % (i, line.strip()))

    # 2-1. 태그 블록 앞뒤의 빈 줄 (목록·문단에 흡수되어 렌더링이 깨짐)
    lines = body.split("\n")
    for i, line in enumerate(lines):
        prev = lines[i - 1] if i else ""
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if OPEN_TAG.match(line) and prev.strip() and not TAG_LINE.match(prev):
            problems.append(
                "여는 태그 앞에 빈 줄 없음 (줄 %d): %s  <- 앞 줄이 문단·목록으로 흡수됨"
                % (i + 1, line.strip())
            )
        if CLOSE_TAG.match(line) and nxt.strip() and not TAG_LINE.match(nxt):
            problems.append(
                "닫는 태그 뒤에 빈 줄 없음 (줄 %d): %s  <- 다음 줄이 문단으로 흡수됨"
                % (i + 1, line.strip())
            )

    # 3. 코드 펜스 짝
    if raw.count(FENCE) % 2:
        problems.append("코드 펜스(```)의 개수가 홀수")

    # 4. 알 수 없는 스타일
    for style in re.findall(r'\{%\s*hint\s+style="([^"]+)"', body):
        if style not in ("info", "success", "warning", "danger"):
            problems.append("알 수 없는 hint 스타일: %s" % style)

    # 5. 남은 블록인용문 (의도한 것인지 확인용, 경고)
    quotes = [l for l in body.split("\n") if l.lstrip().startswith(">")]
    if quotes:
        print("확인 필요: 인용문 %d줄이 남아 있음 (의도한 인용인지 확인)" % len(quotes))

    # 6. 본문 텍스트 보존 비교
    if original:
        def normalize(t):
            t = strip_code_blocks(t)
            # 이미지는 figure 로 바뀌며 캡션이 생길 수 있으므로 양쪽에서 통째로 제외
            t = re.sub(r"<figure>.*?</figure>", "", t, flags=re.S)
            t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
            t = re.sub(r"\{%[^%]*%\}", "", t)           # GitBook 태그 제거
            t = re.sub(r"\[!\w+\]", "", t)               # GitHub alert 라벨 제거 (hint 로 바뀌며 사라짐)
            t = re.sub(r"<[^>]+>", "", t)                # details 등 HTML 태그 제거
            t = re.sub(r"[💡⚠️❗✅🔔>\s]", "", t)         # 라벨 이모지·인용 기호·공백 제거
            return t

        if normalize(raw) != normalize(open(original, encoding="utf-8").read()):
            problems.append("본문 텍스트가 원본과 다름 — 래핑 외 수정이 들어갔는지 확인")

    if problems:
        for p in problems:
            print("FAIL: " + p, file=sys.stderr)
        return 1
    print("OK: %s" % path)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
