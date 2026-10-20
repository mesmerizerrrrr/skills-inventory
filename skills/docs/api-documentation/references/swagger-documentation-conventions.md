# Swagger 문서 분리 관례

도메인별 합성 Swagger 어노테이션과 문서용 응답 클래스를 사용하는 프로젝트의 API 문서를 작성하거나, 사용자가 그 구성을 선택한 경우에 적용한다. 동작별 명세와 필드 설명의 위치를 구분하고, 실제 응답 구조와 문서 스키마가 일치하도록 관리한다.

## 문서 책임의 위치

| 위치 | 맡길 내용 |
| --- | --- |
| 도메인의 Controller | API 묶음의 `@Tag`, 해당 동작의 합성 Swagger 어노테이션, 직접 선언된 경로·쿼리 파라미터의 `@Parameter` |
| `<domain>/presentation/swagger/annotation(s)/<동작>Swagger` | `@Operation`의 요약·설명, 필요한 요청 본문 명세, 동작별 `@ApiResponses` |
| 요청·응답 DTO | 필드별 `@Schema`, 값의 의미·단위·조건·예시 |
| `<domain>/presentation/swagger/response(s)/<응답>Swagger` | 실제 응답을 감싼 `CommonResponse<T>`의 구체적인 문서 스키마 |
| 기존 공통 Swagger Controller·응답 클래스 | 공통 오류와 보안 요구의 문서, 데이터 없는 성공 응답 |

- 같은 도메인의 인접 파일에 맞춰 이름을 정한다. `annotation`/`annotations`, `response`/`responses`의 단복수와 클래스 접미사는 기존 패키지의 표기를 따른다. 문서 작성만을 위해 전체 이름을 통일하지 않는다.
- 설명은 한글을 기본으로 쓰고, 영문 식별자는 실제 이름을 유지한다. 여러 줄의 업무 조건·예시는 기존처럼 Java text block에 작성할 수 있다. HTML 목록 사용 자체를 모든 설명의 필수 형식으로 만들지 않는다.
- 합성 어노테이션은 Controller의 해당 동작에 연결되어야 한다. 기존 선언의 적용 대상과 런타임 유지 설정을 함께 확인한다. 파일만 추가하고 사용하지 않는 상태를 문서화 완료로 보지 않는다.
- 공통 보안 요구와 오류를 이미 상속·조합하고 있다면 개별 동작에 불필요하게 복제하지 않는다. 문서용 어노테이션이 실제 인증·예외 처리를 구현한다고 설명하지 않는다.

## 공통 응답과 문서용 응답 클래스

Controller가 실제 DTO, 컬렉션 또는 `void`를 반환하고 `CommonResponseAdvice` 같은 공통 처리기가 응답을 감싸는 구조에서는, 문서용 응답 클래스가 `CommonResponse<T>`를 구체화하여 Swagger에 최종 응답 구조를 알려준다. Controller 선언과 실제 응답이 다를 수 있으므로 공통 처리의 적용 조건과 예외 경로를 함께 확인한다. 클래스명은 대상 프로젝트의 정의를 따른다.

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

## 예외와 완료 확인

- 합성 어노테이션과 inline `@Operation`이 함께 있는 프로젝트에서는 인접한 문서 배치와 요청 범위를 따른다. 모든 inline 선언을 옮기는 것을 문서 작업의 선행 조건으로 삼지 않는다.
- 예를 들어 `ItemController.search`의 실제 데이터가 `Map<LocalDate, List<ItemDto>>`인데 문서용 응답 클래스가 `List<ItemDto>`를 선언하면 날짜별 묶음이 사라진 명세가 된다. 기존 문서 클래스를 복제하기 전에 실제 반환형과 공통 응답 처리까지 확인하고, 문서의 제네릭과 `getData()`를 실제 계약에 맞춘다.
- 공통 응답 클래스를 포함해 `schema.implementation` → 문서용 응답의 제네릭과 `getData()` → 실제 DTO/Controller 반환형 → 공통 응답 처리 순서로 맞는지 확인한다. 문서 생성·렌더링을 실행했다면 확인한 환경과 결과를 구분해 기록한다.
- 관련 없는 어노테이션 재배치, DTO 리팩터링, 런타임 응답 변경은 보강 범위에 넣지 않는다.
