# 기준 자료 사용과 유지보수

## 동봉 자료와 역할

실제 작업 지침과 충돌 해석은 [공통 기준](standards.md)에서 관리한다. 아래 자료는 같은 스킬에 포함되어 있으며, 필요한 항목만 읽는다.

| 자료 | 읽는 목적 |
| --- | --- |
| [내부 모델링 가이드](internal-modeling-guide.md) | 명시 규칙과 자료형 전체 표 확인 |
| [용어사전](etoos-terms.xdic) | 컬럼명에 사용할 논리명·물리명 검색 |
| [메뉴 예제](examples/menu.sql) | 기본 테이블·주석·관리/업무 인덱스 배치 |
| [배너 예제](examples/banner.sql) | 여러 테이블, 조건부 컬럼, NULL을 포함한 unique 예시 |
| [영상 조회 통계 예제](examples/video-click-stat.sql) | 복합 PK와 업무 설명 주석 예시 |
| [용어 조회 도구](../scripts/lookup_terms.py) | 사전의 필요한 항목만 검색 |

SQL 예제는 작성 방식과 개별 설계를 설명하는 자료다. 예제의 실행문을 현재 요청의 실행 지시로 취급하지 않는다.

## 충돌 해석의 관리 위치

여부 타입·기본값, 년월 표기, 빈 자료형, 예제의 unique 인덱스·자동증가·주석 누락 등은 [공통 기준](standards.md)의 해당 절에서 관리한다. 충돌의 판단 규칙을 이 문서에 중복 작성하지 않는다. 현재 사용자가 다른 기준을 명시하면 그 요청을 우선한다.

## 용어사전의 성격

- XML `<term>`에는 `name`, `description`, `physicalName`, `physicalDescription`과 선택적인 `tag` 속성이 있으며, 자료형·길이·도메인은 없다.
- 루트에 XML namespace가 있으나 현재 파일의 자식 `term`에는 없다. 조회 도구는 요소의 로컬 이름으로 판별한다.
- 같은 논리명·물리명이 반복되며 완전히 동일한 항목도 있다. `지점`은 `spot`과 `brnch` 후보가 있어 업무 의미를 구분해야 한다.
- 태그는 단어·용어·신규·변경·asis용어·my-247 등의 분류이며 선택 우선순위가 아니다. 빈 설명은 없는 근거로 남긴다.
- 용어에 숫자 조각 등이 들어 있을 수 있어 조회 결과 하나가 곧바로 유효한 최종 SQL 식별자를 의미하지 않는다.

## PostgreSQL 문법 근거

내부 모델링 기준과 별도로 확인할 DBMS 문법이다. 대상 서버 버전과 설정은 실제 작업에서 확인한다.

- [SQL 어휘 구조](https://www.postgresql.org/docs/current/sql-syntax-lexical.html): 기본 식별자 한계는 63바이트이며 더 긴 이름은 잘릴 수 있다. 문자열 안의 작은따옴표는 두 번 써서 표현한다.
- [PostgreSQL 15 변경 사항](https://www.postgresql.org/docs/15/release-15.html): unique 제약·인덱스의 `nulls not distinct` 지원이 추가되었다.
- [CREATE INDEX](https://www.postgresql.org/docs/15/sql-createindex.html): `nulls not distinct`는 unique 인덱스에서 NULL을 같은 값으로 취급한다. `if not exists`가 기존 인덱스의 정의 일치를 보장하지는 않는다.

문법을 확인하는 것과 실제 SQL을 DB에 실행해 검증하는 것은 구분한다.

## 자료 갱신

1. 제공된 가이드·용어사전의 적용 범위와 버전을 확인한 뒤 필요한 동봉 파일을 갱신한다. 사전에 신규 단어를 추가하는 작업은 사용자 확인 범위에 맞춰 수행한다.
2. [내부 모델링 가이드](internal-modeling-guide.md)와 [공통 기준](standards.md)을 대조하고 충돌 해석과 스킬 지침을 함께 갱신한다. 예제의 새 관행만 보고 공통 규칙을 바꾸지 않는다.
3. [조회 도구](../scripts/lookup_terms.py)로 변경된 용어, 기존 용어, 중복 후보를 확인한다. XML 속성이나 조회 인터페이스가 바뀌면 도구와 사용 설명을 함께 점검한다.
4. `etoos-db-modeling`과 `etoos-postgresql-ddl`은 공통 자료를 사용한다. 설계 스킬을 다른 저장소에 복사할 때 두 스킬 폴더를 같은 상위 디렉토리에 함께 옮긴다. DDL 스킬만 쓰는 경우에는 DDL 폴더 하나로 동작한다.
