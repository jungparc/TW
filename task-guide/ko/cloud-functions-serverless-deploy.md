# Cloud Functions로 HTTP 함수 배포하기

Cloud Functions는 서버를 직접 준비하지 않고 함수 단위로 코드를 실행하는 서버리스 서비스입니다. 콘솔에서 코드를 작성해 배포하면 함수마다 HTTP 트리거와 HTTPS 엔드포인트가 함께 제공되므로, 인스턴스를 만들고 웹 서버를 설치하는 과정 없이 API 하나를 공개할 수 있습니다.

간단한 처리 하나를 맡기려고 인스턴스를 상시 띄워 두면 요청이 없는 시간에도 리소스를 점유합니다. Cloud Functions의 Pool Manager 유형은 호출될 때만 인스턴스를 만들고, 일정 기간 호출이 없으면 인스턴스를 없애 리소스 사용량이 0이 됩니다.

이 가이드를 따라하면 콘솔에서 함수를 만들고 코드를 빌드해 배포한 다음, 발급된 엔드포인트 URL을 호출해 응답을 확인할 수 있습니다.

![클라이언트의 요청이 함수 엔드포인트를 거쳐 함수 인스턴스에서 실행된 뒤 응답으로 돌아오고, 호출이 없으면 인스턴스가 제거되는 구성](images/cloud-functions-serverless-deploy-flow.svg)

## 시작하기 전에

- NHN Cloud 콘솔에서 Cloud Functions 서비스가 활성화되어 있어야 합니다.
- 함수 이름을 정합니다. **영문 소문자와 숫자, 하이픈(`-`)**만 쓸 수 있고 최대 45자입니다. 이 이름이 엔드포인트 URL에 그대로 들어갑니다.
- 함수 코드는 따로 준비하지 않아도 됩니다. 콘솔이 런타임별 템플릿을 제공하며, 이 가이드는 그 템플릿으로 `hello, world!`를 반환하는 함수를 만듭니다.

## 함수 설정하기

함수 생성은 **함수 설정**과 **코드 작성** 두 단계로 진행합니다. 먼저 함수가 어떤 환경에서 실행될지 정합니다.

1. NHN Cloud 콘솔에서 **Compute > Cloud Functions**를 클릭하세요.

2. **함수 생성**을 클릭하세요.

3. **이름**에 함수 이름을 입력하세요. 입력한 이름이 **엔드포인트 URL** 뒤에 붙어 호출 주소가 정해집니다. 한국(판교) 리전은 다음과 같은 형식입니다.

    ```text
    https://{프로젝트 식별자}-kr1-app.functions.nhncloud.com/{함수 이름}
    ```

4. **유형**은 **Pool Manager**를 그대로 둡니다. 호출될 때만 인스턴스가 만들어지고 호출이 없으면 사라지므로, 요청이 꾸준하지 않은 함수에 적합합니다.

{% hint style="info" %}
## 요청이 많고 빠른 응답이 필요하다면 **New Deployment**를 선택합니다. 

- 인스턴스를 상시 유지해 응답이 빠른 대신, 호출이 없어도 리소스를 계속 사용합니다. 두 유형 모두 다른 함수와 자원을 나눠 쓰지만, **Pool Manager**는 CPU 사용량에 상한이 없어 다른 함수와 경합하면 실행 성능이 달라질 수 있고, **New Deployment**는 **리소스**에서 선택한 메모리 크기에 따라 CPU와 메모리 상한이 함께 정해져 그 범위 안에서 실행됩니다. 
- 실행 성능을 일정하게 유지해야 하는 작업에는 **New Deployment**를 사용하세요.
{% endhint %}


5. **리소스**, **실행 시간 제한**, **동시 실행 설정**은 기본값을 그대로 둡니다. 실행 시간 제한은 `60`초이며 최대 900초까지, 동시 실행 설정은 `1`건이며 최대 1,000건까지 지정할 수 있습니다.

{% hint style="warning" %}
함수 실행이 제한 시간을 넘기면 호출은 `504` 응답으로 끝납니다. 외부 API를 호출하는 함수처럼 응답이 오래 걸리는 작업은 제한 시간을 넉넉히 지정하세요.
{% endhint %}

