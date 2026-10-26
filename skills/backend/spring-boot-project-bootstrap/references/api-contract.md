# API 응답·예외·직렬화

## 공통 응답과 RuntimeException

새 API에 별도 응답 계약이 없다면 다음 구조를 제안하고 초기 공통 기반으로 연결한다. 사용자가 다른 계약을 지정하면 그 계약을 우선한다.

| 구성 | 책임 |
| --- | --- |
| `ResponseCode` | 문자열 업무 코드, 기본 한글 메시지, HTTP status를 한 항목으로 관리한다. 처음에는 성공·잘못된 요청·인증 실패·권한 부족·미존재·서버 오류 등 필요한 코드만 둔다. |
| `CommonResponse<T>` | `code`, `message`, nullable `data`를 가진다. `success(data)`, `fail(code)`, `fail(code, message)` 팩토리로 조립한다. |
| `BaseException extends RuntimeException` | `ResponseCode errorCode`와 선택적 `customMessage`를 보유한다. `ResponseCode`만 받는 생성자는 코드의 메시지를, 상세 메시지를 받는 생성자는 전달 메시지를 `super(message)`에도 연결한다. |
| 공통 업무 예외 | 실제 사용하는 `InvalidArgumentException`, `NotFoundException` 등을 BaseException에 연결한다. 아직 없는 업무의 예외 목록을 미리 만들지 않는다. |
| `CommonExceptionAdvisor` | `@RestControllerAdvice`에서 업무 예외·요청 실패·알 수 없는 예외를 공통 응답과 실제 HTTP status로 변환한다. |
| `CommonResponseAdvice` | 자동 포장을 선택했을 때만 API Controller의 성공 반환값을 공통 응답으로 만든다. |

응답 예시의 코드값은 가상 값이다. 연동 규약이 있으면 그 값을 따르고, 없으면 신규 API의 규칙을 정한다.

```json
{"code":"SUCCESS","message":"성공","data":{"id":1}}
```

```json
{"code":"REQUEST_INVALID","message":"요청값을 확인해주세요.","data":null}
```

`code`는 클라이언트가 분기하는 업무 값이고 HTTP status와 별개다. 실패를 모두 HTTP 200으로 내보내거나 인증 오류를 일반 업무 오류로 취급하는 정책은 기존 예시에서 가져오지 않는다.

공통 예외 처리기는 다음 범위를 실제 사용 버전의 예외 타입에 연결한다.

- `BaseException`: 선택적 상세 메시지를 보존하고 `ResponseCode`에 지정된 HTTP status로 응답한다. 외부 응답에 허용되는 메시지만 상세 메시지로 넘긴다.
- DTO `@Valid`, 메서드 인자 검증, 필수 파라미터·헤더 누락: 잘못된 요청으로 처리한다. 필요하면 안전한 필드 오류 정보도 계약에 포함한다.
- 잘못된 JSON·enum·날짜, query/path 타입 불일치: 역직렬화/바인딩 예외를 400으로 연결한다. 포괄 `Exception` 처리로 떨어져 500이 되지 않게 한다.
- 알려진 프로토콜 오류: 404·405·415 등 프레임워크의 의미를 보존한다. 포괄 처리기가 이 상태를 전부 500으로 바꾸지 않게 한다.
- 예상하지 못한 예외: 서버 로그에는 원인을 남기고 응답에는 일반화한 500 메시지만 보낸다. SQL, 내부 경로, stack trace를 내보내지 않는다.

DTO 필수값·범위는 한글 `message`가 있는 Bean Validation 제약으로 표현하고 Controller에서 검증을 실행한다. DB 조회와 사용자 상태 판단은 이후 업무 Service에 둔다. Swagger의 제약 설명이나 null 표기는 런타임 검증이 아니다.

## 성공 응답 자동 포장

자동 포장을 선택하면 Controller는 DTO·목록 등을 반환하고 Advice가 한 번만 감싼다. `supports()`를 애플리케이션 API 패키지나 명시적 대상으로 제한해 OpenAPI·Actuator·라이브러리 응답까지 바꾸지 않는다.

- 이미 `CommonResponse`인 본문과 공통 예외 응답을 다시 감싸지 않는다.
- `ResponseEntity`의 status·headers를 유지한다. 201 등을 무조건 200으로 덮어쓰지 않는다.
- `void`를 200 + `data: null`로 표현할지, 204 No Content로 표현할지 정한다. 204에는 envelope를 쓰지 않는다.
- `String`은 이미 선택된 문자열 converter와 충돌할 수 있다. 응답 DTO로 통일하거나, 문자열 converter에 맞춰 같은 JSON mapper로 직렬화하는 처리를 구현·검증한다. JSON envelope를 직접 직렬화하면 Content-Type도 `application/json`으로 맞춘다.
- 파일·`Resource`·byte 배열·스트림·SSE·비 JSON media type은 포장 대상에서 제외한다. 실제 지원하는 타입과 제외 방식을 명시한다.

