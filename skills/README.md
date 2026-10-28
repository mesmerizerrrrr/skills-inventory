# 공통 스킬 인벤토리

여러 프로젝트에서 재사용할 작업 지침의 원본을 관리한다. `카테고리/스킬명/SKILL.md` 구조로 관리하며, 파일명과 스킬 식별자는 영문으로, 설명과 지침은 한글로 작성한다.

현재 배포 파일과 작업 입력만으로 이해·적용·유지보수할 수 있는 인벤토리를 제공한다. 제작에 사용한 조사 이력·계정 정보·과거 대화는 포함하지 않는다. 필요한 규칙·예시·자료·도구를 내부에 두고 상대경로로 연결한다.

## AI가 읽는 순서

1. 아래 목록의 **카테고리와 적용할 작업**을 보고 현재 요청에 필요한 스킬만 선택한다. 맞는 스킬이 없으면 억지로 적용하지 않는다.
2. 선택한 스킬의 `SKILL.md`를 읽고 작업한다. 현재 요청 수행에 함께 필요한 경우에만 여러 스킬을 적용한다.
3. `references/`는 선택한 스킬에서 안내한 조건에 해당할 때만 읽는다. 모든 파일을 미리 읽지 않는다.
4. 스킬을 추가하거나 수정할 때는 [생성·유지보수 가이드](MAINTENANCE.md)의 독립 사용 원칙과 검증 기준, [생성 템플릿](_templates/SKILL.template.md)을 읽는다.

이 인벤토리는 작업 방법을 제공한다. 현재 사용자의 요청과 대상 프로젝트의 적용 지침을 먼저 확인하고, 충돌하는 내용이 있으면 그 우선순위와 실제 작업 범위에 맞춰 적용한다.

## 카테고리

| 카테고리 | 분류 기준 | 현재 상태 |
| --- | --- | --- |
| `docs` | 코드 주석, API 사용법 등 이미 정해진 내용을 설명하는 문서 작성 | 스킬 2개; JavaDoc·Swagger 관례 보강 |
| `database` | DB 모델링·DDL, 조회 저장소, 저장 코드와 Java 타입의 매핑 | 스킬 5개 |
| `backend` | 신규 서버 프로젝트 초기 구성, Java 구현 가독성·모델·요청 검증·업무 예외·테스트 작성 | 스킬 5개 |
| `frontend` | 화면·컴포넌트 구현, 상태 관리, 사용자 상호작용 | 예정: 아직 스킬과 폴더 없음 |
| `architecture` | 시스템·모듈의 경계, 책임, 의존 관계를 설계하고 결정 | 도메인별 Java API 구성 스킬 1개 |
| `git` | 버전 관리 작업과 커밋 메시지 작성 관례 | 커밋 메시지 스킬 1개 |

분류는 스킬의 **주목적**을 기준으로 한다. DB 설계는 `database`, DB API의 사용 문서 작성은 `docs`에 둔다. 여러 분야에 걸쳐도 스킬은 한 곳에서 관리하며 관련 분야는 적용 조건에 적는다. 새 작업군이 생기면 카테고리를 추가할 수 있다.

## 스킬 목록

카테고리는 관리용 구분이다. AI는 이 목록에서 필요한 진입 파일로 바로 이동하며, 카테고리 안의 모든 스킬을 읽지 않는다.

