# 브라우저에서 Object Storage 컨테이너에 접근하도록 허용하기

Object Storage는 데이터를 오브젝트 단위로 저장하는 스토리지 서비스입니다. 컨테이너에 올린 오브젝트는 저마다 HTTP 주소를 가지므로, 웹 애플리케이션의 스크립트가 백엔드를 거치지 않고 브라우저에서 직접 읽고 쓸 수 있습니다.

다만 브라우저는 스크립트가 **다른 출처**의 응답을 읽지 못하도록 기본적으로 막습니다. 출처는 주소에서 프로토콜과 호스트, 포트만 떼어 낸 부분입니다. 웹 애플리케이션의 주소와 Object Storage의 API 엔드포인트는 호스트가 달라 서로 다른 출처이므로, 브라우저에서 오브젝트를 직접 다루려면 이 제한을 먼저 풀어야 합니다.

브라우저에서 보낸 요청은 두 개의 관문을 지납니다. 하나는 **서버**가 권한을 확인하는 컨테이너의 접근 정책이고, 다른 하나는 **브라우저**가 응답을 읽어도 되는지 확인하는 교차 출처 리소스 공유(CORS)입니다. **두 관문 중 하나라도 막히면 요청은 실패합니다.**

이 가이드를 따라하면 특정 웹사이트에서 실행되는 스크립트가 컨테이너의 오브젝트에 접근할 수 있도록 접근 정책과 CORS를 설정하고, 설정이 실제로 적용되었는지 확인할 수 있습니다.

![브라우저의 페이지와 Object Storage가 서로 다른 호스트이며, 요청은 접근 정책을 지나 오브젝트에 닿고 돌아온 응답은 브라우저의 CORS 확인을 통과해야 스크립트가 읽을 수 있는 구성](images/obs-access-control-cors-flow.svg)

## 시작하기 전에

- NHN Cloud 콘솔에서 Object Storage 서비스가 활성화되어 있어야 하고, 설정할 컨테이너와 그 안에 요청해 볼 오브젝트가 하나 필요합니다.
- 허용할 웹사이트의 주소를 확인합니다. `https://app.example.com`처럼 프로토콜과 호스트로 이루어진 주소이며, 포트를 쓴다면 포트까지 포함합니다. 스크립트를 실행할 웹사이트가 이미 있다면 그 주소를 사용하고, 없다면 다음 내용을 `cors-test.html`로 저장해 준비하세요. `{ }` 부분은 실제 값으로 바꾸고, 파일은 UTF-8로 저장합니다.

{% hint style="info" %}
`{Object Store 엔드포인트}`는 컨테이너 목록 위쪽의 **API 엔드포인트 설정**을 클릭하면 **Object Store** 항목에서 확인할 수 있습니다. `{컨테이너 이름}`은 컨테이너 목록에 표시된 이름이고, `{오브젝트 이름}`은 컨테이너 **이름**을 클릭하면 열리는 오브젝트 목록에서 확인합니다.
{% endhint %}

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>CORS 확인</title>
</head>
<body>
  <button id="run">요청 보내기</button>
  <pre id="out"></pre>
  <script>
    document.getElementById("run").addEventListener("click", async () => {
      const url = "{Object Store 엔드포인트}/{컨테이너 이름}/{오브젝트 이름}";
      const out = document.getElementById("out");
      try {
        const response = await fetch(url, { cache: "no-store" });
        out.textContent = `status: ${response.status}`;
      } catch (e) {
        out.textContent = `${e.name}: ${e.message}`;
      }
    });
  </script>
</body>
</html>
```

이 페이지는 웹 서버로 띄운 주소에서 열어야 합니다. 파일이 있는 폴더에서 `python -m http.server 8000`을 실행하면 `http://localhost:8000`에서 열리며, 이 주소를 허용할 웹사이트 주소로 사용합니다.

## 접근 정책 설정하기

컨테이너에 누가 접근할 수 있는지를 먼저 정합니다. 접근 정책에서 막힌 요청은 CORS를 열어 두어도 통과하지 못합니다.

1. NHN Cloud 콘솔에서 **Storage > Object Storage**를 클릭하세요.

2. 컨테이너 목록에서 설정할 컨테이너를 클릭해 하단 상세 정보를 열고 **기본 정보** 탭으로 이동하세요.

{% hint style="info" %}
컨테이너 **이름**을 클릭하면 오브젝트 목록으로 이동합니다. 상세 정보를 열려면 이름이 아닌 행의 다른 영역을 클릭하세요.
{% endhint %}

