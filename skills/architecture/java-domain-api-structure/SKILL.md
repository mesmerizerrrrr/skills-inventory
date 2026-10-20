---
name: java-domain-api-structure
description: "Java/Spring API의 도메인별 패키지·계층을 구성하거나 Service 생성·트랜잭션 설정을 다룰 때 사용한다. Service 인터페이스/구현, Lombok 생성자 주입, readOnly 기반 트랜잭션·DB 분기, Repository 분리와 진입점·후처리 경계를 다루며, 문서만 작성하는 작업에는 적용하지 않는다."
---

# 도메인별 Java API 구조

## 적용 기준

업무 도메인 안에서 API 진입점·서비스·저장소의 책임을 구분한다. 사용자 요청과 대상 프로젝트의 지침·기존 구조를 먼저 따른다. 다른 구조를 사용하는 프로젝트를 이 패턴으로 일괄 개편하지 않는다.

Service 클래스를 새로 만들 때는 [신규 Service 생성자 주입](#신규-service-생성자-주입)과 DB 접근에 해당하는 [Service 트랜잭션과 readOnly](#service-트랜잭션과-readonly)를 적용한다. 기존 Service의 트랜잭션을 조정할 때는 트랜잭션 절을 적용한다. 이 규칙을 읽었다는 이유로 기존 패키지를 재편하거나 `Interface/Impl` 분리를 추가하지 않는다.

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

3. API의 주 서비스는 인터페이스와 `impl` 구현으로 나눈다. Controller는 요청 바인딩, 인증 주체·경로값 전달과 서비스 호출을 맡고, 기능 처리와 조회 조합은 서비스에 둔다. 신규 Service의 의존성 주입은 아래 기본 규칙을 따른다.
4. 저장소가 JPA 기본 기능과 별도 조회를 함께 제공한다면 `Repository extends JpaRepository<...>, CustomRepository`로 결합한다. 별도 조회 구현은 `infrastructure/impl`에 둔다. 파생 쿼리만 필요한 작은 저장소에 빈 CustomRepository를 만들지는 않는다.
5. 필요한 변형만 아래 참고 자료에서 적용한다. 구현이 끝나면 새 파일의 소유 도메인, 진입점의 요청자 전달, 주 서비스와 저장소의 연결을 확인한다.

## 신규 Service 생성자 주입

- **새로 만드는 Service 클래스는 Lombok `@RequiredArgsConstructor`와 `private final` 의존성 필드를 기본으로 사용한다.** 주 서비스 구현과 조회·이벤트 등 단일 Service 클래스에 동일하게 적용하며, 단순 필드 대입만 하는 생성자는 직접 작성하지 않는다.
- 기존 Lombok 사용 예시가 없다는 이유만으로 이 기본값을 생략하지 않는다. Lombok 의존성과 annotation processor 설정을 확인하고, 없으면 대상 빌드 방식에 맞게 추가한다. 버전은 프로젝트의 의존성 관리와 JDK 호환 기준을 따른다.
- 사용자나 프로젝트의 명시적 지침이 Lombok 사용을 금지하거나 수동 생성자를 요구하면 그 지침을 따른다. `super(...)`, 추가 초기화 로직, 생성자 인자의 주입 한정자 등 생성된 생성자로 동일한 계약을 유지할 수 없는 경우에는 필요한 명시적 생성자를 사용하고 이유를 남긴다.
- 기존 Service의 일부 로직만 수정하는 작업에 생성자 일괄 교체를 추가하지 않는다. 이 규칙은 Entity·DTO나 모든 Java 클래스의 생성 방식을 정하지 않는다.

```java
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ScheduleQueryService {
    private final ScheduleRepository scheduleRepository;
}
```

구현 후에는 import, `private final` 의존성 필드, Lombok 처리 설정을 확인한다. 프로젝트의 컴파일 경로로 생성자 생성과 호출부 연결을 확인하고, 실행하지 못한 검증은 구분해 보고한다.

## Service 트랜잭션과 readOnly

- DB에 접근하는 Service의 트랜잭션 경계에는 Spring의 `org.springframework.transaction.annotation.Transactional`을 사용하고, **읽기만 수행하면 `@Transactional(readOnly = true)`, 쓰기가 포함되면 `@Transactional`을 기본으로 사용한다.** `readOnly`의 기본값이 `false`이므로 쓰기 선언에 `readOnly = false`를 별도로 적지 않는다. DB 접근이 없는 Service까지 트랜잭션을 일괄 추가하지 않는다.
- `readOnly`는 트랜잭션의 읽기·쓰기 의도와 함께 **읽기 전용 DB로 분기하는 기준**으로 사용한다. 이 분기를 구성한 프로젝트에서는 `true`가 읽기 전용 DB, `false`가 쓰기 가능한 DB를 선택하도록 기존 라우팅 계약을 따른다. 어노테이션만으로 Spring이 DB 분기를 자동 제공하거나 쓰기를 반드시 차단한다고 해석하지 않는다. 라우팅 구성이 없는 프로젝트에 이 규칙만으로 다중 DB 구성을 새로 만들지는 않는다.
- 읽기·쓰기 판단은 메서드 이름이나 반환형보다 실제 호출 흐름을 기준으로 한다. INSERT·UPDATE·DELETE, JPA 변경 감지, 쓰기를 수행하는 하위 호출이 하나라도 있으면 전체 업무 경계를 `false`로 둔다. 결과 DTO를 반환한다는 이유로 조회 전용으로 분류하지 않는다.

| Service의 동작 | 기본 배치 |
| --- | --- |
| 읽기 전용 DB에서 처리할 수 있는 조회만 수행 | 클래스에 `@Transactional(readOnly = true)` |
| 모든 업무 메서드가 쓰기를 포함 | 클래스에 `@Transactional` |
| 조회와 쓰기 메서드가 함께 있음 | 클래스에 `@Transactional(readOnly = true)`, 쓰기 메서드에 `@Transactional` |

- 기존 프로젝트가 메서드별로 어노테이션을 두는 방식이면 그 배치를 유지하되 각 진입 메서드의 유효한 `readOnly`를 확인한다. 클래스와 값이 같은 메서드에 어노테이션을 중복할 필요는 없다. 클래스가 `readOnly = true`이면 쓰기 메서드의 `@Transactional` 자체는 생략하지 않는다.
- **특별한 요구가 없으면 조회에는 `readOnly = true`만 지정하고 쓰기에는 속성을 지정하지 않는다.** `isolation`, `propagation`, `timeout`, `rollbackFor` 등을 관성적으로 추가하지 않는다. 별도 격리 수준·독립 트랜잭션·체크 예외 롤백·트랜잭션 매니저 선택이 필요한 경우에만 필요한 속성을 지정하고 이유를 남긴다. 기존의 추가 속성은 그 필요성을 확인하지 않고 제거하지 않는다.
- 읽기만 하더라도 쓰기 DB의 최신값이 필요하거나 쓰기 DB에서 수행해야 하는 잠금 조회라면 `@Transactional`로 기본값 `readOnly = false`를 적용하고 이유를 남긴다. 같은 업무에서 앞선 쓰기의 결과를 읽는 경우도 기존 쓰기 트랜잭션과 일관성을 유지한다.
- 실제 DB 선택은 적용된 트랜잭션과 커넥션 획득 시점의 라우팅에 달려 있다. 상위 트랜잭션 참여나 같은 객체 내부 호출이 있으면 [트랜잭션 호출 경계](references/structure-decisions.md#트랜잭션-호출-경계)를 확인한다. 메서드의 `readOnly` 값만 보고 호출 도중 DB가 바뀐다고 가정하지 않는다.

변경 후에는 클래스·메서드의 유효한 `readOnly`, 하위 호출의 실제 쓰기 유무, 추가 속성의 사유를 확인한다. 라우팅 DB 선택은 해당 구성을 사용하는 테스트나 데이터소스 선택 로그로 확인하고, 소스 검토만 한 경우 실제 읽기 전용 DB 접근까지 검증했다고 보고하지 않는다.

## 조건에 따라 읽을 자료

- Service·Controller 등의 메서드·생성자 구현을 작성·수정할 때: [Java 구현 코드 가독성](../../backend/java-code-readability/SKILL.md)의 구간·줄바꿈·지역변수 기준을 적용한다. 이 작업을 지원하는 개별 배포본에는 `backend/java-code-readability`도 인벤토리의 상대 배치를 유지하여 포함한다.
- 앱과 관리자·다른 서버에서 같은 업무를 호출하거나, 알림·예약·파일 정리 등 후처리를 분리할 때: [진입점과 후처리 경계](references/boundary-variants.md).
- 기존 코드와 이 기본안이 다르거나 계층·패키지 분리 범위를 판단할 때: [구조 선택과 적용 조건](references/structure-decisions.md).

## 과도하게 확장하지 않을 규칙

- Service가 `presentation.dto`를 사용하거나 Entity가 요청 DTO를 받는 기존 구조도 허용한다. 이 관례를 엄격한 계층 독립성이나 별도 port/adapter 구조로 바꾸어 해석하지 않는다.
- 이벤트 수신·스케줄·외부 처리 전담 서비스는 필요한 경계가 없으면 단일 클래스로 둘 수 있다. 모든 `@Service`에 `Interface/Impl` 쌍을 만들지 않는다.
- `domain` 위치나 DTO 하위 폴더가 다른 기존 도메인은 이번 기능에 필요한 부분만 확장한다. 요청 범위를 넘는 전체 패키지 이동이나 이름 정규화를 하지 않는다.
