# DB·외부 연동 초기 설정

## DB와 JPA를 선택했을 때

DB를 사용하지 않는 프로젝트에는 JPA starter·driver·DataSource와 DB 설정 요구를 추가하지 않는다. DB를 사용하면 종류·연결 방식·스키마 소유권과 읽기/쓰기 범위를 먼저 정한다.

- 연결 정보는 profile과 외부 설정으로 주입하고 pool 크기·timeout은 실제 환경에 맞춘다. 단일 DB가 충분하면 Boot DataSource 자동 설정으로 시작한다.
- 운영/공유 DB의 `ddl-auto`는 스키마 관리 방식에 따라 `none` 또는 `validate`를 선택한다. 테스트 전용 DB의 생성 정책은 별도로 둔다. 기존 테이블을 쓰는 서비스에 `update`·`create`·`create-drop`을 기본 적용하지 않는다.
- DDL 가드를 추가한다면 EntityManagerFactory의 DDL 실행보다 앞에서 잘못된 설정을 차단해야 한다. `ApplicationRunner` 검사만으로 이미 실행된 DDL을 막을 수 있다고 설명하지 않는다. DB 계정의 DDL 권한도 서비스 역할에 맞춘다.
- API 서비스는 `open-in-view=false`를 기본 후보로 두고, 필요한 조회와 응답 조립을 트랜잭션 범위 안에서 처리한다. Entity를 그대로 JSON으로 내보내도록 구성하지 않는다.
- 테스트에서 H2를 사용하면 PostgreSQL 등 실제 DB의 타입·함수·schema·locking까지 검증된 것으로 간주하지 않는다. 필요한 DB 통합 테스트만 실제 엔진의 격리 환경에서 수행한다.

## 공통 Entity와 auditing

공통 감사 컬럼이 실제 스키마에 있을 때 `@MappedSuperclass` 기반 공통 Entity를 만든다. PK·sequence·삭제 플래그·낙관적 잠금 필드를 모든 테이블에 강제하지 않는다.

| 서비스와 컬럼 | 구성 |
| --- | --- |
| 생성/수정 시각을 JPA에서 기록 | 날짜 감사 어노테이션, `AuditingEntityListener`, `@EnableJpaAuditing`을 연결 |
| 생성/수정 사용자도 기록 | `AuditorAware`와 실제 인증 principal을 연결. 익명/시스템 작업의 식별 정책을 별도로 정의 |
| 외부 시스템이 관리하는 테이블을 조회만 함 | 컬럼을 읽도록 매핑하되 불필요한 감사 쓰기 listener는 추가하지 않음 |

시각 타입·DB timezone·시스템 작업의 감사자 정책을 맞춘다. 감사자가 없을 때 임의 사용자 번호를 만들어 넣지 않는다. 쓰기 서비스에서 insert/update의 감사 필드 동작을 검증한다.

## DB 업무 코드 Converter

API 입력 변환과 JPA `AttributeConverter`는 별개다. DB 값의 의미와 실제 저장 타입이 확인된 경우에만 다음 기준으로 적용한다.

- 의미 있는 enum 이름이 DB 값과 같으면 `@Enumerated(STRING)`을 사용할 수 있다. 수량·식별자·비트마스크는 단일 업무 코드로 변환하지 않는다.
- `A`·`10` 같은 불투명 업무 코드가 `ORDINAL`/`STRING`으로 의미와 저장값을 그대로 표현할 수 없으면 의미 있는 enum과 Converter를 만든다.
- 여러 업무 코드 enum에 공통 계약이 필요하면 `PersistableCodeEnum<T>#getDbValue()`와 `DatabaseCodeConverter<E,T> implements AttributeConverter<E,T>`를 공통 기반으로 둘 수 있다. 각 구체 Converter는 enum 타입과 실제 저장 타입을 지정한다.
- `null → null`과 **미정의 코드 → 오류/명시적 UNKNOWN/허용된 null** 정책을 구별한다. 신규 계약의 기본은 미정의 값을 드러내는 것이며, 모든 예외를 잡아 null로 돌리는 구현을 복사하지 않는다.
- `autoApply=true`는 같은 Java 타입의 다른 필드에도 영향을 준다. 컬럼별 코드 계약이 다르면 명시적 `@Convert`를 선택하고, 같은 필드에 `@Enumerated`와 Converter를 함께 적용하지 않는다.