3. **접근 정책 설정 변경**을 클릭한 다음 **접근 정책**에서 **PUBLIC**을 선택하세요. 공개 URL로 누구나 오브젝트를 읽을 수 있는 상태가 되며, 로그인 없이 열어도 되는 이미지나 첨부 파일을 내려받는 용도에 적합합니다. 이 가이드에서는 스크립트가 오브젝트를 읽기만 하므로 PUBLIC을 기준으로 설명합니다.

{% hint style="info" %}
업로드처럼 아무나 실행하면 안 되는 작업을 허용하려면 **PRIVATE**을 선택합니다. 허가된 사용자만 오브젝트에 접근할 수 있으므로 스크립트가 요청할 때마다 인증 토큰을 함께 보내야 하며, 발급 방법은 [Object Storage API 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/api-guide/#auth)를 참고하세요. 다른 프로젝트나 특정 API 사용자에게만 열어야 한다면 테넌트 ID와 API 사용자 ID 단위로 권한을 지정하는 **역할 기반 접근 정책**을 함께 사용합니다. 자세한 내용은 [접근 정책 설정 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/acl-guide/#role-based-access-policies)를 참고하세요.
{% endhint %}

4. **확인**을 클릭하세요.

## CORS 허용 출처 등록하기

브라우저는 스크립트가 실행 중인 출처와 다른 주소로 보낸 요청의 응답을 기본적으로 읽지 못하게 막습니다. 컨테이너에 허용 출처를 등록해 두면 Object Storage가 응답에 허용 헤더를 실어 보내고, 브라우저가 응답을 통과시킵니다.

{% hint style="info" %}
컨테이너 앞에 CDN을 두었다면 컨테이너에 등록한 허용 출처만으로는 부족합니다. CDN은 원본 서버의 응답을 캐시에 담아 재사용하는데, 첫 요청에 `Origin` 헤더가 없으면 허용 헤더가 빠진 응답이 캐시에 남고 이후 요청은 `Origin` 값과 상관없이 그 응답을 받습니다. CDN 서비스의 **HTTP 응답 헤더** 설정에서 `Access-Control-Allow-Origin`을 직접 지정하세요. 자세한 내용은 [CDN 콘솔 사용 가이드](https://docs.nhncloud.com/ko/Contents%20Delivery/CDN/ko/console-guide/#http-response-header)를 참고하세요.
{% endhint %}

1. 컨테이너 목록에서 앞에서 접근 정책을 설정한 컨테이너를 클릭해 하단 상세 정보를 열고 **기본 정보** 탭으로 이동하세요.

2. **교차 출처 리소스 공유(CORS)** 항목의 **변경**을 클릭하세요.

3. 허용할 웹사이트 주소를 한 줄에 하나씩 입력하세요.

    ```text
    https://app.example.com
    https://admin.example.com
    ```

    주소에는 프로토콜(`https://` 또는 `http://`)이 반드시 들어가야 합니다. 빠뜨리면 `{N}번 줄의 주소 형식이 잘못되었습니다.`라는 오류가 표시됩니다. 허용 출처는 최대 100개까지 등록할 수 있습니다.

{% hint style="info" %}
경로나 마지막 슬래시를 붙여도 저장은 되지만, 브라우저가 보내는 출처 값에는 프로토콜과 호스트, 포트까지만 담깁니다. 등록한 문자열과 정확히 일치하는 출처만 허용되므로 `https://app.example.com/upload`가 아니라 `https://app.example.com`으로 입력하세요.
{% endhint %}

{% hint style="warning" %}
`*`만 입력하면 모든 웹사이트의 스크립트가 응답을 읽을 수 있습니다. 공개해도 되는 오브젝트를 읽기 전용으로 제공할 때만 사용하고, 업로드나 삭제를 허용하는 컨테이너에는 출처를 명시하세요.
{% endhint %}

4. **확인**을 클릭하세요.

## 동작 확인하기

설정은 저장하는 즉시 반영되지만 화면에 결과가 보이지 않으므로, 실제로 요청을 보내 확인합니다. 브라우저에서 한 번에 확인할 수도 있지만 실패하면 어느 관문에서 막혔는지 알 수 없으므로, `curl`로 관문을 하나씩 확인한 다음 브라우저로 넘어갑니다. 허용 출처로 등록한 웹사이트가 아직 준비되지 않았다면 1~2단계만으로도 설정이 맞는지 확인할 수 있습니다.

{% hint style="info" %}
설정을 바꾼 뒤 다시 확인할 때는 강력 새로고침(`Ctrl+F5`)으로 캐시를 건너뛰세요. 브라우저가 이전 응답을 캐시에 두고 재사용하면 바뀐 설정이 반영되지 않은 결과가 보입니다.
{% endhint %}

1. 접근 정책부터 확인하세요. PUBLIC 컨테이너는 인증 없이도 오브젝트를 읽을 수 있으므로, 토큰 없이 요청해 보면 앞에서 설정한 값이 반영되었는지 알 수 있습니다.

    ```bash
    curl -i "{Object Store 엔드포인트}/{컨테이너 이름}/{오브젝트 이름}"
    ```

    `200 OK`와 함께 오브젝트가 내려오면 PUBLIC이 적용된 것입니다.

{% hint style="info" %}
PRIVATE으로 설정했다면 `401 Unauthorized`가 돌아오는 것이 정상입니다. 이 경우 스크립트에서 요청에 토큰을 함께 보내야 합니다.
{% endhint %}

2. 프리플라이트 요청으로 CORS 설정을 확인하세요. 브라우저는 다른 출처로 요청을 보낼 때 요청의 형태에 따라 `OPTIONS` 요청으로 허용 여부를 먼저 묻습니다. 이 요청을 직접 보내면 설정이 적용되었는지 응답 헤더로 확인할 수 있습니다.

    ```bash
    curl -i -X OPTIONS \
      -H "Origin: https://app.example.com" \
      -H "Access-Control-Request-Method: GET" \
      "{Object Store 엔드포인트}/{컨테이너 이름}/{오브젝트 이름}"
    ```

    `200 OK`와 함께 요청한 출처가 담긴 `access-control-allow-origin` 헤더가 돌아오면 CORS 설정이 적용된 것입니다. 아직 오브젝트를 올리지 않았어도 확인할 수 있습니다.

    ```text
    HTTP/1.1 200 OK
    access-control-allow-origin: https://app.example.com
    access-control-allow-methods: HEAD, PUT, GET, POST, DELETE, OPTIONS, COPY
    vary: Origin
    ```

    허용 목록에 없는 출처로 요청하면 `401 Unauthorized`가 돌아오고 허용 헤더가 담기지 않습니다. 등록한 주소와 `Origin` 값이 정확히 일치하는지 확인하세요. 프로토콜과 포트까지 같아야 합니다.

    ```text
    HTTP/1.1 401 Unauthorized
    ```

    PRIVATE 컨테이너를 사용한다면 요청에 실어 보낼 토큰 헤더까지 함께 물어보세요. 응답에 `access-control-allow-headers: x-auth-token`이 돌아오면 토큰을 붙인 요청도 통과합니다.

    ```bash
    curl -i -X OPTIONS \
      -H "Origin: https://app.example.com" \
      -H "Access-Control-Request-Method: GET" \
      -H "Access-Control-Request-Headers: x-auth-token" \
      "{Object Store 엔드포인트}/{컨테이너 이름}/{오브젝트 이름}"
    ```

3. 허용 출처로 등록한 주소에서 페이지를 열고 오브젝트를 요청하세요. 「시작하기 전에」의 샘플 페이지를 준비했다면 브라우저에서 열고 **요청 보내기**를 클릭합니다.

{% hint style="info" %}
PRIVATE 컨테이너라면 `fetch`의 `X-Auth-Token` 헤더에 발급받은 토큰을 실어 보냅니다. 이때 토큰은 동작을 확인하는 용도입니다. 공개된 페이지의 스크립트에 토큰을 심으면 누구나 컨테이너에 접근할 수 있으므로, 실제 서비스에서는 응용하기에서 안내하는 서명된 URL을 사용하세요.
{% endhint %}

4. 상태 코드가 `200`이면 두 관문을 모두 통과한 것입니다. CORS에서 막히면 `fetch`는 상태 코드를 돌려주지 못하고 `TypeError: Failed to fetch`로 실패합니다. 자세한 실패 원인은 개발자 도구 콘솔에서 확인할 수 있습니다.

    | 증상 | 막힌 관문 | 확인할 것 |
    | --- | --- | --- |
    | `No 'Access-Control-Allow-Origin' header is present on the requested resource` | CORS | 스크립트가 실행되는 주소가 프로토콜과 포트까지 등록한 허용 출처와 정확히 일치하는지 확인합니다 |
    | `401 Unauthorized` | 접근 정책 | 컨테이너가 PRIVATE이라면 유효한 토큰을 함께 보냈는지 확인합니다 |
    | `403 Forbidden` | 접근 정책 | 역할 기반 접근 정책을 사용한다면 수행하려는 작업에 맞는 권한(`Read`/`Write`)이 선택되어 있는지 확인합니다 |

## 응용하기

- **오브젝트 하나만 한시적으로 공개**: 접근 제어는 모두 컨테이너 단위로 걸리므로, 특정 오브젝트 하나만 열어 주려면 컨테이너를 열지 말고 서명된 URL을 사용합니다. 유효 기간이 지나면 자동으로 만료되어 공유용으로 적합합니다. 자세한 내용은 [서명된 URL 사용 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/presigned-url-guide/)를 참고하세요.
- **콘솔 대신 API로 설정**: 컨테이너를 여러 개 운영한다면 API로 같은 설정을 한 번에 적용할 수 있습니다. CORS는 `X-Container-Meta-Access-Control-Allow-Origin` 헤더로 지정하며, 콘솔과 달리 허용 출처는 공백으로 구분합니다. 자세한 내용은 [API 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/api-guide/#set-container-cors-policy)를 참고하세요. 컨테이너 정책의 `cors` 키를 사용하면 프리플라이트 응답 캐시 시간(`max_age`)과 브라우저에 노출할 응답 헤더(`expose_headers`)까지 지정할 수 있습니다. 자세한 내용은 [컨테이너 정책 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/container-policy-guide/#cors)를 참고하세요.
- **접근 위치를 IP로 제한**: 사내 도구나 배포 서버처럼 접근하는 위치가 고정되어 있다면 컨테이너에 IP ACL을 걸어 그 밖의 요청을 거부할 수 있습니다. 접근 정책과 IP ACL을 함께 설정하면 두 조건을 모두 충족해야 하므로, 불특정 다수가 브라우저로 접속하는 서비스에는 맞지 않습니다. 자세한 내용은 [접근 정책 설정 가이드](https://docs.nhncloud.com/ko/Storage/Object%20Storage/ko/acl-guide/)를 참고하세요.

## 정리하기

확인을 마쳤다면 열어 둔 설정을 되돌리세요. 접근 정책과 허용 출처는 직접 지우기 전까지 계속 유효합니다.

1. 컨테이너 목록에서 컨테이너를 선택한 다음 **기본 정보** 탭에서 **교차 출처 리소스 공유(CORS)** 항목의 **변경**을 클릭하고, 입력란을 비운 다음 **확인**을 클릭하세요. 동작을 확인하려고 `*`를 입력했다면 반드시 지워야 합니다.

2. 공개할 필요가 없는 컨테이너라면 **접근 정책 설정 변경**에서 접근 정책을 PRIVATE으로 되돌리세요. PUBLIC인 컨테이너의 오브젝트는 URL을 아는 누구나 내려받을 수 있습니다.

3. 실습용으로 컨테이너를 새로 만들었다면 **컨테이너 비우기**로 오브젝트를 삭제한 다음 **컨테이너 삭제**를 클릭하세요.

{% hint style="warning" %}
컨테이너 비우기를 실행하면 컨테이너에 저장된 모든 오브젝트가 삭제되며 복구할 수 없습니다.
{% endhint %}

## 용어 정리

| 용어 | 설명 |
| --- | --- |
| 오브젝트 스토리지 | 데이터를 오브젝트 단위로 관리하는 데이터 스토리지로, 많은 양의 데이터를 저장할 수 있음 |
| 컨테이너 | 오브젝트 스토리지에서 최상위 폴더를 의미. 기본적으로 접근 권한 설정의 단위가 됨 |
| 오브젝트 | 오브젝트 스토리지의 기본적인 관리 단위 |
| 토큰 | API와 상호 작용을 위해 사용자를 인증하고 권한을 부여하는 데 사용되는 식별 정보 |
| 출처 | 주소에서 프로토콜과 호스트, 포트만 떼어 낸 부분. 셋 중 하나라도 다르면 다른 출처가 됨 |
| 교차 출처 리소스 공유(CORS) | 다른 출처에서 실행되는 스크립트가 응답을 읽을 수 있도록 서버가 허용하는 방식 |
| 프리플라이트 | 브라우저가 다른 출처로 본 요청을 보내기 전에 허용 여부를 먼저 확인하는 `OPTIONS` 요청 |
