# 모델 선택과 표기

## Entity 생성·변경

- 생성 의도와 필요한 입력이 드러나는 정적 메서드를 사용한다. 이미 `ofCreateRequest(request, relatedEntity)`를 쓰는 도메인은 그 방식을, `create(field, ...)`를 쓰는 도메인은 그 방식을 이어 쓴다. 하나의 이름이나 입력 형태로 통일하지 않는다.
- 상태 변경은 Entity 안의 의미 있는 메서드로 표현한다. 원본의 `SurveyParticipationEntity.ofSurveyStart`, `sectionSubmitted`, `complete`는 이 선택의 예다. 해당 설문 규칙이나 시간 정책을 다른 모델에 복제하지 않는다.
- 요청 DTO를 Entity가 직접 받는 형태도 원본에 존재한다. 별도 command 모델을 의무적으로 만들거나 DTO 의존을 제거하는 리팩터링으로 확대하지 않는다.
- 이미 setter가 필요한 관계 필드나 조립 모델은 그 이유를 확인하고 유지한다. 기존 `PlanCardEntity`의 학습 이력 목록에도 개별 `@Setter`가 있다.

## 응답 변환과 record/class

| 상황 | 이 관례에서의 기본 선택 |
| --- | --- |
| 한 번 구성해 반환하는 단순 응답, 이벤트 값 묶음 | record와 생성자 또는 명명된 정적 팩토리 |
| Entity와 준비된 연관 자료를 응답으로 변환 | 응답 DTO의 `ofEntity`·`of...` 또는 생성자. 서비스가 조회한 자료를 인자로 전달 |
| 요청 바인딩 후 경로·인증 주체를 보충하는 모델 | 기존 mutable class와 필요한 setter 유지 |
| 상속 기반 공통 요청, 단계별 집계나 응답 조립 | 기존 class 구조 유지. record로 바꾸기 위해 호출 흐름을 재설계하지 않음 |

DTO 안에서 응답 표현을 만드는 것과 DB 조회·외부 호출을 수행하는 것을 구별한다. 원본 MenuService는 조회와 정렬·부모별 그룹화를 하고, MenuDto가 전달받은 자료를 응답 트리로 변환한다. DTO마다 별도 Mapper를 만드는 관례는 추출되지 않았다.

필드 이름·접근자·생성자 변경이 직렬화 계약을 바꿀 수 있으므로 기존 JSON 이름을 따라간다. 과거의 특정 필드 오류를 모든 boolean 이름에 적용하는 금지 규칙으로 만들지 않는다.

## 정확한 null 표기와 final

- 원본의 모델 메서드와 응답 값 표기에 반복 사용된 타입은 `org.jspecify.annotations.NonNull`과 `org.jspecify.annotations.Nullable`이다. 같은 선택을 쓰는 대상 프로젝트에서는 정확한 import를 유지한다. 코드에 `@NonNull`이 있다는 이유만으로 런타임 null 검사를 구현했다고 간주하지 않는다.
- 입력 제약의 `jakarta.validation.constraints.NotNull`은 별개다. 모델의 null 계약 표기를 Bean Validation 대용으로 쓰거나, 검증 어노테이션을 JSpecify로 교체하지 않는다. 프로젝트가 다른 null 표기 체계를 쓰면 기존 체계를 따른다.
- 구현 메서드에서 재할당하지 않는 매개변수는 `final`을 우선한다. 인터페이스 선언까지 기계적으로 추가하거나 의도적으로 재할당하는 지역변수를 억지로 분리하지 않는다.
- 지역변수 `final`은 보존된 IDE 설정의 선호지만 소스에서는 일관되게 강제되지 않는다. 새 코드의 인접 표현에 맞추고, 스타일 변경만으로 넓은 diff를 만들지 않는다.

## 기본으로 넣지 않는 요소

`@Builder`, `@Data`, 모든 필드의 setter, 별도 Mapper, 커스텀 null 처리 추상화를 편의상 일괄 추가하지 않는다. 필요성과 해당 도메인의 기존 사용을 보고 선택한다. 이 제한은 해당 요소의 사용 금지를 의미하지 않는다.
