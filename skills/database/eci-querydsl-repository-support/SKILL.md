---
name: eci-querydsl-repository-support
description: "ECI 프로젝트에서 CustomRepository 인터페이스를 구현하면서 QueryDSL을 사용하는 클래스를 생성하거나 수정할 때 사용한다. 프로젝트에 준비된 Querydsl 버전별 RepositorySupport의 필수 상속과 초기화 재사용을 다룬다. 해당 support가 없거나 QueryDSL을 사용하지 않는 구현에는 적용하지 않는다."
---

# ECI 프로젝트 내에서의 QueryDSL 구현 클래스 구현 시 지침

## 목적과 적용 조건

프로젝트가 준비한 QueryDSL support를 상속하여 `EntityManager` 주입과 `JPAQueryFactory` 생성·초기화의 중복을 피한다. 다음 조건을 모두 만족하면 적용한다.

- 현재 작업 대상이 ECI 프로젝트다.
- 대상 클래스가 `~CustomRepository` 등 프로젝트의 커스텀 Repository 인터페이스를 구현하고 QueryDSL을 사용한다. 접미사 철자만 보지 말고 실제 인터페이스와 구현을 확인한다.
- 대상 모듈에서 사용할 수 있는 `Querydsl6RepositorySupport`, `Querydsl4RepositorySupport` 등 프로젝트 공통 support가 준비되어 있다.

**조건에 해당하면 구현체는 해당 support를 반드시 상속한다.** 단순히 `select` 같은 메서드 이름을 비슷하게 구현하거나 별도 factory를 주입하는 것으로 대체하지 않는다.

support가 준비되어 있지 않으면 이 스킬의 상속 규칙을 적용하지 않고 프로젝트의 기존 QueryDSL 초기화 방식을 따른다. 이 규칙을 충족시키기 위해 support를 새로 만들거나 다른 프로젝트에서 복사하거나 QueryDSL·Spring Boot·JDK 버전을 변경하지 않는다. JDBC·JPQL만 사용하는 구현, 일반 Spring Data 인터페이스, ECI가 아닌 프로젝트에 상속을 강제하지 않는다.

## 구현 전에 확인할 사항

1. 대상 모듈의 `build.gradle`·`pom.xml` 등에서 JDK, Spring Boot, QueryDSL 의존성과 persistence API를 확인한다. 버전이 BOM 등에서 관리되면 필요한 경우 의존성 해석 결과를 확인한다.
2. 프로젝트 소스와 현재 모듈이 사용하는 공통 모듈·의존성에서 support 선언과 인접 구현체를 찾는다. 클래스 이름을 `Querydsl{버전}RepositorySupport`로 추측해 만들지 않는다. 이름의 숫자와 실제 라이브러리 버전이 같다고 단정하지 않는다.
3. 실제 support의 패키지, 생성자, 접근 가능한 메서드, `EntityManager` 주입·factory 초기화 경로를 읽는다. `javax.persistence`와 `jakarta.persistence`, QueryDSL 배포 그룹·버전은 대상 프로젝트와 일치시킨다.
4. 여러 support나 데이터소스가 있으면 대상 Entity의 persistence unit과 인접 Repository가 사용하는 support를 선택한다. 다른 데이터소스 전용 support를 이름만 보고 가져오지 않는다.

## 구현 규칙

- 클래스에 `extends 실제Support클래스 implements 실제CustomRepository인터페이스`를 선언한다. 기존 중간 부모가 이미 해당 support를 상속한다면 그 상속 경로를 유지한다. 다른 부모와 충돌하면 임의로 제거하거나 필수 상속을 생략하지 말고 대상 클래스의 상속 구조를 먼저 확인한다.
- support 생성자가 도메인 클래스를 요구하면 **명시적 생성자에서 `super(실제Entity.class)`를 호출한다.** DTO, Q타입, Repository 인터페이스를 도메인 클래스로 넘기지 않는다. 다른 생성자 계약을 가진 support라면 실제 선언에 맞춘다.
- 추가 의존성이 필요한 구현체는 같은 생성자에서 `super(...)` 호출 후 자신의 필드를 초기화한다. Lombok 생성자 어노테이션만으로 필요한 부모 생성자 호출이 생성된다고 가정하지 않는다. Service의 생성자 주입 규칙을 이 Repository의 상속 생성자에 기계적으로 적용하지 않는다.
- 조회는 부모가 제공하는 `select(...)`, `selectFrom(...)`, `from(...)`, `getQueryFactory()` 등 **실제로 존재하는 API**를 사용한다. 버전별 support가 같은 메서드를 제공한다고 가정하지 않는다.
- support가 관리하는 `EntityManager`·`JPAQueryFactory`를 구현체에서 다시 필드로 선언·주입하거나 `new JPAQueryFactory(entityManager)`로 재생성하지 않는다. 필요한 경우 부모의 실제 접근자를 사용한다. 부모의 주입 메서드를 이유 없이 재정의하거나 생성자에서 수동 초기화하지 않는다.
- 부모의 setter 주입 등으로 factory가 나중에 초기화되는 구조에서는 구현체 생성자에서 조회를 실행하지 않는다. Bean 초기화가 완료된 뒤 Repository 메서드에서 사용한다.
- 작업 중인 구현체가 별도 factory를 사용하고 있었다면 실제 호출을 부모 API로 옮긴 후 중복된 필드·주입·import를 정리한다. 관련 없는 Repository나 support의 내부 구현까지 일괄 수정하지 않는다.

생성자 작성이나 support별 API 차이를 확인할 때만 [상속과 초기화 예시](references/support-inheritance.md)를 읽는다. 지원 클래스에 페이징·비트 연산 등의 도구가 있다는 이유만으로 현재 조회에 불필요한 처리까지 추가하지 않는다.

## 결과 확인

- 구현체가 올바른 CustomRepository를 구현하고 프로젝트 support를 실제 상속하는지 확인한다.
- `super(...)`의 Entity와 support의 생성자 계약, persistence API·데이터소스가 대상 조회에 맞는지 확인한다.
- 부모가 제공하는 초기화를 중복하지 않았는지, 호출한 helper와 접근자가 실제로 존재하는지 확인한다.
- 프로젝트의 기존 생성·컴파일 절차로 Q타입, 부모 생성자와 메서드 연결을 확인한다. 초기화·주입 경로가 달라졌다면 가능한 범위에서 Spring Bean 생성과 해당 조회도 확인한다.
- 소스 확인, 컴파일 성공, Bean·조회 실행을 구분해서 보고한다. support가 없어 적용을 제외했다면 그 사실만 간단히 알린다.
