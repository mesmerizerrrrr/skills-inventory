# 모델 작성 예시

생성·변경 메서드와 DTO 변환의 형태를 설명하는 예시다. 업무 제약과 JPA 매핑은 대상 모델의 계약에 맞게 작성한다. record/class와 null/final 선택 기준은 [모델 선택과 표기](model-choices.md)를 따른다.

## 생성과 상태 변경

```java
public class Item {
    private String name;
    private boolean completed;

    private Item(final String name) {
        this.name = name;
    }

    public static Item create(final String name) {
        return new Item(name);
    }

    public void updateName(final String name) {
        this.name = name;
    }

    public void complete() {
        this.completed = true;
    }

    public String getName() {
        return name;
    }

    public boolean isCompleted() {
        return completed;
    }
}
```

`create`, `updateName`, `complete`처럼 호출부가 의도를 표현하게 한다. 기존 도메인이 `ofCreateRequest(request, relatedEntity)`를 사용한다면 그 서명을 유지할 수 있다. 예시와 맞추기 위해 요청 DTO를 별도 command로 변환하거나 모든 생성 메서드를 같은 이름으로 바꾸지 않는다.

필요한 관계 목록만 setter로 연결하는 모델도 허용한다. 변경 의도를 메서드로 표현하는 원칙이 모든 setter의 제거를 요구하는 것은 아니다.

## DTO가 소유하는 단순 변환

위 `Item`을 응답으로 바꾸는 경우:

```java
public record ItemResponse(String name, boolean completed) {
    public static ItemResponse ofEntity(final Item item) {
        return new ItemResponse(item.getName(), item.isCompleted());
    }
}
```

서비스는 필요한 데이터를 조회·정렬하고 `ItemResponse.ofEntity(item)`을 호출한다. 연관 자료가 더 필요하면 서비스가 준비한 값을 변환 메서드에 전달한다. DTO가 Repository를 호출하거나 네트워크 요청을 수행하게 하지 않는다.

요청 바인딩 뒤 경로값이나 인증 주체를 채워야 한다면 mutable class가 적합할 수 있다. 단계별 집계·상속이 필요한 응답도 class를 유지할 수 있으며, 요청은 class·응답은 record라는 고정 규칙으로 바꾸지 않는다. `@Builder`나 별도 Mapper는 조립 필요성과 기존 도메인의 사용 방식을 보고 결정한다.

## 직렬화와 null 계약 확인

예를 들어 기존 응답 키가 `"isCompleted"`라면 Java 필드·접근자 또는 record/class를 바꾸어도 그 JSON 계약을 유지해야 한다. 필요한 경우 프로젝트의 직렬화 설정이나 명시적 매핑을 사용하고 실제 응답을 확인한다. `is` 접두사의 사용 여부만으로 결과를 단정하지 않는다.

JSpecify의 `@NonNull`·`@Nullable`은 값의 null 계약을 표현하고, Bean Validation의 `@NotNull`은 입력 검증 제약을 표현한다. 표기 변경이 필요하면 정확한 import와 적용 위치를 확인하고, 런타임 검증이 필요한 경계에서는 검증 실행 여부도 확인한다.
