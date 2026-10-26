---
name: spring-boot-project-bootstrap
description: "신규 Java/Spring Boot API 프로젝트를 생성하고 빌드·프로필·보안·Jackson·API 응답과 공통 RuntimeException·필요한 DB 기반을 초기 구성할 때 사용한다. 미지정 Spring Boot·JDK 버전을 먼저 확인한다. 기존 프로젝트의 기능 추가·설정 유지보수·버전 업그레이드만 하는 작업에는 적용하지 않는다."
---

# 신규 Spring Boot 프로젝트 생성

업무 기능을 구현하기 전에 빌드·실행할 수 있는 프로젝트와 일관된 API 공통 기반을 만든다. Java와 Spring MVC REST API를 대상으로 하며, 배치·WebFlux·다른 언어가 명시되면 그 요구에 맞는 구성을 우선한다. 이 스킬의 MVC Advice·Filter 구성을 다른 실행 모델에 그대로 적용하지 않는다.

## 생성 전에 확정할 입력

**요청과 현재 대화에 Spring Boot 또는 JDK 버전이 없으면, 누락된 버전을 사용자에게 확인하고 답변을 받은 뒤 버전 의존 파일을 생성한다.** 참고 프로젝트의 버전이나 로컬에 설치된 JDK를 사용자의 선택으로 간주하지 않는다.

- Spring Boot는 사용할 릴리스 계열과 패치 버전, JDK는 빌드·실행 기준 major 버전을 정한다. 사용자가 계열만 정했으면 패치 선택 방침을 함께 확인한다.
- 버전 추천이 필요하면 선택 시점의 공식 지원·호환 범위와 필수 라이브러리 제약을 확인해 호환되는 조합을 제시한다. 이 문서에 특정 버전을 영구 기본값으로 고정하지 않는다.
- “최신 안정 버전으로”, “호환되는 버전은 알아서”처럼 선택을 명시적으로 위임받으면 그 범위에서 확인 후 선정한다. 이미 지정·확인된 버전은 다시 묻지 않는다.
- 답변이 없으면 임의로 버전을 확정하지 않는다. 요구사항 정리와 파일 구성안까지 진행하고, 빌드 파일·Wrapper·버전별 Java 설정 작성은 보류한다. 답변 대기는 승인으로 간주하지 않는다.

확인 예시:

> Spring Boot와 JDK 버전이 명시되지 않았습니다. 사용할 버전 조합을 알려주세요. 정해둔 기준이 없다면 필요한 라이브러리와 호환되는 안정 버전을 확인해 추천하겠습니다. Gradle/Maven 선호도도 함께 알려주세요.

아래 항목은 현재 요청·작업 지침에서 먼저 파악한다. 실제 생성에 필요한 미확정 선택만 묶어서 질문하고, 중요하지 않은 파일명까지 개별 승인을 받지 않는다.

| 입력 | 결정할 내용 |
| --- | --- |
| 프로젝트 식별 | 생성 경로, 프로젝트명, group/artifact, base package |
| 빌드·실행 | Gradle 또는 Maven, DSL, JAR/WAR, 빌드·실행 JDK, 배포 환경 제약 |
| 패키지 구조 | `presentation/application/infrastructure` 또는 `controller/service/repository` 등 사용할 스타일 |
| API 접근 | 공개 API, 사용자 인증 API, 서버 간 API 중 필요한 범위와 인증 제공자 |
| 저장소 | DB 사용 여부·종류, JPA·QueryDSL 필요 여부, 조회 전용/쓰기 서비스 |
| API 계약 | 공통 응답 형식, 날짜·시각·시간대, JSON과 query/path 입력 표현 |

빈 디렉토리인지 확인하고, 파일이 있으면 사용자가 요청한 초기 생성 범위와 충돌하는 파일부터 확인한다. 다른 서비스의 업무 코드·설정값을 통째로 복사하지 않는다.

## 기본 산출물과 선택 구성

REST API의 초기 기반은 아래 순서로 연결한다. 설정 클래스가 존재하는 것보다 실제 Bean·Filter·Converter·Advice 연결이 완료되는 것이 중요하다.

1. **빌드와 실행 골격**: Wrapper, 빌드 파일, 애플리케이션 진입점, 기본·환경별 설정, 테스트 실행 설정을 만든다. [빌드·프로필 초기 설정](references/build-and-config.md)을 읽는다.
2. **API 공통 계약**: `ResponseCode`, `CommonResponse<T>`, `BaseException extends RuntimeException`, 공통 예외 처리와 필요한 응답 Advice를 연결한다. Jackson과 MVC 변환의 경계를 포함해 [API 응답·예외·직렬화](references/api-contract.md)를 읽는다.
3. **접근 정책**: 공개·사용자·서버 간 경로에 맞는 `SecurityFilterChain`과 인증 실패 응답을 구성한다. 공개 API도 공개 범위를 명시한다. [보안 초기 설정](references/security.md)을 읽는다.
4. **저장소 기반**: DB가 필요한 경우에만 DataSource, JPA, 감사 필드, DB 코드 변환과 필요한 조회 기반을 추가한다. [DB·외부 연동 초기 설정](references/persistence-and-integrations.md)의 해당 절을 읽는다.
5. **선택 연동**: OpenAPI, Redis, 외부 HTTP Client, 비동기·스케줄, 파일 저장소 등은 초기 요구사항에 있는 구성만 추가한다. 사용할 계획이 없는 Bean과 비밀값 입력 요구를 미리 만들지 않는다.
6. **초기 검증과 전달**: 아래 완료 기준으로 확인하고 실행 명령·설정 입력·확정한 선택을 프로젝트 README에 남긴다. 업무 도메인이나 실제 배포·인프라 생성은 별도 요청 범위에 따른다.