6. **다음**을 클릭하세요.

## 코드 작성하고 빌드하기

콘솔 코드 에디터에서 함수 코드를 작성하고 빌드합니다. **함수를 생성하려면 빌드를 최소 한 번 수행해야 합니다.**

1. **런타임 환경**에서 사용할 런타임을 선택하세요. 런타임을 선택하면 해당 언어의 템플릿 파일이 코드 에디터에 로드되고 **Entry Point**가 자동으로 채워집니다.

    **NodeJS**를 선택하면 `hello.js`와 `package.json`이 로드되고 Entry Point는 `hello`가 됩니다. `hello.js`의 템플릿이 이미 `hello, world!`를 반환하므로 코드를 고치지 않아도 됩니다.

    ```js
    module.exports = async (context) => {
        return {
            status: 200,
            body: "hello, world!\n"
        };
    }
    ```

    **Python**을 선택하면 `user.py`와 `requirements.txt`가 로드되고 Entry Point는 `user.main`이 됩니다. `user.py`의 템플릿은 YAML 예제이므로, NodeJS와 같은 응답을 내도록 파일 목록에서 `user.py`를 클릭해 다음 코드로 바꿉니다. 반환한 값이 응답 본문이 됩니다.

    ```python
    def main():
        return "hello, world!"
    ```

{% hint style="info" %}
 런타임 목록에는 지원 중단된 런타임에 **지원 중단** 배지가 표시되고, 사용 중단된 런타임은 목록에서 제외되어 선택할 수 없습니다. 지원 중단 런타임으로도 함수를 만들 수 있지만 최신 런타임을 사용하세요.
 {% endhint %}

2. **빌드**를 클릭하세요. 빌드가 끝나면 **빌드 성공**이 표시되고, 아래 **빌드 결과** 탭에서 설치 로그를 확인할 수 있습니다.

3. **테스트**를 클릭해 함수가 실행되는지 확인하세요. **테스트 결과** 탭에 함수 호출 로그가 표시됩니다.

{% hint style="info" %}
 테스트는 실행 로그만 보여 주고 응답 본문은 표시하지 않습니다. 반환값은 함수를 생성한 다음 엔드포인트 URL을 호출해 확인합니다.
{% endhint %}

4. **생성**을 클릭하세요. **함수 생성 정보** 대화 상자에서 내용 확인 후 **생성**을 클릭합니다.

## 동작 확인하기

1. 함수 목록에서 만든 함수의 **빌드 상태**를 확인하세요. 상태는 아이콘으로 표시되며, 초록색 아이콘에 마우스를 올리면 **빌드 성공**이 나타납니다.

2. 함수 이름을 클릭해 상세 정보를 열고 **트리거** 탭으로 이동하세요. 함수를 만들 때 HTTP 트리거가 자동으로 등록되어 있습니다. **Trigger Value**의 **복사**를 클릭해 엔드포인트 URL을 가져옵니다.

3. 복사한 URL을 호출하세요.

    ```bash
    curl -i "{엔드포인트 URL}"
    ```

4. `200 OK`와 함께 `hello, world!`가 반환되면 배포가 끝난 것입니다.

{% tabs %}
{% tab title="HTTP" %}
```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 14

hello, world!
```
{% endtab %}

{% tab title="cURL" %}
```bash
curl -i https://example.com/hello
```
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const res = await fetch("https://example.com/hello");

console.log(res.status);                        // 200
console.log(res.headers.get("content-type"));   // text/html; charset=utf-8
console.log(await res.text());                  // hello, world!
```
{% endtab %}

{% tab title="Python" %}
```python
import requests

res = requests.get("https://example.com/hello")

print(res.status_code)                  # 200
print(res.headers["Content-Type"])      # text/html; charset=utf-8
print(res.text)                         # hello, world!
```
{% endtab %}

{% tab title="Go" %}
```go
res, err := http.Get("https://example.com/hello")
if err != nil {
    log.Fatal(err)
}
defer res.Body.Close()

