# 보안 초기 설정

## 인증 방식과 경로부터 결정

인증이 필요한 요청인지, 누구의 자격을 검증할지 먼저 정한다. 다른 서버의 API key 인증, 사용자의 bearer token, 브라우저 세션을 하나의 의미로 취급하지 않는다.

| API 유형 | 초기 구성 |
| --- | --- |
| 공개 API | 합의한 method/path를 명시적으로 허용한다. 별도 인증 기능을 발명하지 않는다. |
| 사용자 bearer token API | 실제 토큰 검증 방식·issuer/audience 또는 외부 검증 API·principal·권한을 정한다. 지원되는 경우 표준 Resource Server 구성을 우선한다. |
| 세션/쿠키 인증 API | 세션 정책·로그인 흐름·CSRF 토큰 전달과 쿠키 정책을 함께 구성한다. |
| 서버 간 API | API key 또는 서명 프로토콜과 허용 경로·호출자 권한을 연결한다. 사용자 토큰을 발급하는 기능까지 자동으로 만들지 않는다. |

인증 제공자·키 형식이 미정이면 해당 계약을 확인한다. 임시 필터가 모든 요청을 인증 성공으로 처리하게 하거나 전체 경로를 공개해서 초기 생성 완료로 만들지 않는다. 테스트에 필요한 mock 인증은 테스트 범위에 둔다.

## SecurityFilterChain과 실패 응답

- 단일 정책이면 한 체인에서 명시적 공개 경로와 나머지 인증/인가 규칙을 구성한다. 서로 다른 인증 방식의 API 영역이 있으면 `securityMatcher`와 `@Order`로 체인을 분리할 수 있다.
- 여러 체인은 첫 매칭 체인만 적용된다는 전제로 순서와 matcher를 정한다. 마지막에는 전체 경로를 포괄하는 정책을 두어 미매칭 요청이 보안 밖으로 빠지지 않게 한다.
- permit list와 인증 제외 경로의 기본값은 비어 있게 하거나 필요한 공개 경로만 둔다. 누락값을 `/**`로 대체하지 않는다. `permitAll`과 security filter 자체 제외를 구별한다.
- bearer/API key만 사용하는 세션 없는 API는 `SessionCreationPolicy.STATELESS`를 명시한다. form login·HTTP Basic은 선택한 인증 모델에 없는 경우에만 끈다.
- 필터 인증 실패는 `AuthenticationEntryPoint` 또는 해당 필터의 실패 처리로, 인가 실패는 `AccessDeniedHandler`로 공통 JSON을 반환한다. MVC `@RestControllerAdvice`가 필터 예외까지 자동 처리한다고 가정하지 않는다.
- 일반 인증 누락·실패의 401과 권한 부족의 403을 구분한다. CSRF 검증 실패는 익명 요청에서도 403으로 처리될 수 있으므로 인증 실패로 일괄 변환하지 않는다. 공통 mapper·응답 DTO·UTF-8 JSON content type을 사용하고, 이미 응답을 쓴 뒤 체인을 계속 진행하지 않는다.
- 커스텀 필터는 필요한 검증 위치에 한 번만 등록한다. Servlet filter 자동 등록과 Security chain 등록이 겹쳐 두 번 실행되지 않는지 확인한다. 경로는 context path를 포함한 실제 matcher 동작으로 확인한다.

Security가 먼저 거부한 요청은 MVC의 404·405 처리까지 도달하지 않을 수 있다. 공개 전용 API도 미등록 경로·허용하지 않은 method·ERROR dispatch의 최종 응답을 정하고 확인한다. MVC에 도달한 오류의 상태를 보존하는 정책과 구분한다.

체인 선택의 설명은 [Spring Security Java 구성](https://docs.spring.io/spring-security/reference/servlet/configuration/java.html)에 있으며, 구현에는 선택한 Security 버전의 API를 사용한다.

## CORS·CSRF

CORS는 환경별 허용 origin·method·header·credentials를 명시하고 preflight가 인증 필터에서 막히지 않게 연결한다. MVC와 Security에 서로 다른 허용 정책을 중복 선언하지 않는다. credentials를 허용하면서 모든 origin을 허용하는 구성을 기본값으로 만들지 않는다.

CSRF 비활성화는 “REST API” 또는 “STATELESS”라는 이름만으로 결정하지 않는다. 브라우저가 세션/인증 쿠키 등 자격증명을 자동 전송하면 보호가 필요하다. 자동 전송되는 자격증명이 없고 명시적 Authorization 헤더 등으로만 인증하는 API 영역은 그 조건을 확인한 뒤 해당 범위에서 비활성화할 수 있다. 혼합 서비스에서는 체인별로 판단한다. [Spring Security CSRF](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html)의 기본 동작은 unsafe method에 대한 CSRF 보호다.

## 선택 구성

- **API key**: 키를 외부 설정으로 주입하고 어떤 호출자와 권한인지 연결한다. 단순 shared secret 비교를 요청 본문 무결성이나 재전송 방지로 설명하지 않는다.
- **HMAC 서명**: 연동 명세가 있을 때만 구현한다. 알고리즘·canonical request·검증 시각 범위·재전송 방지 계약을 먼저 정한다. timestamp만 서명한 예시를 완성된 요청 무결성 검증으로 복사하지 않는다. 프로토콜이 미정이면 키/서명/nonce 규칙을 임의로 만들어 상대 시스템과 연동됐다고 주장하지 않는다.
- **JWT**: 검증 API를 호출하는 서비스인지 자체 서명 검증인지 구분한다. 검증 서비스에 발급용 비밀키·refresh token 저장소를 자동으로 추가하지 않는다. 만료·issuer/audience·서명 등 계약에서 필요한 검증을 연결한다.
- **HTML/XSS 정제**: HTML 입력이 허용되는 필드에만 정책을 정해 적용한다. 전역 String 정제는 비밀번호·서명 원문·일반 텍스트를 바꿀 수 있다. `@InitBinder`가 JSON body를 모두 정제한다고 가정하지 않는다.
- **OpenAPI/health**: 공개 여부와 상세 정보 노출을 환경별로 정한다. 문서 페이지를 열기 위해 전체 API를 공개하지 않는다.

최소 검증은 공개 경로, 보호 경로의 무자격·잘못된 자격·권한 부족·정상 자격, CORS preflight다. 여러 체인이면 각 경로와 미등록 경로도 검증하고, 쿠키 인증이면 CSRF 누락/유효 요청도 확인한다. 외부 검증 서버를 대체한 테스트와 실제 인증 연동 확인을 구분해 보고한다.
