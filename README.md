# Harness 공통 스킬

여러 프로젝트에서 재사용할 Codex 작업 지침을 관리하는 저장소다. 스킬은 `skills/<카테고리>/<스킬명>/`에 두고, 실행에 필요한 참고 문서·스크립트·자산을 함께 보관한다.

## 처음 사용하기

1. 이 저장소 전체를 원하는 로컬 경로에 clone하거나 복사한다. 폴더 이름과 위치는 자유롭게 정할 수 있다.
2. [공통 스킬 연결 안내](SKILLS_SETUP.md)에 따라 현재 사용자의 Codex에 `skills/` 전체를 연결한다. Git clone만으로 전역 연결이 만들어지지는 않는다.
3. [스킬 목록](skills/README.md)에서 필요한 작업을 확인하고, 새 채팅에서 스킬이 인식되는지 확인한다.

설치를 Codex에 맡기려면 이 저장소에서 다음과 같이 요청한다.

```text
프로젝트 루트의 SKILLS_SETUP.md를 읽고 이 PC에 공통 스킬 연결을 설정해줘.
현재 저장소의 skills 전체를 사용자 전역 경로에 연결하고,
다른 프로젝트에서도 스킬이 인식되는지 확인해줘.
```

## 필요한 환경

- 로컬 스킬을 사용할 수 있는 Codex가 필요하다. 연결은 PC·사용자 계정마다 설정한다.
- Python은 DB 스킬의 용어 조회 도구를 실행할 때만 필요하다. 표준 라이브러리만 사용하며 별도의 패키지 설치는 필요하지 않다. Python 버전·OS별 명령 확인은 [설치 안내](SKILLS_SETUP.md#용어-조회용-python-확인)를 따른다.
- DB 용어사전·SQL 예제·Java 포맷터는 `skills/`에 포함되어 있다. 참고 자료에 기록된 원본 프로젝트를 별도로 내려받을 필요는 없다.

## 관리와 배포

| 경로 | 역할 |
| --- | --- |
| [SKILLS_SETUP.md](SKILLS_SETUP.md) | 최초 연결, 확인, 저장소 이동·연결 해제 안내 |
| [skills/README.md](skills/README.md) | 스킬 선택용 목록 |
| [skills/MAINTENANCE.md](skills/MAINTENANCE.md) | 스킬 추가·수정과 참고 자료 관리 |
| [backdata/README.md](backdata/README.md) | 자료 수집용 임시 폴더 안내. README 외 자료는 Git에서 제외 |
| `outputs/` | 로컬 작업 산출물. Git 배포와 스킬 설치 대상에서 제외 |

배포할 때는 `skills/` 아래의 `references/`, `scripts/`, `assets/`도 함께 포함한다. 특히 `etoos-db-modeling`은 형제 폴더인 `etoos-postgresql-ddl`의 자료를 사용하므로 두 폴더의 배치를 유지한다.

다른 PC에서는 저장소를 갱신한 뒤 해당 PC의 연결을 확인한다. clone 경로를 이동하면 전역 링크도 새 위치로 갱신해야 한다. 기존 연결을 확인하는 방법은 설치 안내를 따른다.
