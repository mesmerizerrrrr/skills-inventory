---
name: java-domain-api-structure
description: "Java/Spring API의 도메인별 디렉토리·패키지, Service 생성·의존 관계·트랜잭션을 구성하거나 순환 의존을 해소할 때 사용한다. 기존 패키지 스타일, 도메인 Service와 BridgeService의 책임·의존 방향, 생성자 주입과 트랜잭션 경계를 다루며, 문서만 작성하는 작업에는 적용하지 않는다."
---

# 도메인별 Java API 구조

## 적용 기준

업무 도메인 안에서 API 진입점·서비스·저장소의 책임을 구분한다. 사용자 요청과 대상 프로젝트의 지침·기존 구조를 먼저 따른다. 다른 구조를 사용하는 프로젝트를 이 패턴으로 일괄 개편하지 않는다.

Service 클래스를 새로 만들 때는 [Service 의존 방향과 BridgeService](#service-의존-방향과-bridgeservice), [신규 Service 생성자 주입](#신규-service-생성자-주입)과 DB 접근에 해당하는 [Service 트랜잭션과 readOnly](#service-트랜잭션과-readonly)를 적용한다. 기존 Service의 의존 관계나 트랜잭션을 조정할 때는 해당 절을 적용한다. 이 규칙을 읽었다는 이유로 기존 패키지를 재편하거나 `Interface/Impl` 분리를 추가하지 않는다.

## 디렉토리 생성·변경 전 스타일 선택

**디렉토리를 새로 만들거나 이동·이름 변경할 때는 대상 프로젝트의 기존 디렉토리 명명 규칙을 먼저 확인하고, 아래 두 스타일 중 맞는 것을 선택한다.** 프로젝트명이나 로컬 경로만으로 결정하지 않고 실제 `package` 선언과 Controller → Service → Repository 연결을 확인한다.

| 스타일 | 구분할 주요 디렉토리 |
| --- | --- |
| `presentation/application/infrastructure` | API 진입점은 `presentation`, 서비스는 `application/service`, 저장소는 `infrastructure` |
| `controller/service/repository` | API 진입점은 `controller`, 서비스는 `service`, 저장소는 `repository`; 기존 `dataprovider/db` 배치도 이 스타일의 변형으로 유지 |

1. 사용자·프로젝트의 명시적 구조 지침을 우선한다. 기존 도메인을 확장하면 그 도메인의 명명을 그대로 이어 쓴다.
2. 새 도메인이면 같은 모듈의 관련 도메인들을 대조해 반복되는 스타일을 선택한다. 다른 모듈의 예시 하나나 이 문서의 첫 번째 스타일을 기본값으로 삼지 않는다.
3. 선택 후에는 [두 가지 패키지 스타일](references/package-styles.md)에서 역할별 위치와 변형을 확인한다. 필요한 역할의 디렉토리만 만들고, 같은 역할의 `controller`와 `presentation` 또는 `repository`와 `infrastructure`를 예시 때문에 중복 생성하지 않는다.
4. 두 스타일이 혼재하면 작업 대상 도메인, 같은 모듈의 관련 도메인 순으로 판단한다. 기존 구조가 두 스타일과 다르면 그 구조를 우선하며, 근거가 없는 새 구조의 선택은 사용자에게 확인한다. 스타일 선택을 기존 디렉토리의 일괄 이동·이름 정규화로 확대하지 않는다.

다른 스킬의 특정 패키지 경로 예시도 선택한 스타일과 대상 도메인의 실제 위치에 맞춰 해석한다. 디렉토리명 대응은 역할의 위치를 정하는 규칙이며 서비스 책임·API 계약·트랜잭션 동작을 바꾸는 근거가 아니다.

## 구현 순서와 배치

1. 같은 업무의 Controller, Service, Repository를 찾아 신규 기능의 소유 도메인을 정한다. 기존 도메인이 있으면 그 경계를 이어 쓰고, 단순히 공용으로 보인다는 이유로 `commons`에 옮기지 않는다.
2. 디렉토리를 생성·변경하기 전에 위 선택 절차를 적용한다. Entity·DTO·예외·이벤트·문서의 위치도 선택한 스타일과 기존 도메인의 하위 패키지·단복수에 맞춘다.
3. 도메인의 주 업무 Service는 인터페이스와 `impl` 구현으로 나눈다. 여러 도메인을 조합하는 `BridgeService`는 Controller가 직접 호출하더라도 단일 `@Service` 클래스로 둘 수 있으며 인터페이스를 필수로 만들지 않는다. Controller는 요청 바인딩, 인증 주체·경로값 전달과 서비스 호출을 맡고, 도메인 내부 처리는 도메인 Service에, 도메인 간 처리 조합은 BridgeService에 둔다. 신규 Service의 의존성 주입은 아래 기본 규칙을 따른다.
4. 저장소가 JPA 기본 기능과 별도 조회를 함께 제공한다면 `Repository extends JpaRepository<...>, CustomRepository`로 결합한다. 별도 조회 구현은 선택한 스타일의 저장소 구현 위치에 둔다. 파생 쿼리만 필요한 작은 저장소에 빈 CustomRepository를 만들지는 않는다.
5. 필요한 변형만 아래 참고 자료에서 적용한다. 구현이 끝나면 선택한 스타일과 참고한 기존 경로를 간단히 설명하고, 디렉토리와 `package`·import의 일치, 새 파일의 소유 도메인, 진입점의 요청자 전달, BridgeService 사용 여부에 따른 의존 방향과 저장소 연결을 확인한다. 이동·이름 변경이 있었다면 해당 패키지를 지정하는 스캔 설정과 테스트 경로도 확인한다.

## Service 의존 방향과 BridgeService

도메인마다 주 업무 Service를 중심으로 책임을 구성하되, **도메인당 Service 클래스가 정확히 하나여야 한다는 제한은 두지 않는다.** 필요한 조회·이벤트·후처리 전담 Service와 기존 업무별 분리는 유지한다. 여기서 계층(layer)은 디렉토리 깊이나 `@Service` 어노테이션 유무가 아니라 업무 책임과 의존 방향을 뜻한다.

```text
단일 도메인 업무: Controller → DomainService → Repository
도메인 조합 업무: Controller → XxxBridgeService → 각 DomainService → 각 Repository
```

- **서로 다른 도메인의 업무 Service를 직접 주입하거나 호출하지 않는다.** 단방향 조회 호출도 포함한다. 다른 도메인의 기능이 필요한 업무 흐름은 상위 BridgeService에서 각 도메인 Service를 호출하도록 구성한다. 같은 계층의 단방향 호출 자체가 Spring 오류라는 뜻은 아니며, 상호 의존의 확대를 예방하기 위한 구조 규칙이다.
- BridgeService는 여러 도메인의 호출 순서·조건·결과를 조합할 때만 만든다. 단일 도메인의 메서드 여러 개, 여러 Repository·테이블의 사용, Controller 수나 주입 필드 수만으로 추가하지 않는다.
- 도메인 Service는 BridgeService에 의존하지 않고, BridgeService는 다른 BridgeService나 Repository를 직접 주입·호출하지 않는다. Repository 등 하위 구성요소도 상위 Service·BridgeService를 참조하지 않는다. 공통 컴포넌트를 거친 간접 역참조도 금지하며, 기존 도메인 내부의 보조 Service 분리도 순환 없이 유지한다.
- 공통 유틸리티·외부 API Client 등은 실제 책임으로 구분한다. 이름에 `Service`가 있다는 이유만으로 도메인 업무 Service로 분류하거나, 이름만 Client·Helper로 바꿔 금지된 업무 의존을 숨기지 않는다.
- BridgeService는 `<업무명>BridgeService`로 명명한다. 개별 도메인의 검증·상태 변경은 해당 도메인 Service에 남긴다. 공통 로직 재사용만 필요하면 하위 공통 컴포넌트 분리도 검토하며, BridgeService를 모든 순환 의존의 유일한 해결책으로 삼지 않는다.
- 신규·변경 업무의 의존 관계에 적용한다. 기존 구조가 다르면 요청한 흐름과 연결된 의존을 확인해 필요한 범위만 바꾸고, 전체 프로젝트의 서비스를 일괄 재편하지 않는다. `@Lazy`, setter 주입, `ObjectProvider`·`getBean`, 순환 참조 허용 설정을 구조 개선의 대체 수단으로 추가하지 않는다.

도메인 조합을 구현하거나 순환 의존을 해소할 때는 [BridgeService의 선택·책임·구현 예시](references/bridge-services.md)를 읽는다. 기존의 상호 주입을 제거했는지, 상위로 되돌아가는 경로가 없는지, 로직 이동 후 트랜잭션 범위가 유지되는지 확인한다.

## 신규 Service 생성자 주입

- **새로 만드는 Service 클래스는 Lombok `@RequiredArgsConstructor`와 `private final` 의존성 필드를 기본으로 사용한다.** 주 서비스 구현과 조회·이벤트 등 단일 Service 클래스에 동일하게 적용하며, 단순 필드 대입만 하는 생성자는 직접 작성하지 않는다.
- 주입 필드의 상단 배치·빈 줄, 공개 메서드 우선 배치와 클래스 종료 전 빈 줄은 [클래스 멤버 배치와 빈 줄](../../backend/java-code-readability/SKILL.md#클래스-멤버-배치와-빈-줄)을 따른다. 해당 공통 스킬을 함께 배포하는 범위는 아래 참고 자료에 명시한다.
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

- DB에 접근하는 Service의 트랜잭션 경계에는 Spring의 `org.springframework.transaction.annotation.Transactional`을 사용하고, **읽기만 수행하면 `@Transactional(readOnly = true)`, 쓰기가 포함되면 `@Transactional`을 기본으로 사용한다.** `readOnly`의 기본값이 `false`이므로 쓰기 선언에 `readOnly = false`를 별도로 적지 않는다. BridgeService처럼 하위 Service를 통해 DB에 간접 접근하는 흐름도 포함하며, 함께 성공·실패해야 하는 변경은 BridgeService의 외부 호출 메서드를 바깥 경계로 삼는다. DB 접근이 없는 Service까지 트랜잭션을 일괄 추가하지 않는다.
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

- Service·Controller 등의 클래스를 생성하거나 멤버 배치·메서드·생성자 구현을 작성·수정할 때: [Java 구현 코드 가독성](../../backend/java-code-readability/SKILL.md)의 클래스 배치·빈 줄·구간·줄바꿈·지역변수 기준을 적용한다. 이 작업을 지원하는 개별 배포본에는 `backend/java-code-readability`도 인벤토리의 상대 배치를 유지하여 포함한다.
- 앱과 관리자·다른 서버에서 같은 업무를 호출하거나, 알림·예약·파일 정리 등 후처리를 분리할 때: [진입점과 후처리 경계](references/boundary-variants.md).
- 기존 변형을 유지하거나 계층·패키지 분리 범위를 판단할 때: [구조 선택과 적용 조건](references/structure-decisions.md).

## 과도하게 확장하지 않을 규칙

- Service가 선택한 스타일의 요청·응답 DTO를 사용하거나 Entity가 요청 DTO를 받는 기존 구조도 허용한다. 이 관례를 엄격한 계층 독립성이나 별도 port/adapter 구조로 바꾸어 해석하지 않는다.
- BridgeService와 이벤트 수신·스케줄·외부 처리 전담 서비스는 단일 클래스로 둘 수 있다. 모든 `@Service`에 `Interface/Impl` 쌍을 만들지 않는다. 기존 인터페이스는 이 허용 규칙만을 이유로 제거하지 않는다.
- `domain` 위치나 DTO 하위 폴더가 다른 기존 도메인은 이번 기능에 필요한 부분만 확장한다. 요청 범위를 넘는 전체 패키지 이동이나 이름 정규화를 하지 않는다.
