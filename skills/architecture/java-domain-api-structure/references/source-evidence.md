# 근거와 적용 한계

확인일은 2026-10-16, 원본 저장소는 `eci-my247-api`, 현재 소스 기준은 `8b06115`이다. 아래 경로는 저장소 루트 기준이며 `src/main/java/com/etoos/my247/`를 생략했다. 파일의 현재 존재·동작은 적용할 프로젝트에서 다시 확인한다. 이 자료를 사용하려고 원본 저장소에 접근할 필요는 없다.

`git log --all --no-merges --author='sangsoo.lee@etoos.com'`의 2025-11-24~2026-10-15 이력에서 구조·모델 관련 파일의 추가/수정/삭제/이름 변경을 분류하고, 대표 구현과 후속 변경의 diff 및 현재 소스를 확인했다. 아래는 규칙에 필요한 근거만 추린 것이다. author 표기는 기여 귀속 근거이며 개인의 단독 설계 의도를 증명하지는 않는다.

| 보존한 선택 | 커밋·날짜 | 원본 경로 | 귀속과 현재 해석 |
| --- | --- | --- | --- |
| 도메인별 Service/Impl, Repository/CustomRepository/Impl | `208988c` · 2026-08-03 / `1643fca` · 2026-08-04 | `menu/{presentation,application/service,infrastructure}/`, `banner/{presentation,application/service,infrastructure}/` | 이상수 직접 신규 추가. 각각 Controller부터 저장소까지 같은 조합으로 작성했으며 현재 유지 |
| 같은 패키지 규칙의 중간 시기 적용 | `7130033` · 2026-04-07 / `3eae3d1` · 2026-04-09 | `survey/application/service/SurveyService.java`, `survey/application/service/impl/SurveyServiceImpl.java`, `survey/infrastructure/` | 이상수 신규 작성·확장. 최신 메뉴·배너만으로 추정한 구조가 아님 |
| 앱/내부 진입점에서 대상자 결정 후 서비스 재사용 | `895696e` · 2026-01-02 / `88b1f0c` · 2026-01-13 | `plan_card/presentation/PlanCardController.java`, `plan_card/presentation/InternalPlanCardController.java` | 이상수 내부 조회 신규 추가 후 생성/수정/삭제 확장. 현재 같은 PlanCardService 사용 |
| 다른 업무에도 내부 진입점 적용 | `1135815` · 2026-01-08 / `0f1e20c` · 2026-01-09 | `profile/presentation/{university,major}/Internal*Controller.java`, `payment/presentation/payment/InternalPaymentController.java` | 이상수 추가. 결제 Internal 파일은 현재 없어 현재 생성 표본으로 사용하지 않음 |
| 기존 App/Internal 요청 처리 보강 | `498c477` · 2026-06-04 | `acdm_schedule/presentation/{AcademicScheduleController,InternalAcademicScheduleController}.java` | 이상수 multipart 처리 보강. 기본 컨트롤러 구조의 최초 작성자로 귀속하지 않음 |
| record 이벤트와 목적별 수신 서비스 | `ba1d8c6` · 2026-02-14 / `291118d` · 2026-02-19 | `plan_card/application/event/`, `plan_card/application/service/PlanCardReserveNotificationService.java`, `plan_card/application/service/PlanCardReserveRecordService.java` | 이상수 신규 추가·확장. 측정 이벤트 payload는 이후 필요한 시각·학생 정보로 확장됨 |
| 별도 도메인의 후커밋 파일 정리 | `0ba2885` · 2026-03-24 | `quest/application/service/impl/QuestServiceImpl.java`, `s3/application/event/FileRemoveEvent.java`, `s3/application/service/FileEventService.java` | 이상수 직접 추가. 예약 데이터 삭제 후 파일 번호 목록 발행, 파일 서비스가 후처리 |

## 강제 규칙으로 채택하지 않은 부분

- `92f5858`(2025-11-24) initial commit의 `commons`와 leaderboard 구조만으로 개인 규칙을 추출하지 않았다. 이후 새 도메인에서 반복한 선택을 근거로 삼았다.
- `9e83ffc`(2026-02-06)에서 상담 Internal Controller와 Facade가 삭제되었다. 과거 존재했던 Facade 계층을 항상 추가하는 규칙은 만들지 않았다.
- `PlanCardReserveNotificationService`는 변경/삭제 이벤트를 `AFTER_COMMIT`으로, 측정 시작 이벤트를 일반 `@EventListener`로 수신한다. 실행 시점을 통일하는 규칙은 없다.
- `5c05eaf`(2026-04-10)는 순환 참조와 관련된 주입 필드를 제거했다. 이 한 건의 수정 자체를 일반 설계 규칙으로 확대하지 않았다.
- 기존 `ltr/domain`, 세분화된 `profile/presentation/...`, `banner/presentation/dto/BannerDto.java` 같은 배치도 있다. 예시 디렉토리와 다르다는 이유만으로 이동하지 않는다.
