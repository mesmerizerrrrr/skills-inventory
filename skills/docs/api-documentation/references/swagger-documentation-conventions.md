# Swagger 문서 분리 관례

`eci-my247-api`에서 이상수가 반복 적용한 문서 구조를 보존한다. 이 구조가 이미 있는 프로젝트의 API 문서를 작성하거나, 사용자가 같은 구성을 선택한 경우에 적용한다. Swagger 자체의 일반 사용법이나 모든 프로젝트에 강제할 아키텍처 기준은 아니다.

## 문서 책임의 위치

| 위치 | 맡길 내용 |
| --- | --- |
| 도메인의 Controller | API 묶음의 `@Tag`, 해당 동작의 합성 Swagger 어노테이션, 직접 선언된 경로·쿼리 파라미터의 `@Parameter` |
| `<domain>/presentation/swagger/annotation(s)/<동작>Swagger` | `@Operation`의 요약·설명, 필요한 요청 본문 명세, 동작별 `@ApiResponses` |
| 요청·응답 DTO | 필드별 `@Schema`, 값의 의미·단위·조건·예시 |
| `<domain>/presentation/swagger/response(s)/<응답>Swagger` | 실제 응답을 감싼 `CommonResponse<T>`의 구체적인 문서 스키마 |
| 기존 공통 Swagger Controller·응답 클래스 | 공통 오류와 보안 요구의 문서, 데이터 없는 성공 응답 |

- 같은 도메인의 인접 파일에 맞춰 이름을 정한다. 원본에는 `annotation`/`annotations`, `response`/`responses`, 클래스 접미사가 혼재하므로 어느 한 표기를 전체 규칙으로 강제하지 않는다.
- 설명은 한글을 기본으로 쓰고, 영문 식별자는 실제 이름을 유지한다. 여러 줄의 업무 조건·예시는 기존처럼 Java text block에 작성할 수 있다. HTML 목록 사용 자체를 모든 설명의 필수 형식으로 만들지 않는다.
- 합성 어노테이션은 Controller의 해당 동작에 연결되어야 한다. 기존 선언의 적용 대상과 런타임 유지 설정을 함께 확인한다. 파일만 추가하고 사용하지 않는 상태를 문서화 완료로 보지 않는다.
- 공통 보안 요구와 오류를 이미 상속·조합하고 있다면 개별 동작에 불필요하게 복제하지 않는다. 문서용 어노테이션이 실제 인증·예외 처리를 구현한다고 설명하지 않는다.

## 공통 응답과 문서용 응답 클래스

이 관례에서 Controller는 실제 DTO, 컬렉션 또는 `void`를 반환하고, 공통 응답 처리는 기존 `CommonResponseAdvice`가 담당한다. 문서용 응답 클래스는 `CommonResponse<T>`를 구체화하여 Swagger에 최종 응답 구조를 알려준다. 실제 프로젝트의 공통 처리와 예외 경로를 확인한 뒤 이 관계를 적용한다.

1. Controller 반환형과 공통 응답 처리로 최종 응답 구조를 확인한다. 별도 응답을 직접 반환하거나 공통 처리를 거치지 않는 API라면 그 실제 동작을 따른다.
2. 해당 도메인의 문서용 응답 클래스에서 `T`를 실제 데이터 형태와 일치시킨다. 목록은 `List<Dto>`, 날짜별 묶음은 `Map<LocalDate, List<Dto>>`처럼 중첩 구조까지 대조한다.
3. 기존 방식대로 `getData()`에 데이터의 의미를 설명하고, 합성 어노테이션의 응답 `implementation`에서 이 문서용 클래스를 참조한다. 공통 코드·메시지 표현은 기존 공통 응답 정의를 재사용한다.
4. 데이터 없는 성공 응답이 실제로 공통 포장을 거친다면 기존 `CommonSwaggerResponses.EmptySuccess`를 재사용한다. `void` 선언만 보고 응답 본문이 없다고 문서화하지 않는다.
5. 목록·Map을 스키마 속성으로 덮어쓸 때는 실제 제네릭 구조를 잃지 않는지 확인한다. 값의 예시가 필요하더라도 다른 API의 응답 클래스를 임시로 연결하지 않는다.

다음은 기존 `CommonResponse`, `ResponseCode`, `ItemDto`가 있는 프로젝트에서 배치 방법만 보여주는 예다. 클래스명·성공 코드·null 표기는 대상 프로젝트의 정의에 맞춘다.

