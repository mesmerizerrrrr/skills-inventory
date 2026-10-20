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

타입 JavaDoc에는 업무 개념과 상수 목록을 두어 가능한 값을 함께 파악하게 하고, 각 상수에는 해당 값의 의미와 적용 조건을 둔다. 다음은 JavaDoc과 API 문서화를 함께 요청받았고 기존에 Swagger를 사용하는 경우의 가상 예다. JavaDoc만 작성할 때는 JavaDoc 부분만 적용한다.

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

    /**
     * 실행 대기
     */
    @Schema(description = "실행 대기")
    WAITING,

    /**
     * 실행 중
     */
    @Schema(description = "실행 중")
    RUNNING
}
```

상수별 조건이 있으면 목록과 상수 설명, API 문서에서 의미가 어긋나지 않도록 맞춘다. 설명이 같다는 이유로 enum의 모든 사용 DTO에 같은 문구를 복제하지 않는다. 기존 Schema 문구와 구현이 다르면 요청된 문서 범위에서 차이를 확인하고, enum 값·직렬화·매핑 자체는 주석 작업으로 변경하지 않는다.

### 적용 범위

기존 프로젝트가 타입 요약과 상수별 설명만 두는 간단한 enum 서식을 사용하면 그 규약을 따른다. 위 예시를 이유로 모든 기존 enum에 일괄 주석을 추가하거나 Swagger를 도입하지 않는다. `@param`의 타입 표기 뒤에는 인자의 실제 의미를 설명하며 타입명만 적고 끝내지 않는다. 확인되지 않은 작성자·버전·시각을 자동으로 넣지 않는다.

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
 * {@link Math}의 정확한 곱셈 연산으로 분 단위의 시간을 초 단위로 변환한다.
 *
 * @param minutes {@code int} 변환할 분 단위 시간. 0 이상이어야 한다.
 * @return {@code int} 초 단위로 변환한 시간
 * @throws IllegalArgumentException {@code minutes}가 음수인 경우
 * @throws ArithmeticException 변환 결과가 {@code int} 범위를 초과하는 경우
 */
public int toSeconds(int minutes) {
    if (minutes < 0) {
        throw new IllegalArgumentException("minutes must be non-negative");
    }
    return Math.multiplyExact(minutes, 60);
}
```

예시의 입력 단위·범위·실패 조건과 태그 종류는 실제 구현에 맞춰 선택한다. 다중행 주석, 본문과 첫 블록 태그 사이 빈 ` *` 줄, 매개변수·반환 타입 표기와 심볼 링크는 공통 기본 서식으로 유지한다.

## 매개변수 타입 예시

`@param` 뒤의 매개변수명은 선언 그대로 두고, 그 다음에 실제 선언 타입의 링크·코드 표기와 설명을 작성한다. 생성자 인자와 record 구성요소도 같은 규칙을 적용한다.

| 선언된 매개변수 | JavaDoc 소스의 매개변수 태그 |
| --- | --- |
| `RequestDto request` | `@param request {@link RequestDto} 생성에 사용할 요청값` |
| `int count` | `@param count {@code int} 가져올 최대 건수. 1 이상` |
| `Long userId` | `@param userId {@link Long} 조회할 사용자 식별자` |
| `List<AppPushHistEntityId> ids` | `@param ids {@link List}&lt;{@link AppPushHistEntityId}&gt; 조회할 푸시 이력 식별자 목록` |
| `Map<String, List<DtoClass>> groups` | `@param groups {@link Map}&lt;{@link String}, {@link List}&lt;{@link DtoClass}&gt;&gt; 코드별 처리 대상 목록` |
| `DtoClass[] items` | `@param items {@link DtoClass}[] 처리할 상세 정보 배열` |
| `T value` | `@param value {@code T} 전달할 값` |
| 타입 매개변수 `<T extends DtoClass>` | `@param <T> {@code T} {@link DtoClass}를 상속하는 처리 결과 타입` |

