# 두 가지 패키지 스타일

Java 도메인의 디렉토리를 생성·변경할 때 [스타일 선택 절차](../SKILL.md#디렉토리-생성변경-전-스타일-선택)에 따라 읽는다. 아래 구조는 역할별 배치 예시다. 필요한 파일이 생길 때만 디렉토리를 만들고, 대상 프로젝트의 기존 하위 경로·단복수를 우선한다.

## presentation/application/infrastructure 스타일

Controller와 DTO를 `presentation`, 서비스와 업무 모델을 `application`, DB 저장소를 `infrastructure`에 배치하는 프로젝트에서 선택한다.

```text
<domain>/
├── presentation/
│   ├── <Domain>Controller.java
│   └── dto/
│       ├── request/<Domain>CreateRequest.java
│       └── response/<Domain>Dto.java
├── application/
│   ├── domain/<Domain>Entity.java
│   └── service/
│       ├── <Domain>Service.java
│       └── impl/<Domain>ServiceImpl.java
└── infrastructure/
    ├── <Domain>Repository.java
    ├── <Domain>CustomRepository.java
    └── impl/<Domain>CustomRepositoryImpl.java
```

- API 진입점과 DTO의 소유 업무를 함께 유지한다. 기능별 하위 패키지가 이미 있으면 그 경계를 이어 쓰며, DTO를 `presentation/dto` 바로 아래 두는 도메인에 `request`·`response` 분리를 강제하지 않는다.
- Entity는 `application/domain` 배치를 따르되, 기존 도메인이 최상위 `domain`을 사용하면 그대로 유지한다. 클래스의 `Entity` 접미사도 기존 명명을 따른다.
- 업무 enum·조회 VO·이벤트·업무 예외가 필요하면 각각 `application/enums`, `application/vo`, `application/event`, `application/exception` 또는 `application/exceptions`의 기존 배치를 따른다. 이름만 보고 모든 타입에 하위 패키지를 만드는 규칙은 아니다.
- 합성 Swagger 어노테이션과 문서용 응답을 분리하는 도메인은 `presentation/swagger/annotation`·`response` 또는 `annotations`·`responses`의 기존 단복수를 유지한다.
- 도메인 주 서비스의 인터페이스와 구현을 `application/service`와 `application/service/impl`에 둔다. 기존 이벤트 처리 전담 서비스가 단일 클래스이면 별도 인터페이스나 `listener` 디렉토리를 추가하지 않는다.

## controller/service/repository 스타일

Controller·서비스·DB 저장소를 `controller`·`service`·`repository`로 구분하고, DTO는 `domain`, JPA Entity는 `entity`에 두는 프로젝트에서 선택한다.

```text
<domain>/
├── controller/<Domain>Controller.java
├── service/
│   ├── <Domain>Service.java
│   └── impl/<Domain>ServiceImpl.java
├── domain/
│   ├── request/<Domain>CreateRequest.java
│   └── response/<Domain>Dto.java
├── entity/<Domain>Entity.java
├── enums/<Domain>Status.java
└── repository/
    ├── <Domain>Repository.java
    ├── <Domain>CustomRepository.java
    └── impl/<Domain>CustomRepositoryImpl.java
```

- 이 스타일의 `domain/request`·`domain/response`는 요청·응답 모델이다. 다른 스타일의 `application/domain`과 이름이 비슷하다는 이유로 Entity 위치로 해석하지 않는다. `domain/dto` 등 기존 모델 구분도 유지한다.
- 업무 enum과 조회 보조 객체는 기존 `enums`·`vo` 배치를 따른다. Entity의 클래스명과 `Entity` 접미사도 인접 코드에 맞춘다.
- 저장소는 다음 변형 중 대상 도메인의 배치를 유지한다. 새 도메인은 같은 모듈의 관련 도메인에 맞춘다. 어느 변형이 더 최신이라는 이유만으로 전체 프로젝트의 표준으로 단정하지 않는다.

  | 기존 저장소 배치 | JPA Repository | CustomRepository | 조회 구현 |
  | --- | --- | --- | --- |
  | `repository` | `repository` | `repository` | `repository/impl` |
  | `custom` 하위 구분 | `repository` | `repository/custom` | `repository/custom/impl` |
  | `dataprovider/db` | `dataprovider/db` | `dataprovider/db` | `dataprovider/db/impl` |

- 서비스에 업무별 분리가 이미 있으면 `service/core`·`service/core/impl`, `service/statistics`·`service/statistics/impl`처럼 해당 경계를 유지한다. 작은 기능에 같은 분리를 미리 만들지 않는다.
- 외부 API 클라이언트와 전용 요청·응답을 `dataprovider/api`·`dataprovider/api/dto/request`·`response`에 두는 도메인은 그 경계를 유지한다. 외부 통신용 DTO를 Controller의 `domain/request`·`response`와 같은 역할로 취급하지 않는다.
- 기존 JPA Converter가 도메인의 `converter`에 있으면 그 위치를 사용한다. Swagger를 Controller의 어노테이션과 `constants`의 설명 상수로 관리하면 해당 방식을 유지한다. 다른 스타일의 `infrastructure/converter`·`presentation/swagger`를 자동 추가하지 않는다.
- 이벤트·예외 등 위 예시에 없는 역할은 대상 프로젝트의 같은 역할을 찾아 위치를 정한다. 첫 번째 스타일의 `application` 하위 경로를 그대로 도입하거나 확인하지 않은 대응 경로를 만들어 내지 않는다.
- `infrastructure`가 외부 HTTP 클라이언트에 사용되는 도메인도 있다. DB 저장소와 외부 연동의 역할을 실제 코드로 구분하며, `infrastructure`라는 이름만 보고 `repository`로 이동하지 않는다.

## BridgeService 배치

[BridgeService 생성 조건](bridge-services.md#생성-여부-판단)에 해당할 때만 적용한다. Bridge는 논리적으로 도메인 Service보다 상위에서 조합을 맡지만, 물리적인 디렉토리 깊이가 계층을 결정하지는 않는다.

| 선택한 스타일 | 기존 Bridge 배치가 없을 때의 위치 |
| --- | --- |
| `presentation/application/infrastructure` | `<업무 소유 도메인>/application/service/bridge/<업무명>BridgeService.java` |
| `controller/service/repository` | `<업무 소유 도메인>/service/bridge/<업무명>BridgeService.java` |

- 기존에 같은 조합 역할의 배치가 있으면 그 위치를 따른다. 위 표는 새 역할의 위치가 필요할 때 쓰는 기준이며 기존 파일의 일괄 이동을 요구하지 않는다.
- 단일 `@Service` 클래스로 둘 수 있으므로 Bridge 전용 인터페이스와 `impl` 디렉토리를 미리 만들지 않는다. 기존 Interface/Impl 쌍은 이 허용 규칙만으로 제거하지 않는다.
- Bridge는 업무를 소유한 도메인 또는 기존 업무 흐름 모듈에 둔다. 조합 대상이 여러 도메인이라는 이유로 전역 `bridge`·`commons`에 모으지 않는다.

## 적용 예시와 확인

| 현재 작업 입력 | 적용할 배치 |
| --- | --- |
| 인접 도메인이 `presentation`, `application/service`, `infrastructure`를 사용하며 새 일정 도메인을 추가 | 첫 번째 스타일을 선택하고 일정에 필요한 Controller·DTO·Service·Repository만 구성 |
| 등록 업무가 여러 도메인 Service를 조합하고 기존 구조가 `controller/service/repository`이며 Bridge 위치는 없음 | 등록 업무 소유 도메인의 `service/bridge/RegistrationBridgeService.java`에 단일 클래스를 배치 |
| 인접 도메인이 `controller`, `service/impl`, `entity`, `domain/request`, `repository/impl`을 사용하며 새 일정 도메인을 추가 | 두 번째 스타일을 선택하고 같은 역할의 디렉토리명을 유지 |
| 기존 영상 도메인이 `controller`, `service/core`, `dataprovider/db/impl`을 사용하며 조회 구현을 추가 | 두 번째 스타일의 기존 변형에 추가; `repository/impl`을 새로 만들지 않음 |
| 기존 응답 DTO가 `presentation/dto` 바로 아래 있으며 응답 하나를 추가 | 같은 위치에 추가; 예시의 `response` 디렉토리를 만들기 위해 기존 DTO를 이동하지 않음 |

변경한 각 파일의 역할과 실제 `package`·import를 대조한다. 요청·응답 DTO와 Entity를 `domain`이라는 이름만으로 혼동하지 않았는지, 같은 역할의 디렉토리를 중복 생성하지 않았는지 확인한다. 이름 변경이 필요한 작업이면 사용처와 스캔 설정을 함께 확인하며, 단순한 스타일 선택을 서비스 책임이나 런타임 동작 변경으로 확대하지 않는다.
