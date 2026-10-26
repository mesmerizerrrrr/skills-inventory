# 빌드·프로필 초기 설정

## 버전과 빌드 골격

사용자에게 확인한 Spring Boot·JDK를 기준으로 아래 조합을 맞춘다. 두 버전의 확인 절차는 [진입 지침](../SKILL.md#생성-전에-확정할-입력)을 따른다.

| 구성 | 초기 결정 |
| --- | --- |
| Spring Boot | 정확한 플러그인/parent 버전과 BOM을 맞춘다. 관리되는 Spring·Jackson·Hibernate 버전을 개별 고정하지 않는다. |
| JDK | Gradle Java toolchain 또는 Maven compiler 설정과 실행 환경을 맞춘다. Gradle 실행 JVM과 컴파일 toolchain의 호환성도 각각 확인한다. |
| 빌드 도구 | 지정한 Gradle/Maven을 따른다. 미지정 시 Gradle Groovy DSL을 후보로 제시하되 현재 조직 지침을 우선한다. 호환되는 Wrapper를 함께 제공한다. |
| 애플리케이션 | base package 아래에 `@SpringBootApplication`을 두어 공통 설정과 이후 도메인이 스캔되게 한다. 실행 JAR을 기본 후보로 삼고 WAR은 요구가 있을 때 선택한다. |
| 테스트 | Boot에 맞는 테스트 starter와 JUnit Platform을 연결하고, 보안 테스트가 있으면 `spring-security-test`를 추가한다. |

Spring Initializr 또는 선택 버전을 지원하는 빌드 도구로 골격·Wrapper를 생성할 수 있다. 요청한 버전을 생성기가 지원하지 않으면 임의로 다른 버전을 선택하지 말고 동일 버전의 올바른 빌드 구성을 작성한다. 다운로드가 불가능하면 실제로 생성되지 않은 Wrapper나 성공하지 않은 빌드를 완료했다고 기록하지 않는다.

필요한 기본 의존성은 MVC/JSON, Validation, Security와 테스트 지원이다. 사용자 요구가 보안 라이브러리 자체를 제외하면 그 선택을 따르고 접근 제어 범위를 기록한다. Lombok을 사용할 때 `compileOnly`와 `annotationProcessor`를 함께 설정하며, 테스트에서도 쓰면 테스트용 processor도 연결한다. null 표기에는 프로젝트가 선택한 JSpecify 등의 체계를 사용하되 이를 Bean Validation의 대체로 설명하지 않는다.

JPA·DB driver·QueryDSL, Cloud/Feign BOM, Redis, OpenAPI, 암호화, 저장소 SDK는 선택한 구성에만 추가한다. 런타임/테스트/annotation processor 의존성을 구분하고, 같은 starter를 중복 선언하지 않는다. Spring Cloud·springdoc·QueryDSL처럼 별도 호환 범위가 있는 도구는 선택한 Boot/JDK와 맞는 배포 계열을 사용한다.

## 설정과 profile

- `application.yml`에는 애플리케이션 이름과 공통 정책을, `application-local.yml`·`application-test.yml` 등에는 필요한 환경 차이를 둔다. 환경 이름은 실제 배포 규칙에 맞춘다.
- 활성 profile은 실행 인자·환경변수로 정하도록 안내한다. 기본 파일에 운영 profile을 박아두거나 테스트가 운영 접속 정보를 상속하게 하지 않는다.
- URL·포트·시간 제한·허용 origin·인증 키 등 환경별 값은 외부화한다. 관련 값은 `@ConfigurationProperties`로 묶고 `@ConfigurationPropertiesScan` 또는 명시적 등록으로 연결한다. 선택한 기능의 필수값에는 검증을 적용해 누락을 드러낸다.
- `.env` 파일이 있다는 이유로 Spring Boot가 자동으로 읽는다고 가정하지 않는다. 실제 환경변수 주입 또는 config import 방식과 실행 명령을 함께 안내한다.
- 실제 DB 계정·API key·암호화 master password는 소스와 예시에서 제외한다. Jasypt가 필요한 환경에서도 `ENC(...)` 처리용 master password는 외부 주입하고, 코드의 고정 암호나 복호화 라이브러리의 존재를 비밀 관리로 간주하지 않는다.
- 텍스트 인코딩은 UTF-8을 기준으로 맞추고, 서버 시간대와 API 날짜·시각 계약을 별도로 정한다. 로그 시간대와 JSON 시간대가 항상 같다고 가정하지 않는다.

YAML 들여쓰기를 포함한 전체 속성 경로를 확인한다. `spring.jackson`·`spring.profiles` 등의 설정이 사용자 정의 설정 아래에 잘못 들어가면 의도대로 적용되지 않을 수 있다. 파일의 문법 검사뿐 아니라 profile 적용 결과와 properties Bean·mapper의 실제 바인딩도 확인한다.

로그는 Boot 기본 로깅으로 시작한다. 파일 경로·회전 정책이 요구될 때만 `logback-spring.xml` 등을 추가하고, 로컬/운영 설정을 구분한다. SQL·바인딩 파라미터·HTTP 본문 전체 로깅을 공통 기본값으로 켜지 않는다. 인증 실패 등의 로그에 키·토큰·비밀번호를 넣지 않는다.

`.gitignore`에는 빌드 결과·생성 코드·개인 IDE 설정·비밀 설정 파일을 제외하되 Wrapper 실행 파일과 필요한 JAR/설정은 포함한다. 생성된 Q class를 원본 Java 소스처럼 커밋하지 않는다.

## 호환성 확인 지점

Boot major가 달라지면 starter, 설정 API와 JSON 라이브러리가 달라질 수 있다. 특히 다음은 복사 전에 구분한다.

- Boot 3의 기본 Jackson 2 구성과 Boot 4의 기본 Jackson 3 구성을 혼용하지 않는다. Jackson 3는 주된 group/package가 `tools.jackson`이며 Jackson annotations는 `com.fasterxml.jackson.annotation`을 유지한다.
- Jackson 2의 `Jackson2ObjectMapperBuilderCustomizer` 예시를 Jackson 3에 그대로 적용하지 않는다. Boot 4/Jackson 3 구성은 해당 버전의 `JsonMapperBuilderCustomizer` 등 지원되는 확장 지점을 사용한다.
- JPA·Validation의 `javax`/`jakarta` namespace, Security DSL, QueryDSL APT classifier, 테스트 어노테이션의 패키지와 starter 구성을 선택 버전에 맞춘다.

고정된 호환표를 이 문서에 누적하지 않는다. 필요한 사용 규칙은 위에 포함되어 있으며, 실제 버전 선정 시 공식 문서의 해당 릴리스 정보를 확인한다: [Boot 시스템 요구사항](https://docs.spring.io/spring-boot/system-requirements.html), [Boot JSON 구성](https://docs.spring.io/spring-boot/reference/features/json.html), [Spring의 Jackson 3 지원](https://spring.io/blog/2025/10/07/introducing-jackson-3-support-in-spring/).

## 초기 실행 확인

Gradle이면 `./gradlew --version`, `./gradlew clean test bootJar`, Maven이면 `./mvnw --version`, `./mvnw verify`를 기본 확인 경로로 삼는다. Maven은 Boot repackage 연결도 확인한다. Windows에서는 해당 `.bat` 또는 `.cmd` Wrapper를 사용한다.

실행할 profile과 의존성이 준비되면 `bootRun`/`spring-boot:run` 또는 생성한 JAR로 기동한다. 의존성이 준비되지 않은 상태에서는 컴파일·격리 테스트 결과와 로컬 기동 미확인을 분리해 보고한다. 테스트를 통과시키려고 제품 설정을 `permitAll`이나 운영 DB 연결로 바꾸지 않는다.