배열·와일드카드 등의 타입 구성은 아래 반환 타입 예시와 동일하다. `@param {@link request}` 또는 `@param {@link T}`처럼 태그가 요구하는 이름 자리를 링크로 바꾸지 않는다.

## 반환 타입 예시

아래 타입과 메서드는 표기 방법을 보여 주는 가상 예다. 실제 코드에서는 선언된 반환 타입·타입 인수를 사용하고, 링크 대상이 현재 패키지 또는 import 등으로 해석되는지 확인한다.

| 선언된 반환 타입 | JavaDoc 소스의 반환 태그 |
| --- | --- |
| `DtoClass` | `@return {@link DtoClass} 조회한 상세 정보` |
| `int` | `@return {@code int} 조건에 맞는 전체 건수` |
| `Integer` | `@return {@link Integer} 집계된 건수. 집계값이 없으면 null` |
| `List<AppPushHistEntityId>` | `@return {@link List}&lt;{@link AppPushHistEntityId}&gt; 조회한 푸시 이력 식별자 목록. 없으면 빈 목록` |
| `Map<String, List<DtoClass>>` | `@return {@link Map}&lt;{@link String}, {@link List}&lt;{@link DtoClass}&gt;&gt; 코드별 상세 정보 목록` |
| `DtoClass[]` | `@return {@link DtoClass}[] 조회한 상세 정보 배열` |
| `int[]` | `@return {@code int}[] 항목별 집계 건수 배열` |
| `T` | `@return {@code T} 전달받은 값` |
| `List<? extends DtoClass>` | `@return {@link List}&lt;{@code ? extends} {@link DtoClass}&gt; 조회한 상세 정보 목록` |

제네릭의 `&lt;`·`&gt;`는 생성 문서에서 `<`·`>`로 표시되며 각 `{@link ...}`는 별도의 타입 링크로 유지된다. 클래스가 아닌 타입 변수·와일드카드를 실제 클래스처럼 링크하지 않는다.

```java
/**
 * 요청 조건에 맞는 푸시 이력 식별자를 조회한다.
 *
 * @param userId {@link Long} 조회할 사용자 식별자
 * @return {@link List}&lt;{@link AppPushHistEntityId}&gt; 푸시 이력 식별자 목록. 없으면 빈 목록
 */
public List<AppPushHistEntityId> findIds(Long userId) {
    // 가상 예시에서는 조회 결과가 없다고 가정한다.
    return List.of();
}
```

## 본문과 메서드 링크 예시

아래 예시는 `java.util.List`를 import한 클래스 안의 메서드다. 본문의 메서드 언급은 실제 선언으로 연결하고, `@param`·`@return`에는 각각 선언 타입과 의미를 적는다. `@throws`의 예외명과 `@see`의 대상은 블록 태그 고유 문법을 유지한다.

```java
/**
 * {@link List#copyOf(java.util.Collection)}로 이름 목록의 변경 불가능한 사본을 만든다.
 * 원본 목록의 항목을 추가하거나 제거해도 반환 목록에는 반영되지 않는다.
 *
 * @param names {@link List}&lt;{@link String}&gt; 복사할 이름 목록. null 목록이나 원소는 허용하지 않는다.
 * @return {@link List}&lt;{@link String}&gt; 입력 순서를 유지하는 변경 불가능한 이름 목록
 * @throws NullPointerException {@code names} 또는 목록의 원소가 null인 경우
 * @see List#copyOf(java.util.Collection)
 */
public List<String> copyNames(final List<String> names) {
    return List.copyOf(names);
}
```

현재 클래스의 메서드는 `{@link #copyNames(List)}`, 특정 필드나 상수는 `{@link Integer#MAX_VALUE}`처럼 연결한다. 링크 대상 메서드의 인자 목록에는 실제 선언 타입을 쓰고, 오버로드를 구분할 수 있는지 확인한다. 매개변수인 `names` 자체를 언급할 때는 `{@code names}`를 사용한다.
