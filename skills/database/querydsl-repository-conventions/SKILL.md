---
name: querydsl-repository-conventions
description: "Java/Spring 프로젝트에서 QueryDSL 조회 Repository와 조회 결과 DTO·VO를 작성하거나 수정할 때 사용한다. 도메인별 CustomRepository 구성, 조회 결과 조립과 projection·체인 줄바꿈을 적용하며, 일반 SQL 튜닝이나 모든 조회의 DTO 전환에는 사용하지 않는다."
---

# QueryDSL 조회 Repository 관례

## 목적과 범위

조회 구현의 위치와 결과 객체를 기존 도메인 구조에 맞추고, 조회 절과 projection 인자를 읽기 쉽게 작성한다. 보존할 선호는 CustomRepository 분리, 기존 조회 지원 클래스 재사용, 결과의 용도에 따른 DTO·VO 선택이다. 특정 페이징 알고리즘·트랜잭션 방식은 이 스킬의 규칙이 아니다.

## 작업 절차

1. **도메인 안의 기존 조회 구조 확인**
   - 대상 Repository, CustomRepository, 구현체와 호출 Service를 함께 읽는다. 기존 QueryDSL 버전과 공통 지원 클래스를 확인한다.
   - 현재 프로젝트의 명시적 지침과 인접 구현을 우선한다. 이 관례를 적용한다는 이유로 공통 프레임워크를 새로 만들거나 기존 Repository 전체를 재배치하지 않는다.
   - 조회 호출부로 Service 클래스를 새로 만들면 [신규 Service 생성자 주입](../../architecture/java-domain-api-structure/SKILL.md#신규-service-생성자-주입)을 함께 적용한다. 필요한 절만 참조하며 전체 패키지 재편이나 `Interface/Impl` 분리를 추가하지 않는다. 이 작업을 지원하도록 스킬을 따로 배포할 때는 `architecture/java-domain-api-structure`도 인벤토리의 상대 배치를 유지하여 함께 포함한다.
   - 호출 Service를 새로 만들거나 트랜잭션을 조정하면 [Service 트랜잭션과 readOnly](../../architecture/java-domain-api-structure/SKILL.md#service-트랜잭션과-readonly)도 적용한다. 조회 전용의 `readOnly = true`에는 프로젝트의 읽기 전용 DB 분기 목적도 있으므로 단순 성능 옵션으로 보고 생략하지 않는다.

2. **조회 구현 위치 맞추기**
   - 이 구조를 채택한 도메인은 `infrastructure/<Domain>Repository`에서 `JpaRepository`와 `<Domain>CustomRepository`를 함께 확장한다.
   - 조회 계약은 `infrastructure/<Domain>CustomRepository`, QueryDSL 구현은 `infrastructure/impl/<Domain>CustomRepositoryImpl`에 둔다.
   - `Querydsl6RepositorySupport` 같은 지원 클래스가 있으면 기존 `select`, `selectFrom`, query factory 접근 방식을 재사용한다. 이름이나 버전까지 다른 프로젝트에 복제할 필요는 없다.
   - ECI 프로젝트의 CustomRepository 구현체에서 QueryDSL을 사용하면 [ECI support 상속 지침](../eci-querydsl-repository-support/SKILL.md)을 함께 확인한다. 공통 support의 존재 여부에 따른 필수 상속·적용 제외는 해당 스킬에서 관리한다. 이 작업을 지원하는 배포본에는 두 스킬을 같은 `database` 아래에 함께 포함한다.
   - 단순 파생 조회·기존 JPQL 메서드까지 모두 CustomRepository로 옮기지는 않는다.

3. **최종 응답과 조회 중간 결과 구분**

   | 조회 결과의 용도 | 우선 검토할 형태 |
   | --- | --- |
   | 필요한 컬럼이 바로 응답을 구성함 | 기존 응답 DTO의 `@QueryProjection` 생성자로 조회 |
   | 추가 조회·반복 전개·여러 결과의 조립이 필요함 | 별도 조회용 Row·VO를 반환한 뒤 응답 DTO로 조립 |
   | 엔티티 자체가 후속 처리에 필요하고 기존 조회가 그 계약을 가짐 | 엔티티 반환 유지 |

   - DTO가 record인지 일반 클래스인지, 중간 객체가 `application/vo`인지 `infrastructure/vo`인지는 인접 구현에 맞춘다. 새로운 공통 `Row` 계층을 만들지 않는다.
   - 조회 인수와 최종 응답 필드가 다르면 기존 DTO의 projection 생성자·팩토리에서 순수한 값 변환을 수행하는 방식을 따른다. DB 재조회나 업무 흐름을 DTO에 넣지 않는다.
   - 컬렉션 조립이 필요한 조회는 부모 결과와 관련 ID 목록으로 조회한 데이터를 나누어 `Map<ID, List<...>>`로 합치는 기존 사례를 검토한다. 단순 조회에도 이 단계를 일률적으로 추가하지 않는다.

4. **기존 선택을 근거 없이 통일하지 않기**
   - `@QueryProjection`, `Projections.constructor`, 엔티티 조회가 공존할 수 있다. 변경한 projection의 인수 순서·타입과 생성자를 함께 맞춘다.
   - 공통 조건을 재사용하는 조회에는 기존 `base.clone()` 구성을 따를 수 있다. `PageImpl`, `PageableExecutionUtils`, count 방식이나 트랜잭션 경계를 하나로 강제하지 않는다.
   - DTO와 Row의 선택이 애매하거나 기존 조회를 분리하려는 경우에만 [조회 결과 형태 선택](references/query-result-shapes.md)를 읽는다.

5. **조회 구간과 표현식을 읽기 쉽게 작성하기**
   - 메서드의 구간 주석·빈 줄과 지역변수 유지 기준은 [Java 구현 코드 가독성](../../backend/java-code-readability/SKILL.md)을 함께 적용한다. 이 공통 규칙을 별도로 복제하지 않으며, 개별 배포 시 `backend/java-code-readability`도 인벤토리의 상대 배치를 유지하여 포함한다.
   - QueryDSL 조회는 `.from()`, `.join()`·`.leftJoin()`, `.on()`, `.where()`, `.groupBy()`, `.having()`, `.orderBy()`, `.offset()`, `.limit()` 등 사용한 절마다 줄을 나눈다. `.fetch()`, `.fetchOne()` 같은 마지막 실행 호출도 별도 줄에 둔다.
   - 여러 컬럼을 받는 `select`, `new Q...(...)`, `Projections.constructor(...)`는 중첩 호출 경계를 드러내고 인자마다 줄을 나눈다. 인자를 첫 줄에 몰아넣은 뒤 나머지만 들여쓰지 않는다.
   - 조회식을 작성하거나 압축된 조회 코드를 정리할 때 [QueryDSL 줄바꿈 예시](references/query-formatting.md)를 읽는다. 예시의 쿼리 분리·페이징 알고리즘을 다른 조회에 새로 강제하지 않는다.

## 결과물과 확인

- 변경한 조회 계약, 구현, DTO·VO와 호출부가 같은 결과 형태를 사용하도록 맞춘다.
- 조건 구성·조회·페이징·결과 조립이 실제 역할별로 구분되는지, projection 인자와 쿼리 절이 줄바꿈으로 드러나는지 확인한다. 서식 수정만으로 조건·정렬·인자 순서·조회 횟수가 바뀌지 않아야 한다.
- projection을 변경했다면 프로젝트의 기존 생성·컴파일 경로로 Q 타입과 생성자 연결을 확인한다. 조회의 묶음·조립·페이징을 바꿨다면 그 변경에 해당하는 결과 수, 순서, 하위 목록을 확인한다.
- 실행 검증과 소스 검토를 구분해서 보고한다. 이 스킬은 조회 성능이나 운영 DB 결과를 미리 보증하지 않는다.
