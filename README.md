# Bulletin Board

## 어플리케이션 실행 방법

1. `git`과 `Docker`, `Docker Compose`를 설치합니다.
    - [git 설치 가이드 url](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%84%A4%EC%B9%98)
    - [Docker 설치 가이드 url](https://docs.docker.com/engine/install/)
    - [Docker Compose 설치 가이드 url](https://docs.docker.com/compose/install/)
2. 해당 레포지토리를 클론합니다.
    ```bash
     $ git clone https://github.com/Pre-Onboarding-Listerine/aimmo-assignment-team-1.git
    ```
3. 레포지토리를 클론한 위치에서 도커 컨테이너를 빌드하고 실행합니다.
    ```bash
    $ docker-compose up
    ```
4. `http://localhost:8000` 이후에 아래 Endpoint를 추가해 api를 호출합니다.

### 완료된 시스템이 배포된 서버의 주소

```commandline
    ec2-13-125-235-63.ap-northeast-2.compute.amazonaws.com
```

## 구현 방법

`django` 프레임워크와 `mongodb`를 사용해 구현하였습니다.

프로젝트의 구성은 `poetry`를 사용해 패키지 의존성을 관리하였고 `docker`를 이용해 프로젝트의 빌드 및 배포를 단순환하였습니다.

프로젝트의 구조는 `django`의 프로젝트 구조를 따르고 있습니다.
- `bulletin`: bulletin board라는 게시판 프로젝트의 구체적인 설정 파일 및 각 앱으로의 요청 라우팅 역할을 맡습니다.
- `member`: 게시판의 회원에 대한 요청을 처리합니다.
- `post`: 게시글에 대한 조작 요청을 처리합니다.
- `security`: 인증 및 인가와 관련된 요청을 처리합니다.

각 app에서 각 함수 및 메소드들을 `tests` 디렉토리의 테스트들로 유닛테스트를 실행할 수 있습니다. 

### Layered Architecture

각 app들은 `views-service-models`의 계층을 갖고 있습니다. 
또한, 각 app들은 컴포넌트끼리 데이터를 전달 및 도메인의 노출을 방지하기 위한 `dto`를 보유하고 있습니다.

그래서 각 계층은 다음과 같은 책임을 맡습니다.
- `views`: 전통적인 Layered Architecture의 presentation layer의 역할을 맡아 엔드포인트로 들어온 요청을 정제하여 알맞은 서비스에 전달합니다.
- `service`: view layer로부터 전달받은 요청을 처리하는 비즈니스 로직을 포함하고 있습니다.
- `models`: 비즈니스 로직 연산을 통한 결과물을 데이터 베이스에 반영하기 위한 코드를 포함하고 있습니다.

## Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법


