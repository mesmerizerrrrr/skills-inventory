# 유형·레이어별 JavaDoc 기준

작성할 대상에 해당하는 절만 읽는다. 모든 항목을 주석의 고정 목차로 사용하지 않는다. 설명할 사실이 확인되지 않거나 해당하지 않으면 생략한다.

## 유형별 기준

| 대상 | 설명할 내용 | 피할 내용 |
| --- | --- | --- |
| `class` | 맡은 역할, 주요 협력 객체와의 관계, 확인된 사용 제약 | 필드와 메서드의 단순 나열, 이름만 보고 추정한 책임 |
| `interface` | 구현체와 호출자가 공유하는 계약, 입력·결과의 의미 | 특정 구현체의 동작을 모든 구현체의 보장으로 표현 |
| `enum` | 값이 나타내는 업무 개념, 필요한 상수별 의미, 외부 코드와의 확인된 매핑 | 이름이나 순서만 보고 추측한 DB 저장값·상태 전이 |
| 생성자 | 객체 생성에 필요한 조건과 인자의 의미 | 반환값 태그, 존재하지 않는 기본값 |
| 메서드 | 수행 결과, 입력 조건, 부작용, 반환값과 예외의 의미 | 구현을 줄 단위로 번역한 설명 |
| 필드 | 단위·포맷·값의 의미 등 선언만으로 알기 어려운 계약 | 타입과 이름을 그대로 반복한 문장 |

인터페이스나 부모 메서드에 이미 충분한 계약이 있으면 중복 설명을 줄인다. 자식 구현의 차이를 설명할 때는 상위 계약과 모순되지 않는지 확인한다.

## enum 문서화 서식

이 서식은 `eci-my247-api`에서 이상수가 작성한 enum의 문서 배치를 보존한다. 타입 JavaDoc에는 업무 개념과 상수 목록을, 상수에는 해당 값의 의미를 둔다. 다음은 JavaDoc과 API 문서화를 함께 요청받았고 기존에 Swagger를 사용하는 경우의 가상 예다. JavaDoc만 작성할 때는 JavaDoc 부분만 적용한다.

```java
/**
 * 작업 진행 상태
 * <ul>
 *     <li>{@link #WAITING}: 실행 대기</li>
 *     <li>{@link #RUNNING}: 실행 중</li>
 * </ul>
 */
@Schema(description = """
    작업 진행 상태
    <ul>
        <li>WAITING: 실행 대기</li>
        <li>RUNNING: 실행 중</li>
    </ul>
    """)
public enum WorkState {

    /** 실행 대기 */
    @Schema(description = "실행 대기")
    WAITING,

    /** 실행 중 */
    @Schema(description = "실행 중")
    RUNNING
}
```

상수별 조건이 있으면 목록과 상수 설명, API 문서에서 의미가 어긋나지 않도록 맞춘다. 설명이 같다는 이유로 enum의 모든 사용 DTO에 같은 문구를 복제하지 않는다. 기존 Schema 문구와 구현이 다르면 요청된 문서 범위에서 차이를 확인하고, enum 값·직렬화·매핑 자체는 주석 작업으로 변경하지 않는다.

### 출처와 적용 한계

2026-10-16에 `eci-my247-api`의 전체 가용 브랜치에서 `이상수 <sangsoo.lee@etoos.com>`의 비병합 enum 이력(2025-11-24~2026-10-13)을 확인하고, 아래 신규 작성 diff와 현재 소스를 대조했다. 경로는 원본 저장소 기준이다.

| 커밋 / 작성일 | 근거 |
| --- | --- |
| `faa8148` / 2026-01-12 | `src/main/java/com/etoos/my247/plan_card/application/enums/PlanCardProgressState.java`: 타입 JavaDoc의 상수 링크 목록, 상수별 한글 설명, Schema 병기 |
| `9e71a16` / 2026-01-12 | `src/main/java/com/etoos/my247/study_history/application/enums/StudyTimerType.java`: 같은 서식을 새 enum에 적용하고 상수에 업무 적용 조건 명시 |

모든 enum이 이 전체 서식을 사용하는 것은 아니다. 예를 들어 `1643fca`(2026-08-04)의 `src/main/java/com/etoos/my247/banner/application/enums/BannerActionType.java`는 더 간단한 형태다. 보존하는 것은 사용자가 선택한 문서화 서식이며, 모든 기존 enum에 일괄 주석을 추가하거나 Swagger 도입을 요구하는 규칙은 아니다. `@param`에 타입명만 반복하거나 작성자·시각을 자동 생성하는 관례는 이 보강에 포함하지 않는다.

## 레이어별 기준

레이어 이름은 탐색의 단서다. 실제 코드에서 확인한 책임을 기준으로 설명하며, 아래 표를 프로젝트의 설계 규칙으로 강제하지 않는다.

| 레이어 또는 역할 | 확인하고 설명할 사항 |
| --- | --- |
| Controller / API 진입점 | 처리하는 요청의 목적, 인증·인가나 검증이 수행되는 위치, 서비스 위임 결과. 상세 HTTP 명세를 JavaDoc에 전부 복제할 필요는 없다. |
| Service / 업무 처리 | 업무 조건과 상태 변화, 실제 저장·외부 호출 등 부작용. 트랜잭션 경계가 중요하면 설정과 호출 방식을 확인한 뒤 설명한다. |
| Repository / DAO | 조회인지 변경인지, 핵심 검색 조건, 정렬·페이징·빈 결과의 의미. 조회 결과를 DTO에 매핑하는 것만으로 DB 변경이라고 쓰지 않는다. |
| Entity / 도메인 모델 | 업무 개념, 주요 상태·관계·제약. DB 매핑은 어노테이션·컨버터·스키마 등 확인한 근거로 설명한다. |
| DTO / 요청·응답 모델 | 값의 의미, 단위·포맷, 확인된 필수·선택 조건. 선언과 실제 검증의 차이가 있으면 구별한다. |
| 유틸리티 / 공통 처리 | 변환 규칙, 입력 경계, 실패 시 동작. 불변성이나 스레드 안전성을 근거 없이 보장하지 않는다. |

## 짧은 예시

다음은 작성 방식만 보여주는 가상 예시다. 실제 대상 코드의 계약을 대신하지 않는다.

```java
/**
 * 분 단위의 시간을 초 단위로 변환한다.
 *
 * @param minutes 변환할 분 단위 시간. 0 이상이어야 한다.
 * @return 초 단위로 변환한 시간
 * @throws IllegalArgumentException minutes가 음수인 경우
 * @throws ArithmeticException 변환 결과가 int 범위를 초과하는 경우
 */
public int toSeconds(int minutes) {
    if (minutes < 0) {
        throw new IllegalArgumentException("minutes must be non-negative");
    }
    return Math.multiplyExact(minutes, 60);
}
```

예시의 핵심은 입력 단위·범위와 실패 조건을 구현에 맞게 설명하는 것이다. 이 형식을 모든 메서드에 기계적으로 복사하지 않는다.
