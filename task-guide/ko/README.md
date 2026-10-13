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
  metadata:
    visible: false
  tags:
    visible: false
  actions:
    visible: false
---

# NHN Cloud Task Guides

## 문제를 직접 해결하는 가이드

증상에서 출발해 원인을 좁히고, 자주 하는 작업은 단계별로 따라 할 수 있도록 정리했습니다.

<button type="button" class="button primary" data-action="ask" data-icon="gitbook-assistant">무엇을 하려고 하나요?</button>

<a href="troubleshooting/instance-creation-failed.md" class="button primary">트러블슈팅 시작하기</a><a href="how-to/cloud-monitoring-alarm-policy.md" class="button secondary">How-to 둘러보기</a>

<h3 align="center">How-to 가이드</h3>

<p align="center">자주 하는 작업을 처음부터 끝까지 따라 합니다.</p>

<table data-card-wrap="false" data-view="cards"><thead><tr><th><select><option value="pZx4KvTm8NrQ" label="MONITORING" color="blue"></option><option value="wGb6HsYd3LcF" label="NETWORK" color="blue"></option><option value="rJt5XbNu9QeM" label="SECURITY" color="blue"></option></select></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><span data-option="pZx4KvTm8NrQ">MONITORING</span></td><td><h4>Cloud Monitoring</h4></td><td>임계치 기반 알림 설정하기</td><td><a data-mention href="how-to/cloud-monitoring-alarm-policy.md">cloud-monitoring-alarm-policy.md</a></td><td><a data-mention href="how-to/l7-load-balancer-configuration.md">l7-load-balancer-configuration.md</a></td></tr><tr><td><span data-option="wGb6HsYd3LcF">NETWORK</span></td><td><h4>Load Balancer</h4></td><td>URL 경로 기반으로 트래픽 분산하기</td><td><a data-mention href="how-to/l7-load-balancer-configuration.md">l7-load-balancer-configuration.md</a></td><td><a data-mention href="how-to/network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td></tr><tr><td><span data-option="rJt5XbNu9QeM">SECURITY</span></td><td><h4>Network Firewall</h4></td><td>정책 구성 및 로그 전송 설정하기</td><td><a data-mention href="how-to/network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td><td><a data-mention href="how-to/cloud-monitoring-alarm-policy.md">cloud-monitoring-alarm-policy.md</a></td></tr><tr><td><span data-option="rJt5XbNu9QeM">SECURITY</span></td><td><h4>Secure Key Manager</h4></td><td>암호화 키 관리하기</td><td><a data-mention href="how-to/skm-key-management.md">skm-key-management.md</a></td><td><a data-mention href="how-to/skm-api-call-with-user-access-key-token.md">skm-api-call-with-user-access-key-token.md</a></td></tr></tbody></table>

***

<h3 align="center">자주 찾는 트러블슈팅</h3>

<p align="center">증상과 같은 제목을 찾아 들어가세요.</p>

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><h4><i class="fa-server">:server:</i></h4></td><td><h4>인스턴스 생성 실패</h4></td><td>인스턴스가 ERROR 상태가 되거나 생성 요청이 거부될 때</td><td><a data-mention href="troubleshooting/instance-creation-failed.md">instance-creation-failed.md</a></td><td><a data-mention href="troubleshooting/instance-ssh-connection-failed.md">instance-ssh-connection-failed.md</a></td></tr><tr><td><h4><i class="fa-terminal">:terminal:</i></h4></td><td><h4>SSH 접속 실패</h4></td><td>SSH 클라이언트로 인스턴스에 연결되지 않을 때</td><td><a data-mention href="troubleshooting/instance-ssh-connection-failed.md">instance-ssh-connection-failed.md</a></td><td><a data-mention href="how-to/network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td></tr><tr><td><h4><i class="fa-scale-balanced">:scale-balanced:</i></h4></td><td><h4>LB 멤버 INACTIVE</h4></td><td>헬스 체크가 실패해 멤버로 트래픽이 가지 않을 때</td><td><a data-mention href="troubleshooting/lb-healthcheck-inactive-member-troubleshooting.md">lb-healthcheck-inactive-member-troubleshooting.md</a></td><td><a data-mention href="how-to/network-firewall-policy-configuration.md">network-firewall-policy-configuration.md</a></td></tr></tbody></table>