예를 들어 `A → ACTIVE`, `I → INACTIVE` 계약이면 두 값의 저장·복원, null, 미정의 `Z`를 검증한다. 이 설정만으로 API JSON도 `A/I`가 된다고 설명하지 않는다. 실제 구현의 상세 기준은 [JPA 업무 코드 enum 매핑](../../../database/jpa-coded-enum-mapping/SKILL.md)을 함께 적용한다.

## QueryDSL·읽기/쓰기 DB 분리

**QueryDSL이 필요한 경우** 선택한 JPA/JDK와 맞는 배포 계열·버전·namespace·APT classifier를 확인하고 core/JPA/APT 버전을 맞춘다. annotation processor와 main/test generated sources 경로를 연결한다. 임의로 다른 배포 계열의 classifier를 가져오지 않는다.

필요한 공통 `JPAQueryFactory` 또는 RepositorySupport가 있으면 중복 생성을 피하고 초기화 책임을 한 곳에 둔다. 기존 support가 없는 신규 프로젝트에 상속만 적어두지 말고 실제 필요한 최소 구현을 제공한다. 조회가 없는 상태에서 빈 CustomRepository/Impl을 양산하지 않는다. 사용한 Entity의 Q class가 Wrapper 컴파일에서 생성되는지 확인한다.

**읽기/쓰기 DB가 실제로 분리된 경우**에만 routing DataSource를 추가한다. 읽기 전용 트랜잭션과 쓰기 가능한 트랜잭션의 목적지를 정하고, routing DataSource·lazy connection 획득·transaction manager·`@Primary`/qualifier 연결을 구성한다.

`@Transactional(readOnly = true)`만으로 분리가 자동 제공되지는 않는다. 라우팅은 커넥션을 선택하는 시점의 트랜잭션 상태에 의존한다. 기본 목적지는 쓰기 DB로 두고, 상위 트랜잭션 참여·자기 호출·쓰기 직후 최신값 조회까지 고려한다. 분기를 추가했다면 실제 선택된 DataSource를 테스트로 확인한다.

## 요구가 있을 때만 추가할 연동

| 요구 | 초기 구성할 내용 |
| --- | --- |
| OpenAPI | Boot와 호환되는 springdoc, 실제 API 패키지·응답 envelope·오류·security scheme, 환경별 문서 공개 정책 |
| 외부 HTTP API | RestClient/Feign 등 선택한 Client, base URL·timeout·오류 매핑, 필요한 인증 헤더, 테스트 대체 서버. Feign 선택 시 Cloud BOM 호환성 확인 |
| Redis | 실제 저장 목적, key prefix·TTL·직렬화·접속 설정. 사용처 없는 Redis Bean은 제외 |
| 비동기 실행 | 필요한 executor의 pool·queue·오류 처리. 요청자/트랜잭션 context가 자동 전달된다고 가정하지 않음 |
| 스케줄 | 실행 profile·시간대와 실제 작업. 다중 인스턴스 중복 실행 방지가 필요할 때만 lock provider 구성 |
| 파일/객체 저장소 | 필요한 SDK·bucket/경로·권한·외부 자격증명과 테스트 방식 |

외부 시스템의 실제 endpoint·비밀값·버킷·스케줄 업무를 참고 코드에서 복사하지 않는다. 초기 프로젝트에서 검증한 것은 client 구성과 대체 서버 호출인지, 실제 외부 서비스 연동인지 구분한다.