| 스킬 | 카테고리 | 적용할 작업 | 진입 파일 |
| --- | --- | --- | --- |
| `java-javadoc` | `docs` | Java 클래스·인터페이스·enum·메서드의 JavaDoc 작성 또는 수정 | [SKILL.md](docs/java-javadoc/SKILL.md) |
| `api-documentation` | `docs` | 호출자가 사용할 API 명세·사용법·요청/응답·오류 문서 작성 또는 수정 | [SKILL.md](docs/api-documentation/SKILL.md) |
| `etoos-db-modeling` | `database` | 이투스 업무 요구사항을 테이블·컬럼·키·논리 관계로 설계하고 DBA 전달 SQL 작성 | [SKILL.md](database/etoos-db-modeling/SKILL.md) |
| `etoos-postgresql-ddl` | `database` | 확정된 설계를 이투스 규칙의 PostgreSQL DDL `.sql`로 작성·수정·검토 | [SKILL.md](database/etoos-postgresql-ddl/SKILL.md) |
| `querydsl-repository-conventions` | `database` | QueryDSL 조회 저장소·결과 조립을 구현하고 projection·체인 줄바꿈 적용 | [SKILL.md](database/querydsl-repository-conventions/SKILL.md) |
| `eci-querydsl-repository-support` | `database` | ECI의 QueryDSL CustomRepository 구현체에서 준비된 공통 support를 상속하고 초기화 재사용 | [SKILL.md](database/eci-querydsl-repository-support/SKILL.md) |
| `jpa-coded-enum-mapping` | `database` | `ORDINAL`·`STRING`으로 의미와 저장값을 표현할 수 없는 DB 업무 코드를 enum과 Converter로 매핑 | [SKILL.md](database/jpa-coded-enum-mapping/SKILL.md) |
| `java-model-conventions` | `backend` | Entity 생성·변경 메서드와 DTO 표현·변환을 기존 Java 모델 관례에 맞게 작성 | [SKILL.md](backend/java-model-conventions/SKILL.md) |
| `java-code-readability` | `backend` | Java 클래스의 주입 필드·공개 메서드 배치·빈 줄과 구현 구간·주석·줄바꿈·지역변수 기준 적용 | [SKILL.md](backend/java-code-readability/SKILL.md) |
| `java-api-validation-errors` | `backend` | 요청 DTO 검증·한글 메시지·도메인 예외를 공통 오류 응답 계약에 연결 | [SKILL.md](backend/java-api-validation-errors/SKILL.md) |
| `java-test-conventions` | `backend` | 메소드·분기별 유닛 테스트, 기능별 fixture, 테스트 전용 설정과 Repository 한정 H2 DB 검증 | [SKILL.md](backend/java-test-conventions/SKILL.md) |
| `spring-boot-project-bootstrap` | `backend` | 버전 확인부터 신규 Spring Boot API의 빌드·보안·Jackson·공통 응답/예외·선택 DB 기반 초기 생성 | [SKILL.md](backend/spring-boot-project-bootstrap/SKILL.md) |
| `java-domain-api-structure` | `architecture` | 기존 패키지 스타일 선택, 도메인 Service·BridgeService 의존 방향과 순환 의존 해소, 생성자 주입·트랜잭션 기준 | [SKILL.md](architecture/java-domain-api-structure/SKILL.md) |
| `git-commit-conventions` | `git` | 한글 Conventional Commits 메시지 작성·추천·검토와 티켓 표기 적용 | [SKILL.md](git/git-commit-conventions/SKILL.md) |

Java 소스의 JavaDoc을 쓰는 작업은 `java-javadoc`, API 호출 계약을 설명하는 문서 작업은 `api-documentation`을 선택한다. Java로 구현된 API라는 이유만으로 두 스킬을 모두 읽지 않는다.

Java 클래스를 생성하거나 멤버 배치·메서드·생성자의 구현을 작성·수정할 때는 `java-code-readability`를 적용한다. 클래스의 주입 필드·공개 메서드 배치·빈 줄과 내부 처리 구간의 `//` 주석·지역변수 기준을 담당한다. QueryDSL projection·체인의 구체적인 서식은 `querydsl-repository-conventions`에서 관리하며, JavaDoc만 수정할 때 구현 포맷 변경까지 추가하지 않는다.

Java 테스트 코드를 작성·수정할 때는 `java-test-conventions`를 선택한다. 일반 계층의 메소드·분기별 유닛 테스트와 Repository 계층에 한정한 실제 DB 검증을 다룬다. 테스트의 구간 주석·fixture·환경설정 위치는 이 전용 스킬에서 관리한다.

DB의 테이블·키·관계부터 정해야 하면 `etoos-db-modeling`, 정해진 모델의 SQL만 작성하면 `etoos-postgresql-ddl`을 선택한다. 설계 스킬은 최종 SQL 작성에 DDL 스킬을 함께 사용한다. 일반 조회 SQL 작성·성능 튜닝은 두 스킬의 주목적이 아니다.

조회 저장소를 구현할 때는 `querydsl-repository-conventions`, DB 업무 코드의 enum 매핑을 구현할 때는 `jpa-coded-enum-mapping`을 선택한다. SQL만 작성하는 요청에 Java 조회 구조를 추가하지 않는다. DB 값과 enum 상수명이 이미 일치하거나 기존 순번 계약으로 표현되는 경우에는 Converter 스킬의 적용 조건에 해당하지 않는다.

ECI 프로젝트에서 QueryDSL을 사용하는 CustomRepository 구현체를 생성·수정할 때는 `eci-querydsl-repository-support`도 적용한다. 프로젝트에 준비된 공통 support의 상속·초기화 규칙을 담당하며, support가 없으면 이 전용 규칙은 적용하지 않는다. 일반 조회 결과 조립 규칙은 `querydsl-repository-conventions`에서 관리한다.

API 모듈의 경계·패키지부터 정할 때는 `java-domain-api-structure`, 개별 Entity·DTO를 작성할 때는 `java-model-conventions`, 요청 검증·오류 동작을 구현할 때는 `java-api-validation-errors`를 선택한다. Java API라는 이유만으로 관련 스킬을 모두 읽지 않는다.

신규 Spring Boot API 프로젝트의 빌드·실행 골격과 공통 설정을 처음 준비할 때는 `spring-boot-project-bootstrap`을 선택한다. Spring Boot·JDK 버전이 미지정이면 먼저 확인하며, 기존 프로젝트의 기능 추가·설정 유지보수·버전 업그레이드만 하는 요청에는 적용하지 않는다.