포장 대상의 판단과 converter 실행은 다른 단계다. 일반 객체 하나의 성공만으로 모든 반환 유형이 동작한다고 판단하지 않는다.

## 세 종류의 변환을 구분

| 경계 | 적용 수단 | 적용되지 않는 곳 |
| --- | --- | --- |
| JSON body ↔ Java DTO | Jackson serializer/deserializer, module/customizer, 필드 어노테이션 | query/path/form 문자열 바인딩, DB 컬럼 |
| query/path/form 문자열 ↔ Java 타입 | MVC `Converter`·`Formatter`, `@DateTimeFormat`, `WebMvcConfigurer#addFormatters` | JSON body, DB 컬럼 |
| DB 값 ↔ Entity 속성 | JPA `AttributeConverter` | 외부 API의 enum/날짜 표현 |

한 경계의 설정만으로 나머지 경계도 맞춰졌다고 간주하지 않는다. 예를 들어 DB의 `A`를 의미 있는 enum으로 매핑해도 JSON의 `"ACTIVE"`/`"A"` 선택은 별도 API 계약이다.

## Jackson 초기 설정

날짜·시각을 문자열로 사용한다면 요청과 응답의 형식을 함께 정하고 양방향으로 적용한다. 예를 들어 로컬 업무 시각 계약은 다음처럼 둘 수 있다. 이 예시를 무조건 강제하지 않는다.

| 타입 | 표현 예시 | 확인할 의미 |
| --- | --- | --- |
| `LocalDate` | `2026-01-02` | 날짜만 표현 |
| `LocalTime` | `09:30:00` | 초·소수초 허용 여부 |
| `LocalDateTime` | `2026-01-02 09:30:00` | 시간대가 없는 업무 시각. ISO의 `T` 형식과 구분 |
| `Instant`·`OffsetDateTime` | offset을 포함하는 ISO 형식 | 여러 시간대에서 동일 순간을 표현해야 할 때 선택 |

- Boot가 구성한 mapper를 확장하고, 주입받은 동일 설정의 mapper를 MVC와 보안 오류 writer에서 사용한다. 임의의 `new ObjectMapper()`로 Java time 등의 설정을 누락하지 않는다.
- Jackson 2에서는 `Jackson2ObjectMapperBuilderCustomizer`와 Java time serializer/deserializer를 사용할 수 있다. 모듈 목록 전체를 바꿔 Boot가 등록한 다른 모듈을 잃지 않도록 additive 등록 방식을 선택한다. Jackson 3에서는 그 버전의 mapper/customizer와 날짜 지원 API로 구현한다.
- `LocalDateTime`에 서버 시간대 설정만 적용해서 offset이 생겼다고 설명하지 않는다. 날짜 패턴의 년도·엄격한 파싱·윤년·소수초·null 정책을 함께 확인한다.
- 필드 이름은 `lowerCamelCase`, null 필드는 포함하는 계약을 기본 후보로 삼되 기존 호출 계약을 우선한다. test profile에서도 동일한 이름 규칙·null·날짜 정책을 적용한다. naming strategy 설정만으로 일부 `@JsonProperty`의 계약까지 동일해졌다고 가정하지 않는다.
- enum 표현, 미정의 enum 거부 여부와 알 수 없는 JSON 필드 허용 여부를 API 계약으로 정한다. 단순히 역직렬화 오류를 피하려고 미정의 값을 조용히 null로 바꾸지 않는다.
- 문자열 정제·특정 필드 변환은 필요한 필드/DTO 범위에 적용한다. 모든 문자열에 HTML 제거나 전역 다형 타입 허용 설정을 넣지 않는다.

## MVC query/path 변환

ISO 형식 또는 합의한 패턴을 `@DateTimeFormat`이나 공통 Formatter/Converter로 등록한다. JSON에서 공백을 쓰더라도 URL의 시각은 `2026-01-02T09:30:00`처럼 별도 계약으로 정할 수 있다.

`WebMvcConfigurer#addArgumentResolvers`의 리스트 앞에 넣었다는 사실만으로 내장 `@PathVariable` resolver보다 먼저 실행된다고 가정하지 않는다. 단순 날짜 변환에는 타입 변환 기능을 우선 사용한다. 별도 resolver가 필요하면 지원 대상과 실제 선택 우선순위를 HTTP 호출로 검증한다. 추가 설정만을 위해 `@EnableWebMvc`로 Boot MVC 자동 설정을 무심코 대체하지 않는다.

초기 계약 검증에는 정상 DTO의 JSON 왕복, 잘못된 날짜/enum/JSON의 400, query와 path 각각의 날짜 변환, null/빈 값, 예외 상세 메시지 전달을 포함한다. mapper 단위 테스트와 MVC 바인딩 테스트를 구분한다. 확장 지점의 설명은 [Spring MVC 타입 변환](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/conversion.html)에서도 확인할 수 있다.
