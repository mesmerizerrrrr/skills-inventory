# QueryDSL 줄바꿈 예시

## 예시의 전제

다음은 부모 예약을 페이징한 뒤 현재 페이지의 첨부를 별도로 조회하는 **메서드 서식 예시**다. 부모·첨부 분리 조회나 이 count 방식을 모든 조회에 요구하지 않는다. `ReservationPageRows`는 `Page<ReservationRow>`와 `List<ReservationFileRow>`를 받으며, Q타입과 projection 생성자는 이미 준비되어 있다고 가정한다.

여기서 `queryFactory`는 기존 프로젝트 방식으로 초기화되어 접근 가능한 `JPAQueryFactory`다. 이 예시를 쓰려고 별도 factory 초기화를 추가하지 않는다. ECI의 공통 support를 상속하는 구현은 부모의 실제 `select(...)`·`getQueryFactory()` 등으로 시작하며, 구체적인 상속·생성자는 [ECI support 상속 지침](../../eci-querydsl-repository-support/SKILL.md)을 따른다. 해당 경우 이 스킬도 같은 `database` 아래에 포함해야 한다.

프로젝트 support와 표준 Spring `QuerydslRepositorySupport`는 이름만으로 바꿔 쓸 수 없다. 부모에 접근 가능한 `queryFactory` 필드가 있다고 가정하지 않고, 생성자에 임의의 `Class<?>` 주입을 요구하지 않는다.

## 여러 역할이 이어지는 조회 메서드

```java
/**
 * 학생과 선택 상태의 부모 페이지를 조회하고 그 페이지의 첨부 전체를 추가 조회한다.
 *
 * @param studentId {@link Long} 조회할 학생 식별자
 * @param status {@link ReservationStatus} 선택 상태. {@code null}이면 상태 제한 없음
 * @param pageable {@link Pageable} 페이지 번호와 크기. 예약 식별자 내림차순 정렬은 고정
 * @return {@link ReservationPageRows} 부모 기준 전체 건수와 정렬된 부모·첨부 조회 결과
 */
@Override
public ReservationPageRows findPage(final Long studentId, final ReservationStatus status, final Pageable pageable) {

    // 예약과 첨부 조회에 사용할 Q타입 준비
    final QReservation reservation = QReservation.reservation;
    final QReservationFile file = QReservationFile.reservationFile;

    // 학생과 선택 상태로 공통 조회 조건 구성
    final BooleanBuilder condition = new BooleanBuilder(reservation.studentId.eq(studentId));
    if (status != null) {
        condition.and(reservation.status.eq(status));
    }

    // 예약을 기준으로 현재 페이지 조회
    final List<ReservationRow> parents = queryFactory.select(
        new QReservationRow(
            reservation.id,
            reservation.studentId,
            reservation.reservationDate,
            reservation.memo,
            reservation.status
        )
    )
        .from(reservation)
        .where(condition)
        .orderBy(reservation.id.desc())
        .offset(pageable.getOffset())
        .limit(pageable.getPageSize())
        .fetch();

    // 동일 조건의 전체 건수로 부모 페이지 조립
    final Long count = queryFactory.select(
        reservation.id.count()
    )
        .from(reservation)
        .where(condition)
        .fetchOne();

    final Page<ReservationRow> page = new PageImpl<>(
        parents,
        pageable,
        count == null
            ? 0
            : count
    );

    // 빈 페이지는 첨부 조회 없이 반환
    if (parents.isEmpty()) {
        return new ReservationPageRows(page, List.of());
    }

    // 현재 페이지의 예약에 속한 첨부 조회
    final List<Long> parentIds = parents.stream()
        .map(ReservationRow::id)
        .toList();
    final List<ReservationFileRow> files = queryFactory.select(
        new QReservationFileRow(
            file.id,
            file.reservationId,
            file.name
        )
    )
        .from(file)
        .where(file.reservationId.in(parentIds))
        .orderBy(file.id.asc())
        .fetch();

    return new ReservationPageRows(page, files);
}
```

`parents`, `count`, `page`, `parentIds`, `files`는 처리 단계를 드러내므로 유지한다. 마지막 반환값을 `result`에 담아 바로 반환하는 변수는 추가하지 않는다. `files`를 제거하려고 첨부 조회 전체를 반환 생성자의 인자 안에 넣으면 조회와 조립의 경계가 흐려진다.

위 코드는 기존의 조건·정렬·쿼리 실행 순서·빈 페이지 조기 반환을 유지하면서 서식을 드러낸 예시다. Java 버전이 다른 작업에 `List.of()`·`Stream.toList()`까지 복사하지 않고 대상 프로젝트에서 사용 가능한 API를 유지한다.
