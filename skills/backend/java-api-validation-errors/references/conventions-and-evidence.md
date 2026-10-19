# 검증·예외 관례의 근거

## 조사 기준

- 저장소: `eci-my247-api`, 기준 커밋 `8b06115e9bb52f3ee75d28622d430b83e2a7dc92` (`release`).
- 작성자: `이상수 <sangsoo.lee@etoos.com>`; 조사일: 2026-10-16.
- 2025-11-24~2026-10-15 비병합 이력의 변경 경로를 분류하고, 예외·검증·Advice·응답 코드 관련 42개 커밋의 변경 목록에서 도입·수정·원복을 구분했다. 아래 주요 diff와 현재 DTO·Controller·처리기를 대조했다. 모든 업무 실패나 운영 응답을 실행 검증한 결과는 아니다.
- 아래 소스 경로는 저장소의 `src/main/java/com/etoos/my247/`를 기준으로 한다. 원본 저장소가 없어도 진입문서의 지침은 사용할 수 있다.

## 보존한 선택

| 커밋·작성일 | 확인한 변경 | 대표 소스 |
| --- | --- | --- |
| `c3e463f` · 2026-01-12 | `BaseException`에 상세 메시지를 추가하고 Advice가 이를 사용하도록 보강. 요청 DTO의 제약에 한글 메시지와 복합 검증을 추가 | `commons/application/exceptions/BaseException.java`, `commons/presentation/advice/CommonExceptionAdvisor.java`, `plan_card/presentation/dto/request/PlanCardCreateRequest.java` |
| `f47cced` · 2026-01-31 | 금칙어 발견 시 일반 `Exception`과 문자열 메시지 대신 `ProhibitWordException` 및 전용 응답 코드로 표현 | `prohibit_word/application/exceptions/ProhibitWordException.java` |
| `62bfadf` · 2026-02-22 | 기존 `RuntimeException`인 예약 중복 예외를 `BaseException`과 `ALREADY_RESERVED_QUEST_SLOT`에 연결 | `quest/application/exception/QuestAlreadyReservedException.java` |
| `6ece094` · 2026-04-14 | 다른 도메인에서도 요청 DTO의 `@Hidden`·`@AssertTrue` 조합으로 허용 유형 검사 | `immediately_plan/presentation/dto/request/CreateImdPlanCardDetrmnRequest.java` |
| `653c532` · 2026-05-12 | 일정 이름 DTO의 `@NotBlank`, `@Size`와 한글 메시지, `@Schema.maxLength`를 함께 보강 | `settings/presentation/dto/request/ExamScheduleModifyRequest.java` |
| `d93707b` · 2026-07-27 | 푸시 요청 제약·문서 최대 길이를 함께 추가하고 App/Internal Controller 양쪽에 `@Valid` 연결 | `push/presentation/dto/request/PushSendRequest.java`, `push/presentation/InternalPushController.java` |

파일 검증은 `e1518be`(2026-02-07) 이미지 검사 추가 후 `de78486`(2026-02-10)에서 크기 검사를 별도 제약으로 분리했다. `55cf3f7`(2026-06-04)은 확장자 검증기를 추가했다. 특정 허용 확장자·용량은 업무 설정이므로 이 스킬에 고정하지 않는다.

## 일반 규칙으로 확대하지 않은 부분

- 공통 `BaseException`·`NotFoundException`의 뼈대는 `92f5858` 초기 커밋에 이미 있다. 이후 직접 보강하고 여러 업무에서 채택한 관례이며 독자적으로 처음 고안했다는 근거는 아니다.
- `exception`과 `exceptions` 폴더명이 혼용되고, 예외 접미사도 일부 다르다. 해당 도메인에 맞추며 일괄 이름 변경을 요구하지 않는다.
- 여러 업무 코드가 HTTP 422를 사용하지만 모든 업무 실패를 422로 반환하라는 규칙은 아니다. 코드 번호·메시지·HTTP 상태는 현재 API 계약을 확인한다.
- 모든 조건에 새 예외 클래스를 만드는 방식은 아니다. `InvalidArgumentException`과 상세 메시지를 사용하는 경우도 있다.
- `f70bd9c`(작성일 2026-07-02, 커밋일 2026-07-24)는 여러 `IllegalArgumentException`을 공통 예외로 바꿨다. 이를 이유로 라이브러리·DB 변환 오류까지 무조건 요청 오류로 치환하는 규칙은 만들지 않는다.
- 요청 형식 오류에서 원인 메시지를 그대로 노출하거나 복합 검증에서 누락값 처리가 빠진 현재 예제를 그대로 복제하지 않는다. 보존 대상은 배치·표현 선택이다.
- iframe 응답용 Advice 우회는 추가와 원복이 반복되었다. 삭제된 `SkipCommonResponse`를 현재 공통 방식으로 소개하지 않는다.