```java
public class ItemListResponseSwagger extends CommonResponse<List<ItemDto>> {

    public ItemListResponseSwagger() {
        super(ResponseCode.SUCCESS, null);
    }

    @Schema(description = "조회된 항목 목록")
    @Override
    public List<ItemDto> getData() {
        return super.getData();
    }
}
```

문서 작성만을 위해 Controller의 반환형이나 공통 응답 포장을 변경하지 않는다. 위 예제는 문서용 클래스의 형태이며 실행 응답 객체를 새로 생성하도록 요구하지 않는다.

## 반례와 완료 확인

- 원본의 `LeaderboardController`에는 분리된 어노테이션과 inline `@Operation`이 함께 있다. 분리를 선호하는 구조로 보존하되, 모든 inline 선언의 이동을 문서 작업의 선행 조건으로 삼지 않는다.
- 조사 시점 `release@8b06115`의 `PlanCardController.search`는 날짜별 Map을 반환하지만 `PlanCardSearchResponseSwagger`는 List를 선언한다. 이 파일 쌍은 완성된 템플릿으로 복제하지 않는다. 새 문서나 수정 대상은 현재 계약을 기준으로 작성한다.
- 공통 응답 클래스를 포함해 `schema.implementation` → 문서용 응답의 제네릭과 `getData()` → 실제 DTO/Controller 반환형 → 공통 응답 처리 순서로 맞는지 확인한다. 문서 생성·렌더링을 실행했다면 확인한 환경과 결과를 구분해 기록한다.
- 관련 없는 어노테이션 재배치, DTO 리팩터링, 런타임 응답 변경은 보강 범위에 넣지 않는다.

## 출처와 적용 한계

2026-10-16에 로컬 `eci-my247-api`의 전체 가용 브랜치에서 `이상수 <sangsoo.lee@etoos.com>`의 비병합 이력을 확인했다. 관련 Controller·Swagger·enum 이력 범위는 2025-11-24~2026-10-13이며, 아래 대표 커밋의 실제 diff와 현재 코드를 대조했다. 초기 커밋에 존재한다는 이유만으로 개인 관례로 채택하지 않았다. 동일 변경의 중복 커밋은 별도 반복 근거로 세지 않았다.

아래 경로는 모두 `eci-my247-api` 저장소 기준이다. 과거 커밋의 경로가 현재와 다를 수 있다.

| 커밋 / 작성일 | 보존 판단에 사용한 근거 |
| --- | --- |
| `4b4b3e1` / 2025-11-25 | `src/main/java/com/etoos/my247/commons/config/swagger/CommonSwaggerController.java`, `src/main/java/com/etoos/my247/commons/config/swagger/CommonSwaggerControllerSecured.java`, `src/main/java/com/etoos/my247/commons/config/swagger/responses/CommonSwaggerResponses.java`: 공통 오류·보안 문서와 빈 성공 응답을 직접 도입 |
| `5716ad5` / 2025-12-03 | `src/main/java/com/etoos/my247/plan_card/presentation/swagger/annotations/PlanCardSearchSwagger.java`, `src/main/java/com/etoos/my247/plan_card/presentation/swagger/response/PlanCardSearchResponseSwagger.java`: 동작별 합성 어노테이션과 문서용 응답 클래스 추가 |
| `ffbbb5e` / 2025-12-08 | `src/main/java/com/etoos/my247/plan_card/presentation/swagger/response/PlanCardSearchResponseSwagger.java`: 목록을 잘못 표시하던 명시적 스키마 속성 제거. 특정 라이브러리 해결책을 범용 규칙으로 확대하지 않음 |
| `a4e4c6d` / 2025-12-19 | `src/main/java/com/etoos/my247/subject/presentation/swagger/response/SubjectAreaSelectedColorResponseSwagger.java`: Map 응답에도 같은 구조 적용 |
| `dedbadf` / 2026-06-02 | `src/main/java/com/etoos/my247/leaderboard/presentation/LeaderboardController.java`, `src/main/java/com/etoos/my247/leaderboard/presentation/swagger/response/StudyTimeLeaderboardStatsSwagger.java`: 응답 클래스는 분리하면서 Operation은 inline으로 둔 반례 |
| `1643fca` / 2026-08-04 | `src/main/java/com/etoos/my247/banner/presentation/swagger/annotation/BannerListSwagger.java`, `src/main/java/com/etoos/my247/banner/presentation/swagger/response/BannerListResponseSwagger.java`: 후속 도메인에서도 같은 구조로 신규 작성 |

커밋은 배치 관례의 출처이며, 현재 API 동작이나 운영 응답이 모두 정확하다는 보증은 아니다. 재사용 시 대상 프로젝트의 현재 구조와 요청 범위를 우선한다.
