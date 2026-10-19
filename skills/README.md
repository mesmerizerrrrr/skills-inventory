# 공통 스킬 인벤토리

여러 프로젝트에서 재사용할 작업 지침의 원본을 관리한다. `카테고리/스킬명/SKILL.md` 구조로 관리하며, 파일명과 스킬 식별자는 영문으로, 설명과 지침은 한글로 작성한다.

## AI가 읽는 순서

1. 아래 목록의 **카테고리와 적용할 작업**을 보고 현재 요청에 필요한 스킬만 선택한다. 맞는 스킬이 없으면 억지로 적용하지 않는다.
2. 선택한 스킬의 `SKILL.md`를 읽고 작업한다. 현재 요청 수행에 함께 필요한 경우에만 여러 스킬을 적용한다.
3. `references/`는 선택한 스킬에서 안내한 조건에 해당할 때만 읽는다. 모든 파일을 미리 읽지 않는다.
4. 유지보수 안내와 템플릿은 스킬을 추가하거나 수정할 때 읽는다.

이 인벤토리는 작업 방법을 제공한다. 현재 사용자의 요청과 대상 프로젝트의 적용 지침을 먼저 확인하고, 충돌하는 내용이 있으면 그 우선순위와 실제 작업 범위에 맞춰 적용한다.

## 카테고리

| 카테고리 | 분류 기준 | 현재 상태 |
| --- | --- | --- |
| `docs` | 코드 주석, API 사용법 등 이미 정해진 내용을 설명하는 문서 작성 | 스킬 2개; JavaDoc·Swagger 관례 보강 |
| `database` | DB 모델링·DDL, 조회 저장소, 저장 코드와 Java 타입의 매핑 | 스킬 4개 |
| `backend` | Java 모델·요청 검증·업무 예외 등 서버 코드 구현 | 스킬 2개 |
| `frontend` | 화면·컴포넌트 구현, 상태 관리, 사용자 상호작용 | 예정: 아직 스킬과 폴더 없음 |
| `architecture` | 시스템·모듈의 경계, 책임, 의존 관계를 설계하고 결정 | 도메인별 Java API 구성 스킬 1개 |

분류는 스킬의 **주목적**을 기준으로 한다. DB 설계는 `database`, DB API의 사용 문서 작성은 `docs`에 둔다. 여러 분야에 걸쳐도 스킬은 한 곳에서 관리하며 관련 분야는 적용 조건에 적는다. 새 작업군이 생기면 카테고리를 추가할 수 있다.

## 스킬 목록

카테고리는 관리용 구분이다. AI는 이 목록에서 필요한 진입 파일로 바로 이동하며, 카테고리 안의 모든 스킬을 읽지 않는다.

| 스킬 | 카테고리 | 적용할 작업 | 진입 파일 |
| --- | --- | --- | --- |
| `java-javadoc` | `docs` | Java 클래스·인터페이스·enum·메서드의 JavaDoc 작성 또는 수정 | [SKILL.md](docs/java-javadoc/SKILL.md) |
| `api-documentation` | `docs` | 호출자가 사용할 API 명세·사용법·요청/응답·오류 문서 작성 또는 수정 | [SKILL.md](docs/api-documentation/SKILL.md) |
| `etoos-db-modeling` | `database` | 이투스 업무 요구사항을 테이블·컬럼·키·논리 관계로 설계하고 DBA 전달 SQL 작성 | [SKILL.md](database/etoos-db-modeling/SKILL.md) |
| `etoos-postgresql-ddl` | `database` | 확정된 설계를 이투스 규칙의 PostgreSQL DDL `.sql`로 작성·수정·검토 | [SKILL.md](database/etoos-postgresql-ddl/SKILL.md) |
| `querydsl-repository-conventions` | `database` | QueryDSL 조회 저장소와 projection·조회 결과 조립을 기존 관례에 맞게 구현 | [SKILL.md](database/querydsl-repository-conventions/SKILL.md) |
| `jpa-coded-enum-mapping` | `database` | `ORDINAL`·`STRING`으로 의미와 저장값을 표현할 수 없는 DB 업무 코드를 enum과 Converter로 매핑 | [SKILL.md](database/jpa-coded-enum-mapping/SKILL.md) |
| `java-model-conventions` | `backend` | Entity 생성·변경 메서드와 DTO 표현·변환을 기존 Java 모델 관례에 맞게 작성 | [SKILL.md](backend/java-model-conventions/SKILL.md) |
| `java-api-validation-errors` | `backend` | 요청 DTO 검증·한글 메시지·도메인 예외를 공통 오류 응답 계약에 연결 | [SKILL.md](backend/java-api-validation-errors/SKILL.md) |
| `java-domain-api-structure` | `architecture` | 도메인별 Java API의 패키지·계층·App/Internal 진입점·후처리 책임 구성 | [SKILL.md](architecture/java-domain-api-structure/SKILL.md) |

Java 소스에 주석을 쓰는 작업은 `java-javadoc`, API 호출 계약을 설명하는 문서 작업은 `api-documentation`을 선택한다. Java로 구현된 API라는 이유만으로 두 스킬을 모두 읽지 않는다.

