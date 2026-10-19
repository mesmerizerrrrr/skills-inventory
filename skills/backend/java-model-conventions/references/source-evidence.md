# 근거와 예외

확인일은 2026-10-16, 원본 저장소는 `eci-my247-api`, 현재 소스 기준은 `8b06115`이다. 아래 Java 경로는 저장소 루트의 `src/main/java/com/etoos/my247/`를 생략했다. 이 자료와 자산은 스킬 안에 보존되어 원본 저장소 접근 없이 사용할 수 있다.

2025-11-24~2026-10-15의 `sangsoo.lee@etoos.com` 비병합 이력 전체에서 모델·서비스·진입점 관련 파일 변경을 분류하고, 신규 모델과 후속 변경의 diff를 현재 코드와 비교했다. 표는 재사용할 선택을 뒷받침하는 소수의 근거이며, 모든 커밋의 규칙을 수록하지 않는다.

| 선택 | 커밋·날짜 | 원본 경로 | 귀속과 보존 범위 |
| --- | --- | --- | --- |
| Entity 정적 생성과 의도별 변경 | `962ad13` · 2025-11-27 | `plan_card/application/domain/PlanCardEntity.java` | 이상수 신규 추가. `ofCreateRequest`, `update` 형태를 현재도 유지 |
| 별도 업무에서도 같은 Entity 방식 | `7130033` · 2026-04-07 / `3eae3d1` · 2026-04-09 | `survey/application/domain/SurveyParticipationEntity.java` | 이상수 Entity 신규 추가 후 `ofSurveyStart`, `sectionSubmitted`, `complete` 추가 |
| DTO 소유 변환 | `208988c` · 2026-08-03 | `menu/presentation/dto/response/MenuDto.java`, `menu/application/service/impl/MenuServiceImpl.java` | 이상수 신규 작성. 서비스의 조회·정렬과 DTO의 `ofEntity` 변환 분리 |
| record 응답과 변환 생성자 | `1643fca` · 2026-08-04 | `banner/presentation/dto/BannerDto.java` | 이상수 신규 작성. 여러 원천 값을 응답 필드로 변환하는 생성자. 쿼리 투영 세부는 이 스킬의 규칙에서 제외 |
| record 응답, JSpecify 값 표기 | `450b5de` · 2026-07-27 | `push/presentation/dto/response/AppPushHistoryResponse.java` | 이상수 신규 추가. `org.jspecify.annotations.NonNull/Nullable` 사용 |
| mutable 요청과 불변 응답의 병존 | `7130033` · 2026-04-07 / `3eae3d1` · 2026-04-09 | `survey/presentation/dto/request/SurveyAnswerInputInfo.java`, `survey/presentation/dto/response/SurveyProgressResponseDto.java` | 이상수가 class 요청과 record 응답을 각각 작성. 모든 요청/응답의 타입을 고정하는 규칙은 아님 |
| final 매개변수 및 NonNull 표기 | `962ad13` · 2025-11-27 / `208988c` · 2026-08-03 | `plan_card/application/domain/PlanCardEntity.java`, `menu/presentation/dto/response/MenuDto.java` | 이상수 작성부에서 반복 확인. final이 없는 인자도 있어 일괄 강제 대신 선호로 보존 |
| IDE 포맷터 자산 | `92f5858` · 2025-11-24 | `extra/ETOOS_CODESTYLE.xml` | initial commit으로 반입. 후속 개인 관례와 구분해 원본 보존 |

## 후속 변경과 반례

- 학사일정 Entity의 기본 생성·변경 메서드는 `5265dbe`(2026-05-19, `de5ember@etoos.com`)에 속한다. 이상수의 `55cf3f7`(2026-06-04)은 그 방식의 파일 관계 처리 보강이다. 사용자 단독 신규 설계의 근거로 사용하지 않았다.
- `PlanCardEntity`는 특정 관계 목록에 `@Setter`가 있고, `PlanCardListDto` 및 `StudyHistoryStatisticsDto`는 class다. setter 금지·record 강제 규칙을 만들지 않았다.
- `PlanCardEntity.ofCreateRequest`는 요청 DTO를 직접 받고 `AcademicScheduleEntity.create`는 필드와 관계를 따로 받는다. 특정 팩토리 서명이나 DTO 독립성을 강제하지 않는다.
- `c0e449e`(2026-04-27)는 상담 응답의 불필요한 `@Builder` 사용을 정리했다. 이를 모든 Builder 사용 금지로 해석하지 않는다.
- `f3a1af9`(2025-12-19)의 DTO 직렬화 이름 수정은 호출 계약 확인의 근거다. 해당 필드명이나 당시 오류를 새 모델의 영구 명명 규칙으로 보존하지 않는다.
