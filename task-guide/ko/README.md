---
description: NHN Cloud를 사용하다 막히는 지점을 스스로 해결하도록 돕는 트러블슈팅·How-to 가이드 모음입니다.
layout:
  width: wide
  title:
    visible: false
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: false
  pagination:
    visible: true
---

# NHN Cloud 활용 가이드

## 문제를 직접 해결하는 가이드

증상에서 출발해 원인을 좁히고, 자주 하는 작업은 단계별로 따라 할 수 있도록 정리했습니다.

<button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">무엇을 하려고 하나요?</button>

<a href="instance-creation-failed.md" class="button primary">트러블슈팅 시작하기</a><a href="cloud-functions-serverless-deploy.md" class="button secondary">How-to 둘러보기</a>

<h3 align="center">How-to 가이드</h3>

<p align="center">자주 하는 작업을 처음부터 끝까지 따라 합니다.</p>

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><h4><i class="fa-bolt">:bolt:</i></h4></td><td><h4>Cloud Functions</h4></td><td>서버 없이 HTTP 함수 배포하기</td><td><a data-mention href="cloud-functions-serverless-deploy.md">cloud-functions-serverless-deploy.md</a></td><td><a data-mention href="obs-static-website-hosting.md">obs-static-website-hosting.md</a></td><td><a data-mention href="skm-key-management.md">skm-key-management.md</a></td></tr><tr><td><h4><i class="fa-box-archive">:box-archive:</i></h4></td><td><h4>Object Storage</h4></td><td>정적 웹사이트 호스팅하기</td><td><a data-mention href="obs-static-website-hosting.md">obs-static-website-hosting.md</a></td><td><a data-mention href="obs-access-control-cors.md">obs-access-control-cors.md</a></td><td><a data-mention href="cloud-functions-serverless-deploy.md">cloud-functions-serverless-deploy.md</a></td></tr><tr><td><h4><i class="fa-key">:key:</i></h4></td><td><h4>Secure Key Manager</h4></td><td>암호화 키 관리하기</td><td><a data-mention href="skm-key-management.md">skm-key-management.md</a></td><td><a data-mention href="skm-api-call-with-user-access-key-token.md">skm-api-call-with-user-access-key-token.md</a></td><td><a data-mention href="cloud-functions-serverless-deploy.md">cloud-functions-serverless-deploy.md</a></td></tr></tbody></table>

***

<h3 align="center">자주 찾는 트러블슈팅</h3>

<p align="center">증상과 같은 제목을 찾아 들어가세요.</p>

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><h4><i class="fa-server">:server:</i></h4></td><td><h4>인스턴스 생성 실패</h4></td><td>인스턴스가 ERROR 상태가 되거나 생성 요청이 거부될 때</td><td><a data-mention href="instance-creation-failed.md">instance-creation-failed.md</a></td><td><a data-mention href="instance-ssh-connection-failed.md">instance-ssh-connection-failed.md</a></td><td><a data-mention href="network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td></tr><tr><td><h4><i class="fa-terminal">:terminal:</i></h4></td><td><h4>SSH 접속 실패</h4></td><td>SSH 클라이언트로 인스턴스에 연결되지 않을 때</td><td><a data-mention href="instance-ssh-connection-failed.md">instance-ssh-connection-failed.md</a></td><td><a data-mention href="network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td><td><a data-mention href="instance-creation-failed.md">instance-creation-failed.md</a></td></tr><tr><td><h4><i class="fa-scale-balanced">:scale-balanced:</i></h4></td><td><h4>LB 멤버 INACTIVE</h4></td><td>헬스 체크가 실패해 멤버로 트래픽이 가지 않을 때</td><td><a data-mention href="lb-healthcheck-inactive-member-troubleshooting.md">lb-healthcheck-inactive-member-troubleshooting.md</a></td><td><a data-mention href="network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td><td><a data-mention href="instance-ssh-connection-failed.md">instance-ssh-connection-failed.md</a></td></tr></tbody></table>
