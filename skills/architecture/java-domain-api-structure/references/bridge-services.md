# BridgeService의 선택과 구현

여러 도메인의 업무를 조합하거나 서비스 순환 의존을 해소할 때 읽는다. 허용·금지 의존 방향은 [Service 의존 방향과 BridgeService](../SKILL.md#service-의존-방향과-bridgeservice)를 기준으로 한다. BridgeService는 도메인 Service 위에서 업무 흐름을 조합하는 선택적 역할이며, Spring이 별도 계층으로 인식하거나 의존 방향을 강제하는 기능은 아니다.

## 생성 여부 판단

| 상황 | 구성 |
| --- | --- |
| 학생 등록 한 가지 업무를 수행 | Controller → StudentService. 전달만 하는 Bridge를 추가하지 않는다. |
| 등록 처리에서 학생 도메인의 등록과 수강 도메인의 신청을 조합 | Controller → RegistrationBridgeService → StudentService·EnrollmentService |
| 일정 처리에 다른 도메인의 학생 조회 결과가 필요 | Bridge가 StudentService에서 조회한 뒤 필요한 값을 ScheduleService에 전달한다. 조회만 하더라도 ScheduleService에 StudentService를 주입하지 않는다. |
| 한 Controller의 서로 다른 엔드포인트가 각각 독립된 도메인 업무를 호출 | 엔드포인트마다 해당 Service를 호출할 수 있다. 주입 필드가 둘이라는 이유로 Bridge를 추가하지 않는다. |
| 한 도메인의 Service가 여러 Repository를 사용하거나 조회 SQL이 여러 테이블을 조인 | 그 사실만으로 Bridge를 만들지 않는다. 실제 업무 책임과 도메인 간 서비스 조합 여부를 판단한다. |
| 여러 Controller가 같은 단일 도메인 업무를 호출 | 기존 도메인 Service를 공유한다. 진입점 개수는 Bridge 생성 조건이 아니다. |
| 업무 완료 뒤 독립된 알림·파일 정리가 필요 | [이벤트 후처리](boundary-variants.md#이벤트-후처리)의 시점·실패 계약을 따른다. 기존 후처리를 모두 Bridge로 옮기지 않는다. |

복잡도나 코드 길이에 임계값을 두지 않는다. 두 도메인의 짧은 동기 조합에도 Bridge가 필요할 수 있고, 긴 단일 도메인 처리에는 필요하지 않을 수 있다.

## 책임과 소유권

- Bridge는 도메인 호출 순서, 호출 결과에 따른 분기, 도메인 간 흐름의 조건과 응답 조립을 맡는다. 각 도메인의 입력·상태 검증과 변경 규칙은 도메인 Service에 둬서 직접 호출하는 다른 진입점에도 적용되게 한다.
- 도메인 Service는 필요한 값·식별자를 인자로 받는다. Bridge나 다른 도메인의 Service 객체·콜백을 넘겨받아 역으로 호출하는 방식으로 의존 방향을 우회하지 않는다.
- 다른 도메인 Service 대신 그 Repository를 직접 주입해 해당 도메인의 검증·상태 변경을 우회하지 않는다. 여러 테이블을 사용하는 조회와 다른 도메인의 업무 로직을 대신 구현하는 행위를 구분한다.
- `<업무명>BridgeService`처럼 조합의 목적을 이름에 드러낸다. 전역 `BridgeService` 하나에 무관한 업무를 계속 모으거나 모든 도메인에 Bridge를 하나씩 만들지 않는다.
- 조합 업무를 소유한 도메인에 둔다. 여러 도메인을 연결한다는 이유로 `commons`로 옮기지 않으며, 기존에 별도 업무 흐름 모듈이 있으면 그 소유권을 따른다. 구체적인 위치는 [패키지별 BridgeService 배치](package-styles.md#bridgeservice-배치)를 따른다.
- Controller가 직접 호출하는 Bridge도 단일 `@Service` 클래스로 작성할 수 있다. 도메인 주 서비스의 Interface/Impl 규칙을 Bridge에 자동 적용하지 않는다. 신규 클래스의 생성자 주입은 [기존 Lombok 규칙](../SKILL.md#신규-service-생성자-주입)을 그대로 따른다.

## 트랜잭션을 포함한 구현 예시

다음은 학생 등록과 수강 신청이 같은 트랜잭션 매니저의 DB에서 함께 성공·실패해야 하는 예다. `StudentService.register`와 `EnrollmentService.enroll`은 각 도메인의 검증·변경을 담당하며, 서로를 주입하지 않는다. 예시의 타입·메서드명은 실제 프로젝트의 계약에 맞춘다.

```java
@Service
@RequiredArgsConstructor
public class RegistrationBridgeService {

    private final StudentService studentService;
    private final EnrollmentService enrollmentService;

    @Transactional
    public Long register(RegistrationRequest request) {
        // 학생 등록
        final Long studentId = studentService.register(request.student());

        // 수강 신청
        enrollmentService.enroll(studentId, request.courseId());

        return studentId;
    }

}
```

- 필요한 import는 `lombok.RequiredArgsConstructor`, `org.springframework.stereotype.Service`, `org.springframework.transaction.annotation.Transactional`과 해당 프로젝트 타입이다. 외부 진입점은 주입받은 Bridge의 공개 메서드를 호출한다.
- 하위 호출까지 포함해 [Service 트랜잭션과 readOnly](../SKILL.md#service-트랜잭션과-readonly)를 적용한다. 조회 조합은 읽기 전용 조건을 확인하고, 쓰기가 하나라도 포함된 업무 경계는 `@Transactional`을 사용한다. Repository를 직접 주입하지 않는다는 이유로 Bridge의 DB 접근을 누락하지 않는다.
- 같은 스레드·동일 트랜잭션 매니저에서 기본 `REQUIRED`로 참여하는 하위 Service는 Bridge의 트랜잭션을 공유한다. Bridge에 경계가 없으면 각 Service 호출이 따로 커밋될 수 있다. 함께 성공·실패할 업무라면 전파 설정과 예외의 롤백 조건을 확인한다.
- Bridge가 읽기 전용 트랜잭션을 시작한 상태에서 하위 쓰기 메서드를 호출해도 쓰기 트랜잭션으로 전환되지 않는다. 같은 객체 내부 호출, `REQUIRES_NEW`, 읽기 전용 DB 라우팅의 주의점은 [트랜잭션 호출 경계](structure-decisions.md#트랜잭션-호출-경계)를 따른다.
- 이름이 Bridge라는 이유만으로 트랜잭션을 붙이지 않는다. DB 접근이 없는 외부 호출 조합, 명시적으로 독립된 트랜잭션이 필요한 작업은 실제 경계에 맞춘다. 외부 HTTP 호출·서로 다른 트랜잭션 매니저·비동기 처리가 로컬 DB 트랜잭션 하나로 함께 롤백된다고 가정하지 않는다.

## 기존 순환 의존을 옮길 때

`AService → BService → AService`가 있으면 조합 흐름의 진입점을 Bridge로 올리고, A·B의 개별 기능은 각 Service에 남긴다. 호출자도 해당 Bridge로 연결하고 기존의 교차 주입을 제거한다. `AService → BridgeService → AService`처럼 연결을 바꾸거나 A·B의 상호 주입을 남긴 채 Bridge만 추가하면 해결되지 않는다.

이름만 변경하거나 인터페이스를 사이에 추가해도 실제 빈의 의존 그래프는 바뀌지 않을 수 있다. 공통 계산·정책의 재사용이 원인이면 상위 Bridge 대신 하위 공통 컴포넌트로 분리하는 편이 맞을 수 있다. 이벤트로 분리할 때는 주입 그래프뿐 아니라 동기 수신자의 재호출과 실행 시점·실패 계약도 확인한다.

변경 후에는 다음을 확인한다.

- 도메인 Service의 교차 의존과 상위로 되돌아가는 간접 경로가 제거됐는가?
- Bridge가 도메인 Service의 계약을 호출하며 기존 검증·실행 순서·예외·응답 의미가 유지되는가?
- 함께 성공·실패할 DB 변경에 같은 트랜잭션이 적용되는가? 원자성이 필요한 흐름은 후속 처리 실패 시 선행 변경도 롤백되는지 검증한다.
- 대상 프로젝트의 검증 경로로 컴파일과 Spring 컨텍스트 생성이 가능한가? 정적 검토·컴파일·컨텍스트 시작·실제 롤백 검증은 각각 수행 여부를 구분해 보고한다.

Spring의 생성자 순환 의존 동작은 [Dependency Injection](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html), `@Service`의 범용 역할은 [Service API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/stereotype/Service.html)를 참고할 수 있다. Bridge 명명과 허용 의존 방향은 이 인벤토리의 구조 규칙이다.