body, _ := io.ReadAll(res.Body)
fmt.Println(res.Status)                        // 200 OK
fmt.Println(res.Header.Get("Content-Type"))    // text/html; charset=utf-8
fmt.Println(string(body))                      // hello, world!
```
{% endtab %}
{% endtabs %}

브라우저 주소 창에 같은 URL을 입력해도 결과를 볼 수 있습니다.


{% code title="[테스트용] index.js" overflow="wrap" lineNumbers="true" %}

```javascript
‌import * as React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, window.document.getElementById('root'));
```

{% endcode %}

## 응용하기

- **일정 주기로 실행**: Timer 트리거를 추가하면 크론 표현식으로 지정한 주기마다 함수를 실행할 수 있습니다. API Gateway와 연동해 인증이나 사용량 제어를 붙일 수도 있습니다. 자세한 내용은 [트리거 가이드](https://docs.nhncloud.com/ko/Compute/Cloud%20Functions/ko/trigger-guide/)를 참고하세요.
- **설정값을 코드와 분리**: 외부 서비스 인증 정보나 접속 정보를 코드에 넣지 않고 환경 변수로 등록할 수 있습니다. 함수당 100개까지 등록할 수 있으며, 값은 콘솔 조회 화면에서 마스킹되지만 저장과 로그에는 암호화가 적용되지 않으므로 노출되면 곤란한 값은 주의해서 다룹니다. 자세한 내용은 [Cloud Functions 콘솔 사용 가이드](https://docs.nhncloud.com/ko/Compute/Cloud%20Functions/ko/console-guide/#function-environment-variables)를 참고하세요.
- **로컬에서 작성한 코드 올리기**: 코드 에디터에서는 디렉터리를 추가할 수 없습니다. 폴더 구조가 있는 코드는 **코드 작성** 단계의 **코드** 탭에서 편집기 위의 목록을 **코드 에디터**에서 **사용자 로컬 환경**으로 바꾼 다음 ZIP 파일로 업로드합니다. **ZIP 파일 다운로드**로 템플릿을 내려받아 로컬에서 수정한 뒤 올리면 구조를 그대로 유지할 수 있습니다. 런타임별 파일 구조와 주의 사항은 코드 템플릿 가이드의 [NodeJS](https://docs.nhncloud.com/ko/Compute/Cloud%20Functions/ko/code-template-node-guide/), [Python](https://docs.nhncloud.com/ko/Compute/Cloud%20Functions/ko/code-template-python-guide/) 문서를 참고하세요.
- **실행 로그 확인**: 로그 서비스 연동을 사용하면 함수 실행 로그를 Log & Crash Search에서 조회할 수 있습니다. 자세한 내용은 [Cloud Functions 콘솔 사용 가이드](https://docs.nhncloud.com/ko/Compute/Cloud%20Functions/ko/console-guide/#basic-information-of-functions)를 참고하세요.

## 정리하기

실습으로 만든 함수는 사용을 마치면 삭제하세요. Pool Manager 유형은 호출이 없으면 리소스를 사용하지 않지만, 엔드포인트 URL은 삭제하기 전까지 계속 열려 있습니다.

1. 함수 목록에서 삭제할 함수를 선택한 다음 **함수 삭제**를 클릭하세요.

{% hint style="warning" %}
함수를 삭제하면 작성한 코드와 설정이 함께 삭제되며 복구할 수 없습니다.
{% endhint %}


## 용어 정리

| 용어 | 설명 |
| --- | --- |
| 서버리스 | 클라우드 서비스 사용자가 애플리케이션 핵심 기능 개발에만 집중할 수 있도록 클라우드 서비스 공급자(CSP)가 인프라 및 플랫폼 자원뿐 아니라 애플리케이션 구동에 필요한 주변 응용 소프트웨어 기능을 가상화하여 제공하는 클라우드 서비스 |
| 엔드포인트 | 요청을 받아 응답을 제공하는 서비스를 사용할 수 있는 지점. 주로 API 엔드포인트를 의미하며, URL 형식이 사용됨 |
| 인스턴스 | 가상의 CPU, 메모리, 기본 디스크로 구성된 가상 서버 |
| 크론 표현식 | 공백으로 구분된 5개 또는 6개의 필드로 구성된 문자열로 특정 시간 또는 간격으로 작업을 실행하기 위한 시간 집합을 표현하기 위해 사용함 |
