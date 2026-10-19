# 출처·충돌 해석·자료 관리

## 보존한 자료

2026-10-16 사용자가 제공한 이투스 DB 모델링 가이드와 가이드가 직접 참조하는 자료를 아래 위치에 원본 바이트 그대로 복사했다. 원문은 근거 보존용이며 실제 작업 지침은 [공통 기준](standards.md)에서 관리한다.

| 원래 파일명 | 보존 위치 | 읽는 목적 |
| --- | --- | --- |
| 이투스 DB 모델링 가이드.md | [source-guide.md](source-guide.md) | 명시 규칙·자료형 전체 표·해석 근거 확인 |
| ETOOS_용어사전_MY247_20251114.xdic | [etoos-terms.xdic](etoos-terms.xdic) | 컬럼명에 사용할 논리명·물리명 검색 |
| 260730-my247전용메뉴.sql | [examples/menu.sql](examples/menu.sql) | 기본 테이블·주석·관리/업무 인덱스 배치 |
| 260731-배너.sql | [examples/banner.sql](examples/banner.sql) | 여러 테이블, 조건부 컬럼, NULL을 포함한 unique 예시 |
| 260805-모의고사 해설영상 통계.sql | [examples/video-click-stat.sql](examples/video-click-stat.sql) | 복합 PK와 업무 설명 주석 예시 |

원래 위치는 저장소의 `backdata/이투스_DBA_guiade/`였다. `backdata/README.md`는 이 위치를 삭제될 수 있는 임시 자료 폴더로 설명하므로 스킬의 실행 의존성으로 삼지 않는다. 원문에 남은 절대 경로는 당시의 출처 표기이며 현재 참조 경로가 아니다. 자료 보존을 이유로 `backdata`를 삭제할 필요는 없다.

## 충돌 해석의 관리 위치

여부 타입·기본값, 년월 표기, 빈 자료형, 예제의 unique 인덱스·자동증가·주석 누락 등은 [공통 기준](standards.md)의 해당 절에서 원문 근거와 함께 관리한다. 충돌의 판단 규칙을 이 문서에 중복 작성하지 않는다. 현재 사용자가 다른 기준을 명시하면 그 요청을 우선한다.

## 용어사전의 성격

- XML `<term>` 8,756개가 들어 있다. `name`, `description`, `physicalName`, `physicalDescription`과 선택적인 `tag` 속성이 있으며, 자료형·길이·도메인은 없다.
- 루트에 XML namespace가 있으나 현재 파일의 자식 `term`에는 없다. 조회 도구는 요소의 로컬 이름으로 판별한다.
- 같은 논리명·물리명이 반복되며 완전히 동일한 항목도 있다. `지점`은 `spot`과 `brnch` 후보가 있어 업무 의미를 구분해야 한다.
- 태그는 단어·용어·신규·변경·asis용어·my-247 등의 분류이며 선택 우선순위가 아니다. 빈 설명은 없는 근거로 남긴다.
- 용어에 숫자 조각 등이 들어 있을 수 있어 조회 결과 하나가 곧바로 유효한 최종 SQL 식별자를 의미하지 않는다.

## PostgreSQL 문법 근거

2026-10-16 공식 문서에서 확인한 보완 사항이다. 대상 서버 버전과 설정은 실제 작업에서 별도로 확인한다.

- [SQL 어휘 구조](https://www.postgresql.org/docs/current/sql-syntax-lexical.html): 기본 식별자 한계는 63바이트이며 더 긴 이름은 잘릴 수 있다. 문자열 안의 작은따옴표는 두 번 써서 표현한다.
- [PostgreSQL 15 변경 사항](https://www.postgresql.org/docs/15/release-15.html): unique 제약·인덱스의 `nulls not distinct` 지원이 추가되었다.
- [CREATE INDEX](https://www.postgresql.org/docs/15/sql-createindex.html): `nulls not distinct`는 unique 인덱스에서 NULL을 같은 값으로 취급한다. `if not exists`가 기존 인덱스의 정의 일치를 보장하지는 않는다.

이 문법 확인은 실제 SQL 예제나 신규 DDL을 DB에 실행해 검증했다는 뜻이 아니다.

## 자료 갱신

1. 새 가이드·용어사전의 출처와 기준일을 확인하고 해당 보존 파일을 교체한다. 사전에 신규 단어를 추가하는 작업은 사용자 확인 범위에 맞춰 수행한다.
2. 원문과 [standards.md](standards.md)를 대조하고 충돌 표와 스킬 지침을 함께 갱신한다. 예제의 새 관행만 보고 공통 규칙을 바꾸지 않는다.
3. [조회 도구](../scripts/lookup_terms.py)로 변경된 용어, 기존 용어, 중복 후보를 확인한다. 사전 버전이나 항목 수가 바뀌면 이 문서의 수치도 갱신한다.
4. `etoos-db-modeling`과 `etoos-postgresql-ddl`은 공통 자료를 사용한다. 설계 스킬을 다른 저장소에 복사할 때 두 스킬 폴더를 같은 상위 디렉토리에 함께 옮긴다. DDL 스킬만 쓰는 경우에는 DDL 폴더 하나로 동작한다.