DB의 테이블·키·관계부터 정해야 하면 `etoos-db-modeling`, 정해진 모델의 SQL만 작성하면 `etoos-postgresql-ddl`을 선택한다. 설계 스킬은 최종 SQL 작성에 DDL 스킬을 함께 사용한다. 일반 조회 SQL 작성·성능 튜닝은 두 스킬의 주목적이 아니다.

조회 저장소를 구현할 때는 `querydsl-repository-conventions`, DB 업무 코드의 enum 매핑을 구현할 때는 `jpa-coded-enum-mapping`을 선택한다. SQL만 작성하는 요청에 Java 조회 구조를 추가하지 않는다. DB 값과 enum 상수명이 이미 일치하거나 기존 순번 계약으로 표현되는 경우에는 Converter 스킬의 적용 조건에 해당하지 않는다.

API 모듈의 경계·패키지부터 정할 때는 `java-domain-api-structure`, 개별 Entity·DTO를 작성할 때는 `java-model-conventions`, 요청 검증·오류 동작을 구현할 때는 `java-api-validation-errors`를 선택한다. Java API라는 이유만으로 관련 스킬을 모두 읽지 않는다.

**기준 상태:** 이투스 설계·DDL 스킬은 사용자 제공 모델링 가이드·용어사전·SQL 예제를 근거로 한다. Java 구현 스킬 5개와 기존 문서 스킬의 보강 내용은 `eci-my247-api`의 이상수 작성 이력에서 추출한 관례이며, 새 업무 요구사항이나 모든 프로젝트의 강제 규칙은 아니다. 2026-10-16 사용자가 7개 항목을 채택했고, Converter의 사전 조건과 enum 문서화 범위를 지정했다. 각 스킬의 참고 자료에 대표 커밋·현재 코드와 반례를 남겼다. 정적 소스 분석과 문서 검증은 실제 운영 동작 검증과 구분한다.

## 디렉토리 구조

```text
skills/
├── README.md                         # AI의 스킬 선택용 목록
├── MAINTENANCE.md                    # 사람의 유지보수·공통 사용 안내
├── _templates/
│   └── SKILL.template.md             # 새 스킬을 만들 때 복사할 양식
├── docs/                             # 문서화 카테고리
│   ├── java-javadoc/
│   │   ├── SKILL.md                  # JavaDoc 작성 절차
│   │   └── references/
│   │       └── type-and-layer-guidance.md # 유형·레이어별 작성 기준
│   └── api-documentation/
│       ├── SKILL.md                  # API 문서 작성 절차
│       └── references/              # 조건부 Swagger 작성 관례
├── architecture/
│   └── java-domain-api-structure/    # 도메인 계층·진입점·후처리 구성
├── backend/
│   ├── java-model-conventions/      # Entity·DTO 표현과 코드 서식
│   └── java-api-validation-errors/  # 요청 검증·업무 오류 표현
└── database/
    ├── querydsl-repository-conventions/ # 조회 저장소·결과 조립
    ├── jpa-coded-enum-mapping/       # 사전 조건에 따른 Converter 선택
    ├── etoos-db-modeling/
    │   └── SKILL.md                  # 업무에서 모델을 설계하는 절차
    └── etoos-postgresql-ddl/
        ├── SKILL.md                  # DBA 전달 SQL 작성 절차
        ├── scripts/
        │   └── lookup_terms.py       # 필요한 용어만 조회
        └── references/
            ├── standards.md         # 두 DB 스킬의 공통 규칙
            ├── source-notes.md      # 출처·자료 갱신 안내
            ├── source-guide.md      # 사용자 제공 가이드 원본 보존
            ├── etoos-terms.xdic      # 용어사전 원본 보존
            └── examples/            # 기존 업무 SQL 3개 보존
```

## 유지보수와 공통 사용

- 규칙 수정·스킬 추가·다른 프로젝트에서의 사용법: [MAINTENANCE.md](MAINTENANCE.md)
- 다른 PC에서 공통 스킬 연결: [프로젝트 루트의 SKILLS_SETUP.md](../SKILLS_SETUP.md)
- 새 스킬 양식: [_templates/SKILL.template.md](_templates/SKILL.template.md)
- 카테고리는 한 단계만 둔다. 예정 카테고리의 폴더는 실제 스킬을 추가할 때 만든다.

**사용자 전역 연결:** [설치 안내](../SKILLS_SETUP.md)에 따라 `~/.agents/skills/harness`를 이 저장소의 `skills/` 디렉토리 전체에 연결하면, 같은 사용자 계정의 다른 프로젝트에서도 스킬을 찾을 수 있다. 전체 폴더를 연결한 경우 새 카테고리와 유효한 `SKILL.md`를 추가해도 개별 연결은 필요하지 않다. 저장소를 내려받는 것만으로 전역 연결이 생성되지는 않는다.

스킬 추가 시 이 목록도 함께 갱신한다. 실행 중인 채팅에 즉시 반영되지 않으면 새 채팅을 시작하거나 Codex를 다시 시작한다. 다른 컴퓨터·원격 실행 환경은 별도로 연결해야 한다. 설정과 이전 절차는 [SKILLS_SETUP.md](../SKILLS_SETUP.md)를 참고한다.