역할 배치의 예시는 다음과 같다. 선택한 패키지 스타일에 맞춰 명명하고, 필요한 파일만 생성한다.

```text
<base-package>/
├── Application.java
└── commons/
    ├── config/                   # Security, 외부 연동, 설정 properties
    ├── application/exceptions/   # BaseException, 공통 업무 예외
    ├── presentation/             # ResponseCode, 공통 DTO·Advice, Jackson·MVC 설정
    └── infrastructure/db/        # DB 사용 시 JPA·감사·Converter·조회 지원
```

`commons`에는 여러 도메인이 공유하는 초기 계약만 둔다. 예제 업무를 위해 학생·예약·토큰 발급 등의 도메인을 만들지 않는다. 확인용 엔드포인트는 테스트 전용으로 둘 수 있으며, 공개 경로는 요구된 health/API 경로로 한정한다.

## 관련 스킬의 적용 범위

이 스킬의 초기 설정 판단과 예시는 동봉한 참고 문서만으로 이해할 수 있다. 구체적인 코드 작성이 아래 작업을 포함하면 해당 공통 지침도 적용한다. 인벤토리 전체를 배포하면 상대 참조가 유지되며, 부분 배포 시 사용하는 형제 스킬 폴더와 그 스킬이 명시한 의존 자료까지 같은 배치로 포함한다.

- Java 클래스 구현: [java-code-readability](../java-code-readability/SKILL.md).
- 도메인·Service까지 생성: [java-domain-api-structure](../../architecture/java-domain-api-structure/SKILL.md). 초기 공통 기반만 만드는 요청에 빈 Service·Repository 계층을 추가하지 않는다.
- 요청 DTO·업무 예외 구현: [java-api-validation-errors](../java-api-validation-errors/SKILL.md). 기존 계약에 연결하는 규칙이며, 초기 공통 계약의 생성은 이 스킬에서 담당한다.
- 실제 DB 업무 코드 매핑: [jpa-coded-enum-mapping](../../database/jpa-coded-enum-mapping/SKILL.md). 코드표가 없는 상태에서 임의 Converter를 생성하지 않는다.

## 초기 생성 완료 기준

- 확정한 Boot·JDK·빌드 도구 조합이 빌드 파일, Wrapper, 로컬 실행 안내와 일치한다. Wrapper로 컴파일·테스트·실행 산출물 생성을 확인한다.
- 필요한 설정만으로 테스트 컨텍스트가 뜨고, 준비된 로컬 의존성을 사용한 실행 여부를 별도로 확인한다. 실제 DB·인증 서버가 없으면 테스트 대체 구성과 미검증 연동을 명시한다.
- 검증 실패, 공통 업무 예외, 예상하지 못한 예외가 정한 계약대로 처리되는지 확인한다. 날짜/enum과 query/path 변환은 채택한 타입과 변환이 있는 경우에 검증하며, 검증만을 위해 불필요한 변환기를 만들지 않는다.
- 보안 경로의 인증 누락·실패·권한 부족과 공개 경로, 여러 체인이 있으면 경로 매칭을 검증한다. 인증 mock 테스트만으로 외부 인증 연동 완료를 주장하지 않는다.
- 응답 Advice를 사용하면 중복 포장, `String`, `void`/204, 명시적 상태·헤더, 파일·스트림 등 실제 지원하는 반환 유형의 동작을 확인한다.
- DB 코드 Converter를 도입한 경우 정상·null·미정의 값 정책을, 감사 필드를 도입한 쓰기 서비스는 해당 필드의 동작을 확인한다. 다중 DB 분기는 그 구성을 선택한 경우에만 확인한다.
- 프로젝트 README에는 확정 버전, 실행·테스트 명령, profile·필수 환경변수, 공통 응답/시간 형식, 선택한 구성과 미검증 항목을 남긴다. 실제 비밀값은 넣지 않는다.

결과를 전달할 때는 생성 위치, 채택한 초기 구성, 실행한 검증과 외부 환경 때문에 남은 확인 사항을 구분한다. 컴파일만 성공한 상태를 실제 서버·DB·인증 연동 성공으로 보고하지 않는다.
