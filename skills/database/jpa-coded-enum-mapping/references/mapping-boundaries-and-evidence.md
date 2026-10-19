# 코드 매핑의 적용 판단과 근거

숫자·문자 코드의 성격이나 Converter의 공통 적용 범위가 불명확할 때만 읽는다.

## 적용 판단

| 확인한 저장 계약 | 판단 |
| --- | --- |
| 수강 상태를 DB 문자열 `"1"`로 저장하고 Java에서는 `ENROLLED`로 표현함 | 의미명과 저장 코드가 다르므로 코드 값을 가진 enum과 Converter 사용 |
| 단일 선택형 문항을 DB `"S"`로 저장하고 Java에서는 `RADIO_BTN`로 표현함 | 같은 방식으로 의미와 저장값 분리 |
| 랜딩 동작을 DB `"POPUP"`로 저장하고 Java enum명도 `POPUP`임 | 기존 `@Enumerated(EnumType.STRING)` 유지 |
| 기존 `ORDINAL`의 선언 순서와 DB 저장 계약이 명시적으로 일치함 | 이 스킬을 이유로 Converter로 전환하지 않고 기존 매핑 유지 |
| 컬럼이 숫자이지만 의미·자료형만 알려져 있고 코드표는 없음 | Converter 적용 여부를 아직 결정하지 않음. 실제 코드와 의미를 확인 |
| 여러 대상 유형을 하나의 숫자 비트마스크에 저장함 | 단일 enum 코드 매핑으로 다루지 않고 기존 비트마스크 모델 유지 |

앞의 세 행은 `eci-my247-api` 현재 소스에서 확인한 사례다. `"1"`, `"S"` 자체를 다른 도메인의 공통 코드로 사용하지 않는다. 날짜 문자열이나 특수 boolean 변환도 발견되었지만 이 스킬의 업무 코드 enum 적용 범위에는 포함하지 않았다.

## 공통화할 때 확인할 경계

- 기존 `DatabaseCodeConverter`는 `PersistableCodeEnum#getDbValue()`를 통해 변환한다. enum명·ordinal 대신 명시된 DB 값을 쓰는 선택을 재사용한다.
- 이 공통 Converter의 현재 미정의 값·예외 처리 방식은 null 반환이다. 다른 Converter에는 예외를 던지는 구현도 있다. 프로젝트 전체가 동일한 오류 정책을 가진다고 단정하지 않는다.
- `GroupScheduleWeekDayConverter`는 DB 요일 코드의 의미가 Java 요일 값과 다르다는 사실을 반영한다. 과거의 숫자 코드 추정이 수정된 사례이므로 실제 코드-의미를 확인하는 근거로만 사용한다. 해당 요일 체계나 `autoApply` 설정을 다른 프로젝트로 복제하지 않는다.
- 설문 대상 유형의 Converter는 후속 모델 변경으로 삭제되었다. 과거 커밋에 Converter가 있다는 이유로 현재 비트마스크 컬럼에 다시 도입하지 않는다.

## 출처

2026-10-16, `eci-my247-api`의 Converter 경로와 관련 Entity·enum에 대한 이상수 `<sangsoo.lee@etoos.com>`의 전기간 비병합 변경 이력, 주요 diff, 현재 코드를 대조했다. 다음 경로는 저장소 상대 경로다. 적용 조건은 같은 날짜 사용자가 지정한 **불투명 업무 코드이며 ORDINAL·STRING으로 의미와 저장값을 그대로 표현할 수 없는 경우**로 한정했다.

| 커밋·날짜 | 대표 경로 | 확인한 선택 |
| --- | --- | --- |
| `92f5858` · 2025-11-24 | `src/main/java/com/etoos/my247/commons/infrastructure/db/converter/DatabaseCodeConverter.java` | initial commit부터 공통 구조 존재. 독자 창안의 근거로 사용하지 않음 |
| `c2ff78d` · 2026-01-21 | `src/main/java/com/etoos/my247/group/application/enums/GroupRegistrationState.java`, `src/main/java/com/etoos/my247/group/infrastructure/converter/GroupRegistrationStateConverter.java` | `ENROLLED`와 DB 문자열 `"1"` 분리 |
| `8a93475` · 2026-01-21 | `src/main/java/com/etoos/my247/counsel/application/enums/CounselTimeType.java`, `src/main/java/com/etoos/my247/counsel/infrastructure/converter/CounselTimeTypeConverter.java` | 시간대 의미와 `"001"` 등 저장 코드 분리 |
| `7130033` · 2026-04-07, `3eae3d1` · 2026-04-09 | `src/main/java/com/etoos/my247/survey/application/enums/SurveyQuestionType.java`, `src/main/java/com/etoos/my247/survey/infrastructure/converter/SurveyAnswerTypeConverter.java` | 문항·답변 유형에서 같은 공통 Converter 재사용 |
| `1643fca` · 2026-08-04 | `src/main/java/com/etoos/my247/banner/application/domain/BannerEntity.java` | 의미명과 저장값이 같은 enum은 STRING 매핑 |
| `5e36a60` · 2026-08-12 | `src/main/java/com/etoos/my247/survey/infrastructure/converter/SurveyTargetTypeConverter.java` | 비트마스크 모델 전환으로 삭제된 과거 경로 |
| `4cefe49` · 2026-10-07 | `src/main/java/com/etoos/my247/group/infrastructure/converter/GroupScheduleWeekDayConverter.java` | 실제 DB 요일 의미에 맞게 기존 매핑 수정 |

현재 소스의 코드표와 역사적 변경을 확인한 기록이며, 운영 DB의 모든 저장값을 조사한 기록은 아니다.
