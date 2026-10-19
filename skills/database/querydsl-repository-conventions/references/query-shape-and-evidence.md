# 조회 형태 선택의 사례와 근거

DTO 직접 조회와 중간 Row·VO 중 선택하거나 기존 조회를 분리할 때만 읽는다. 경로는 모두 `eci-my247-api` 저장소 기준이며, 다른 프로젝트에서 이 파일들이 존재해야 하는 것은 아니다.

## 반복해서 사용한 구조

- **단순 응답 projection:** `push/presentation/dto/response/AppPushHistoryResponse.java`는 record의 생성자에 `@QueryProjection`을 두고, CustomRepository가 `QAppPushHistoryResponse`를 생성한다.
- **조회 인수와 응답 필드가 다른 DTO:** `banner/presentation/dto/BannerDto.java`는 원본 URL과 파일 URL을 조회 생성자로 받아 하나의 응답 URL로 정한다. 순수 변환은 이 생성자에 있고 조회 조인은 Repository에 있다.
- **조회용 중간 객체:** 공지 상세는 `infrastructure/vo/NoticeDetailMappingVo`, 플랜카드는 `application/vo/PlanCardSearchRow`를 사용한다. 중간 객체 위치는 한 가지로 통일되어 있지 않다.
- **여러 조회의 조립:** 플랜카드는 Row 목록과 카드 ID별 학습 이력 Map으로 응답을 만든다. 상담은 조회된 상담 ID 목록으로 댓글·과목을 조회해 응답을 조립한다.
- **엔티티 반환도 유지:** 메뉴 Repository는 엔티티 목록을 반환하고, 이후 `MenuDto.ofEntity`로 트리를 만든다. 모든 조회를 응답 DTO projection으로 바꾸는 규칙은 없다.

위 축약 경로 앞에는 `src/main/java/com/etoos/my247/`가 붙는다. 참조 위치는 사례이며 새 도메인의 업무 조건·정렬·수치는 복사하지 않는다.

## 보존하지 않는 선택

- 공지·푸시의 `PageImpl`과 상담의 `PageableExecutionUtils`는 공존한다. 상담의 메모리 필터·slice까지 표준 페이징 기법으로 삼지 않는다.
- 플랜카드의 `Projections.constructor`와 다른 도메인의 `@QueryProjection`이 공존한다. 생성 방식은 주변 코드와 변경 목적에 맞춘다.
- `2791e2a`에서 플랜카드 조회 Service의 트랜잭션을 제거했지만, `6d1de95`에서 다시 `@Transactional(readOnly = true)`가 추가됐다. 과거 성능 개선 커밋을 근거로 트랜잭션 제거를 일반 원칙으로 만들지 않는다.
- 공통 지원 클래스의 `fetchPage`나 `hasAnyBit`가 있다는 이유만으로 모든 조회에서 사용하게 하지 않는다.

## 출처

2026-10-16, `eci-my247-api`의 아래 경로에 대한 이상수 `<sangsoo.lee@etoos.com>`의 전기간 비병합 변경 이력과 주요 diff를 현재 코드와 대조했다. 경로는 저장소 상대 경로다.

| 커밋·날짜 | 대표 경로 | 확인한 선택 |
| --- | --- | --- |
| `92f5858` · 2025-11-24 | `src/main/java/com/etoos/my247/commons/infrastructure/db/querydsl/Querydsl6RepositorySupport.java` | initial commit에 이미 존재. 개인이 처음 고안한 구조라고 주장하지 않음 |
| `258e009` · 2025-12-18 | `src/main/java/com/etoos/my247/notice/infrastructure/impl/BoardPostCustomRepositoryImpl.java` | 공지 목록의 CustomRepository와 DTO 조회 |
| `8a93475` · 2026-01-21 | `src/main/java/com/etoos/my247/counsel/infrastructure/impl/CounselCustomRepositoryImpl.java` | 상담 조회 VO 및 하위 목록 조립 |
| `a009816` · 2026-04-28 | `src/main/java/com/etoos/my247/notice/infrastructure/vo/NoticeDetailMappingVo.java` | 응답 전에 사용할 별도 조회 VO |
| `2791e2a` · 2026-05-13, `6d1de95` · 2026-06-05 | `src/main/java/com/etoos/my247/plan_card/application/service/impl/PlanCardServiceImpl.java` | Row·이력 Map 조립 유지, 트랜잭션 정책은 후속 변경됨 |
| `450b5de` · 2026-07-27 | `src/main/java/com/etoos/my247/push/presentation/dto/response/AppPushHistoryResponse.java` | record의 QueryProjection 생성자 |
| `208988c` · 2026-08-03, `1643fca` · 2026-08-04, `a0667d5` · 2026-08-05 | `src/main/java/com/etoos/my247/menu/infrastructure/impl/MenuCustomRepositoryImpl.java`, `src/main/java/com/etoos/my247/banner/presentation/dto/BannerDto.java` | 엔티티 조회와 DTO projection을 용도에 따라 병용 |

이는 소스와 커밋에서 확인한 구조의 근거다. 각 조회의 운영 성능·현재 데이터 정확성을 검증한 기록은 아니다.
