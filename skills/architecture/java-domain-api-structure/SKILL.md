---
name: java-domain-api-structure
description: "Java/Spring API 기능을 추가하거나 구조를 정리할 때 이상수의 도메인별 패키지, Service 인터페이스/구현, Repository 분리 관례를 적용한다. App/Internal 진입점과 이벤트 후처리 경계가 필요한 구현도 포함하며, 문서만 작성하는 작업에는 적용하지 않는다."
---

# 도메인별 Java API 구조

## 적용 기준

`eci-my247-api`에서 반복된 구현 선택을 보존한다. 사용자 요청과 대상 프로젝트의 지침·기존 구조를 먼저 따른다. 다른 구조를 사용하는 프로젝트를 이 패턴으로 일괄 개편하지 않는다.

## 구현 순서와 기본 배치

1. 같은 업무의 Controller, Service, Repository를 찾아 신규 기능의 소유 도메인을 정한다. 기존 도메인이 있으면 그 경계를 이어 쓰고, 단순히 공용으로 보인다는 이유로 `commons`에 옮기지 않는다.
2. 새 도메인을 구성할 때 다음 배치를 기본안으로 사용한다. 기존 도메인의 하위 패키지·복수형·명명은 그대로 따른다.

   ```text
   <domain>/
   ├── presentation/
   │   ├── <Domain>Controller.java
   │   └── dto/{request,response}/
   ├── application/
   │   ├── domain/
   │   ├── service/<Domain>Service.java
   │   └── service/impl/<Domain>ServiceImpl.java
   └── infrastructure/
       ├── <Domain>Repository.java
       ├── <Domain>CustomRepository.java
       └── impl/<Domain>CustomRepositoryImpl.java
   ```

3. API의 주 서비스는 인터페이스와 `impl` 구현으로 나눈다. Controller는 요청 바인딩, 인증 주체·경로값 전달과 서비스 호출을 맡고, 기능 처리와 조회 조합은 서비스에 둔다. 기존 Lombok 사용 관례가 있으면 `private final` 필드와 `@RequiredArgsConstructor` 방식으로 주입하고, 그렇지 않으면 현재 생성자 주입 방식을 따른다.
4. 저장소가 JPA 기본 기능과 별도 조회를 함께 제공한다면 `Repository extends JpaRepository<...>, CustomRepository`로 결합한다. 별도 조회 구현은 `infrastructure/impl`에 둔다. 파생 쿼리만 필요한 작은 저장소에 빈 CustomRepository를 만들지는 않는다.
5. 필요한 변형만 아래 참고 자료에서 적용한다. 구현이 끝나면 새 파일의 소유 도메인, 진입점의 요청자 전달, 주 서비스와 저장소의 연결을 확인한다.

## 조건에 따라 읽을 자료

- 앱과 관리자·다른 서버에서 같은 업무를 호출하거나, 알림·예약·파일 정리 등 후처리를 분리할 때: [진입점과 후처리 경계](references/boundary-variants.md).
- 기존 코드와 이 기본안이 다르거나 관례의 출처·예외를 판단할 때: [근거와 적용 한계](references/source-evidence.md).

## 과도하게 확장하지 않을 규칙

- Service가 `presentation.dto`를 사용하고 Entity가 요청 DTO를 받는 사례도 있다. 이 관례를 엄격한 계층 독립성이나 별도 port/adapter 구조로 바꾸어 해석하지 않는다.
- 이벤트 수신·스케줄·외부 처리 전담 서비스에는 인터페이스가 없는 사례가 있다. 모든 `@Service`에 `Interface/Impl` 쌍을 만들지 않는다.
- `domain` 위치나 DTO 하위 폴더가 다른 기존 도메인은 이번 기능에 필요한 부분만 확장한다. 요청 범위를 넘는 전체 패키지 이동이나 이름 정규화를 하지 않는다.
