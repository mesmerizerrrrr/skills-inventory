# H2와 Repository 테스트 설정

이 문서는 Repository 계층의 실제 쿼리·JPA 기능을 검증할 때만 사용한다. Service·Controller·도메인 객체 테스트에는 이 설정을 복사하지 않는다.

## 필요한 구성만 연결

1. 테스트할 Repository 메소드와 Entity·테이블·QueryDSL 구현을 확인한다. JPA Repository라면 `@DataJpaTest`, JDBC DAO라면 `@JdbcTest` 등 필요한 DB 구성만 선택한다. 어노테이션의 import 경로와 테스트 모듈은 프로젝트의 Spring Boot 버전에 맞춘다.
2. H2 의존성을 Maven의 `test`, Gradle의 `testRuntimeOnly` 등 테스트 범위에 둔다. 테스트 Java 코드에서 H2 API를 직접 참조하는 경우에만 컴파일에도 필요한 테스트 의존성을 사용한다.
3. `src/test/resources/application-test.yml`에 테스트 DB 설정을 두고 테스트 클래스에서 `@ActiveProfiles("test")` 등으로 활성화한다. 이 파일은 이름만으로 자동 활성화되지 않는다.
4. QueryDSL의 `JPAQueryFactory`·커스텀 Repository·공통 RepositorySupport 등에 필요한 연결만 `src/test/java`의 `@TestConfiguration`과 명시적 `@Import`로 제공한다. 대상 구현은 실제 클래스를 사용하고, 쿼리 실행 자체를 mock하지 않는다.
5. 기존 애플리케이션의 광범위한 스캔·다중 DataSource·외부 연동 설정 때문에 slice가 실패하면 test 경로에서 Entity·Repository·설정의 로드 범위를 좁힌다. 실패를 피하려고 `@SpringBootTest`로 전환하거나 main 설정을 수정하지 않는다.

`@TestConfiguration`과 `@Import`는 테스트 Bean을 추가하는 수단이며, 기본 애플리케이션 설정 탐색까지 차단하지는 않는다. 애플리케이션 설정을 배제해야 하면 test 경로에 최소 `@Configuration`을 두고 `@ContextConfiguration(classes = ...)`으로 명시한다. 필요한 Entity·Repository만 탐색하고, 추가 QueryDSL Bean은 해당 테스트 구성에 연결한다. 정상적으로 격리되는 기존 slice까지 일괄 교체하지 않는다.

## 테스트 리소스 설정 예시

아래는 단일 DataSource와 JPA를 사용하는 프로젝트의 `src/test/resources/application-test.yml` 예시다. 테스트 slice의 내장 DB 교체 정책과 실제 DataSource를 확인하여 H2 선택이 반영되게 한다.

```yaml
spring:
  datasource:
    embedded-database-connection: h2
    generate-unique-name: true
  jpa:
    hibernate:
      ddl-auto: create-drop
```

- H2와 JDBC/JPA 관련 의존성이 있어야 한다. 이 설정은 테스트 클래스에 연결한 profile의 일부이며, 파일만 추가한 것을 DB 검증 완료로 보지 않는다.
- 자동 내장 DB 구성을 사용하는 예시이므로 URL을 생략했다. 운영 설정의 URL이나 커스텀 DataSource가 우선한다면 test 경로의 설정에서 명시적인 `jdbc:h2:mem:<테스트용이름>` URL과 driver·사용자 정보를 지정한다. 파일 DB나 외부 서버 URL을 사용하지 않는다.
- 명시적인 URL을 사용하면 `generate-unique-name`이 그 URL의 DB 이름까지 바꿔주지 않는다. 서로 다른 컨텍스트·병렬 실행 사이의 DB 이름 충돌과 데이터 공유 여부를 따로 확인한다.
- JPA가 없는 JDBC 테스트에는 `spring.jpa` 설정을 추가하지 않는다. 필요한 DDL·데이터 SQL은 `src/test/resources`에 두고, 해당 테스트에만 연결한다.
- 기존 Flyway/Liquibase·SQL 초기화가 운영 DB 전용 문법을 사용하면 test profile에서 해당 실행을 제어하고 H2용 최소 스키마를 test 리소스로 준비한다. Hibernate DDL과 SQL·migration을 중복 실행하지 않는다. 스키마·마이그레이션의 운영 호환성을 검증한 것으로 해석하지 않는다.
- 다중 DataSource에서는 실제로 사용할 각 연결이 H2 메모리 DB인지 확인한다. 첫 번째 연결만 교체하고 나머지를 운영 설정에 남겨두지 않는다. JDBC 연결 metadata와 활성 설정을 확인하되 비밀값은 출력하지 않는다.

Spring Boot의 [내장 DB 지원](https://docs.spring.io/spring-boot/reference/data/sql.html)과 [테스트 slice](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)는 버전별 세부 설정 확인용 참고 자료다.

## 쿼리 결과를 검증하는 방법

- **QueryDSL 조회**: `given`에서 조건에 맞는 데이터와 제외되어야 할 데이터를 함께 저장한다. JPA이면 필요한 `flush`·`clear` 후 `when`에서 대상 조회 메소드를 호출한다. `then`에서 실제 결과의 ID·필드·정렬·페이징 중 계약에 해당하는 항목을 확인한다.
- **정렬 계약**: 결과 순서를 assertion으로 확인하고, 실제 구현의 명시적인 `orderBy`도 확인한다. H2가 우연히 PK 순서로 반환한 결과만으로 쿼리가 정렬을 보장한다고 판단하지 않는다.
- **조회 분기**: 결과 있음·없음, 선택 검색 조건의 존재·부재, 경계값 등 의미 있는 조건마다 별도 `@Test`를 작성한다. 여러 조건을 한 테스트에서 바꿔가며 재조회하지 않는다.
- **JPA 저장·수정·삭제**: 대상 메소드를 `when`에서 실행하고 필요한 `flush`·`clear`를 거쳐 `then`에서 DB 재조회 결과를 검증한다. 영속성 컨텍스트의 기존 객체만 확인해 실제 저장 검증으로 오인하지 않는다. 제약조건 예외가 flush 시점에 발생하면 `when`에서 호출과 flush를 함께 포착한다.
- **격리**: 지원되는 테스트 트랜잭션의 롤백을 기본으로 사용한다. 직접 JDBC 연결·별도 트랜잭션·비동기 실행은 그 롤백에 참여하는지 확인하고, 참여하지 않으면 테스트 전용 초기화·정리를 명시한다. 테스트 실행 순서에 의존하지 않는다.
- **fixtures**: Entity 생성은 기능별 fixture 클래스로 묶되, 해당 테스트의 DB 저장과 조건 데이터 구성은 `given`에서 보이게 작성한다.

JPA Repository의 기능 테스트는 현재 요청과 애플리케이션의 영속성 계약에 필요한 범위로 작성한다. 상속받은 모든 메소드를 기계적으로 나열하지 않는다. H2 호환 모드가 특정 문법 실행을 도와도 운영 DB의 모든 함수·타입·잠금 동작까지 같다고 간주하지 않는다.
