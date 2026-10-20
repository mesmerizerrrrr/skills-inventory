# 공통 support 상속과 초기화 예시

아래는 상속과 조회 진입 형태를 설명하는 가상 예시다. `TaskEntity`, `QTaskEntity`, `TaskCustomRepository`는 예시용 이름이다. 실제 코드에서는 현재 도메인의 Entity·인터페이스·생성된 Q타입과 **프로젝트에 존재하는 support**를 사용한다.

## 도메인 클래스를 받는 support

다음 예시는 `Querydsl6RepositorySupport`가 `Class`를 받는 생성자와 `selectFrom(EntityPath<T>)`를 제공하고, 부모의 주입 메서드에서 `EntityManager`와 factory를 초기화하는 경우다. `java.util.List` 및 실제 도메인·support 타입의 import는 프로젝트에 맞춘다.

```java
/**
 * {@link Querydsl6RepositorySupport}를 사용해 작업을 조회한다.
 */
public class TaskCustomRepositoryImpl extends Querydsl6RepositorySupport
        implements TaskCustomRepository {

    /**
     * {@link TaskEntity}를 조회할 공통 support를 구성한다.
     */
    public TaskCustomRepositoryImpl() {
        super(TaskEntity.class);
    }

    /**
     * 식별자에 해당하는 작업 목록을 조회한다.
     *
     * @param taskId {@link Long} 조회할 작업 식별자
     * @return {@link List}&lt;{@link TaskEntity}&gt; 조회된 작업 목록. 없으면 빈 목록
     */
    @Override
    public List<TaskEntity> findByTaskId(final Long taskId) {
        final QTaskEntity task = QTaskEntity.taskEntity;
        return selectFrom(task)
                .where(task.id.eq(taskId))
                .fetch();
    }
}
```

구현체에는 `EntityManager`·`JPAQueryFactory` 필드나 주입 코드가 없다. Spring이 부모에 정의된 주입 경로를 처리하고, 조회 시점에는 부모의 `selectFrom(...)`이 초기화된 factory를 사용한다. Repository 구현체의 Bean 발견·등록 방식은 대상 프로젝트의 기존 구성에 맞춘다.

## 다른 support 버전에 적용하기

- `Querydsl4RepositorySupport`가 준비된 프로젝트에서는 그 클래스의 실제 import와 생성자를 사용한다. 위 예시의 `6`을 설치된 QueryDSL 버전 숫자로 단순 치환하지 않는다.
- `select`, `selectFrom`, `getQueryFactory`가 모두 있는지 확인한다. 어떤 support에 `from(...)`이 있다고 해서 다른 support에도 호출을 복사하지 않는다.
- 부모가 제공하는 `getQueryFactory()`가 필요하다면 그 반환 factory를 사용한다. `getEntityManager()`를 얻어 별도의 factory를 만드는 방식으로 되돌리지 않는다.
- Jakarta 기반 support를 `javax.persistence` 기반 프로젝트로 복사하지 않는다. 반대 방향도 마찬가지다. 기존 support의 persistence API와 의존성 구성을 따른다.
- 기본 생성자가 없고 `Class`를 요구하는 부모에는 `super(TaskEntity.class)`가 필요하다. 구현체에 `@RequiredArgsConstructor`만 붙이면 해결된다고 가정하지 않는다.

## 구현체 자체 의존성이 추가로 필요한 경우

부모가 요구하는 생성자 호출과 구현체 자신의 의존성 주입은 하나의 명시적 생성자에서 처리한다. 예를 들어 시간 조건을 계산하기 위해 `java.time.Clock`을 주입하는 구현이라면 다음 형태다. 이 예시 때문에 `Clock`이나 설정 Bean을 새로 추가하지 않는다.

```java
private final Clock clock;

/**
 * {@link TaskEntity}의 공통 조회 지원과 시간 조건의 기준을 구성한다.
 *
 * @param clock {@link Clock} 조회 시점의 시간 조건 계산에 사용할 시계
 */
public TaskCustomRepositoryImpl(final Clock clock) {
    super(TaskEntity.class);
    this.clock = clock;
}
```

추가 의존성 주입을 위해 부모의 `setEntityManager(...)`를 덮어쓰거나 `JPAQueryFactory`를 다시 만들 필요는 없다. 실제 support가 다른 생성자 계약을 제공하면 그 계약에 맞춘다.

## support가 없는 경우

ECI 프로젝트라도 현재 모듈과 사용하는 공통 의존성에 해당 support가 없으면 이 스킬의 상속 규칙은 적용하지 않는다. 기존 프로젝트가 `JPAQueryFactory` Bean을 주입하거나 다른 방식으로 초기화한다면 그 구성을 이어 쓴다. 존재하지 않는 support import·상속 선언을 추가하지 않는다.
