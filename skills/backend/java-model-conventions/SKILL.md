---
name: java-model-conventions
description: "Java Entity·요청/응답 DTO를 추가하거나 수정할 때 이상수의 생성·변경 메서드, DTO 내부 변환, record/class 선택과 null/final 표기 관례를 적용한다. 일반 Java 설명이나 DB 스키마 설계만 하는 작업에는 적용하지 않는다."
---

# Java 모델 작성 관례

## 적용 기준

`eci-my247-api`에서 반복된 모델 표현 방식을 보존한다. 사용자 요청과 대상 프로젝트의 규칙을 먼저 따르고, 기존 도메인의 타입·직렬화·생성 방식에 맞춘다. 스타일을 맞추기 위한 전면 재작성은 하지 않는다.

## 모델을 작성할 때

1. **Entity 생성과 변경:** 인접 Entity의 `ofCreateRequest`, `of...`, `create` 같은 정적 생성 메서드와 `update`, `complete`, `delete` 같은 의도별 변경 메서드를 따른다. 서비스는 필요한 객체를 준비하고 해당 메서드를 호출한다. 새 쓰기 모델에 광범위한 setter를 기본으로 열기보다 변경 단위를 메서드로 표현한다.
2. **DTO 변환 위치:** 단순 Entity → 응답 변환은 응답 DTO의 생성자나 `ofEntity`·`of...`에 둔다. 서비스는 조회·정렬·연관 데이터 준비를 맡고 변환을 호출한다. 이미 서비스에서 조립하는 응답을 모두 옮기거나 별도 Mapper 계층을 자동 도입하지 않는다.
3. **record/class 선택:** 불변 응답·값 묶음은 인접 코드가 사용하는 record를 우선한다. 바인딩 후 값 보충, 상속, 단계별 집계·변경이 필요한 모델은 기존 class 방식과 필요한 Lombok 어노테이션을 유지한다. 요청/응답이라는 이름만으로 타입을 결정하지 않는다.
4. **표기:** 재할당하지 않는 구현 메서드 매개변수의 `final` 사용을 우선하고, null 표기는 인접 코드가 사용하는 정확한 어노테이션 import를 확인한다. JSpecify `@NonNull/@Nullable`, Bean Validation `@NotNull`, Lombok `@NonNull`을 같은 표기로 교체하지 않는다. 상세 선택은 아래 참고 자료를 따른다.

## 조건에 따라 읽을 자료

- 새 Entity·DTO 작성, 타입 선택, null/final 표기가 애매할 때: [모델 선택과 표기](references/model-choices.md).
- 코드 서식 설정을 추가·복구하거나 이투스 포맷터를 요청받았을 때: [포맷터 적용 범위](references/formatter.md)와 보존된 XML을 사용한다. 보통의 모델 수정에서는 IDE 설정을 바꾸지 않는다.
- 다른 형태의 기존 코드가 있거나 출처를 확인할 때: [근거와 예외](references/source-evidence.md).

## 결과물과 확인

- 모델의 생성·변경 호출부와 직렬화되는 필드명이 기존 계약을 유지하는지 확인한다. record/class 변경, 생성자 시그니처 변경, null 처리 변경이 있다면 해당 경계의 실제 호출·직렬화·검증 동작을 확인한다.
- setter 전면 금지, record 전면 적용, 모든 인자·변수의 `final` 강제는 이 스킬의 규칙이 아니다. 쿼리 투영 방식·DB 매핑 정책도 이 스킬만으로 변경하지 않는다.