Java 도메인의 디렉토리를 새로 만들거나 이동·이름 변경할 때는 `java-domain-api-structure`의 [스타일 선택 절차](architecture/java-domain-api-structure/SKILL.md#디렉토리-생성변경-전-스타일-선택)를 적용한다. 기존 디렉토리 안의 파일만 수정하는 작업에 전체 구조 재검토를 추가하지 않는다.

Service 클래스를 새로 만들 때는 `java-domain-api-structure`의 [신규 Service 생성자 주입](architecture/java-domain-api-structure/SKILL.md#신규-service-생성자-주입)을 적용한다. DB에 접근하는 Service를 새로 만들거나 트랜잭션을 조정하면 [Service 트랜잭션과 readOnly](architecture/java-domain-api-structure/SKILL.md#service-트랜잭션과-readonly)도 적용한다. QueryDSL 조회 호출부에서도 필요한 절을 참조하며, 단순 Service 추가·트랜잭션 변경에 전체 도메인 구조 규칙을 적용하지 않는다.

Service를 새로 만들거나 서비스 간 의존 관계를 변경할 때는 [Service 의존 방향과 BridgeService](architecture/java-domain-api-structure/SKILL.md#service-의존-방향과-bridgeservice)를 적용한다. 도메인 조합과 순환 의존을 다루면 해당 절에서 연결한 상세 기준·예시를 함께 읽는다.

커밋 메시지를 추천·검토하거나 실제 커밋 요청을 수행할 때는 `git-commit-conventions`를 선택한다. 코드 구현이나 PR 설명 작성만 요청받은 경우에는 자동으로 커밋 작업을 추가하지 않는다.

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
│   └── java-domain-api-structure/    # 도메인 계층·BridgeService·진입점·후처리 구성
├── backend/
│   ├── java-model-conventions/      # Entity·DTO 표현과 IDE 서식 자산
│   ├── java-code-readability/       # 클래스 배치·빈 줄·구간·지역변수 기준
│   ├── java-api-validation-errors/  # 요청 검증·업무 오류 표현
│   ├── java-test-conventions/       # 메소드·분기별 테스트와 Repository H2 검증
│   └── spring-boot-project-bootstrap/ # 버전 확인·신규 프로젝트 공통 기반 생성
├── git/
│   └── git-commit-conventions/      # 한글 커밋 메시지와 티켓 표기
└── database/
    ├── querydsl-repository-conventions/ # 조회 저장소·결과 조립
    ├── eci-querydsl-repository-support/ # ECI 공통 support 상속·초기화
    ├── jpa-coded-enum-mapping/       # 사전 조건에 따른 Converter 선택
    ├── etoos-db-modeling/
    │   └── SKILL.md                  # 업무에서 모델을 설계하는 절차
    └── etoos-postgresql-ddl/
        ├── SKILL.md                  # DBA 전달 SQL 작성 절차
        ├── scripts/
        │   └── lookup_terms.py       # 필요한 용어만 조회
        └── references/
            ├── standards.md         # 두 DB 스킬의 공통 규칙
            ├── reference-maintenance.md # 자료 구조·갱신 안내
            ├── internal-modeling-guide.md # 내부 모델링 규칙
            ├── etoos-terms.xdic      # 명명에 사용하는 용어사전
            └── examples/            # DDL 작성 예시
```

## 유지보수와 공통 사용

- 규칙 수정·스킬 추가·다른 프로젝트에서의 사용법: [MAINTENANCE.md](MAINTENANCE.md)
- 다른 PC에서 공통 스킬 연결: [프로젝트 루트의 SKILLS_SETUP.md](../SKILLS_SETUP.md)
- 새 스킬 양식: [_templates/SKILL.template.md](_templates/SKILL.template.md)
- 카테고리는 한 단계만 둔다. 예정 카테고리의 폴더는 실제 스킬을 추가할 때 만든다.

**사용자 전역 연결:** [설치 안내](../SKILLS_SETUP.md)에 따라 `~/.agents/skills/harness`를 이 저장소의 `skills/` 디렉토리 전체에 연결하면, 같은 사용자 계정의 다른 프로젝트에서도 스킬을 찾을 수 있다. 전체 폴더를 연결한 경우 새 카테고리와 유효한 `SKILL.md`를 추가해도 개별 연결은 필요하지 않다. 저장소를 내려받는 것만으로 전역 연결이 생성되지는 않는다.

스킬 추가 시 이 목록도 함께 갱신한다. 실행 중인 채팅에 즉시 반영되지 않으면 새 채팅을 시작하거나 Codex를 다시 시작한다. 다른 컴퓨터·원격 실행 환경은 별도로 연결해야 한다. 설정과 이전 절차는 [SKILLS_SETUP.md](../SKILLS_SETUP.md)를 참고한다.
