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
4. `http://localhost` 이후에 아래 Endpoint를 추가해 api를 호출합니다.

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

## Layered Architecture

각 app들은 `views-service-models`의 계층을 갖고 있습니다. 
또한, 각 app들은 컴포넌트끼리 데이터를 전달 및 도메인의 노출을 방지하기 위한 `dto`를 보유하고 있습니다.

그래서 각 계층은 다음과 같은 책임을 맡습니다.
- `views`: 전통적인 Layered Architecture의 presentation layer의 역할을 맡아 엔드포인트로 들어온 요청을 정제하여 알맞은 서비스에 전달합니다.
- `service`: view layer로부터 전달받은 요청을 처리하는 비즈니스 로직을 포함하고 있습니다.
- `models`: 비즈니스 로직 연산을 통한 결과물을 데이터 베이스에 반영하기 위한 코드를 포함하고 있습니다.

## Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법

### Endpoints

- 회원가입: `POST /members`
- 로그인: `POST /security`
- 게시물 작성 post: `POST /posts`
- 게시물 수정 patch: `PATCH /posts`
- 게시물 삭제 delete: `DELETE /posts`
- 게시물 확인 get: `GET /posts/<post_id>`
- 게시물 리스트 get: `GET /posts/postings`

## 회원가입

### request

```http request
POST /members
Content-Type: application/json
```

#### request json body

```json
{
   "username": "asd",     // 회원명을 의미하며 중복될 수 없습니다.
   "password": "123qwer"  // 비밀번호를 의미합니다.
}
```

### response

#### 성공시

```bash
response status: 201 Created
```
#### 실패시

```bash
# 유저명이 중복될 경우
response status: 409 Conflict
```

## 로그인

### request

```http request
POST /security
Content-Type: application/json
```

#### request json body

```json
{
   "username": "asd",     // 회원명을 의미하며 중복될 수 없습니다.
   "password": "123qwer"  // 비밀번호를 의미합니다.
}
```

### response

#### 성공시

```bash
response status: 200 OK
response content {"access_token": <Bearer JWT>}
```

#### 실패시

```bash
# 입력한 유저명을 찾을 수 없는 경우
response status: 404 NotFound

# 비밀번호가 맞지 않을 경우
response statue: 401 Unauthorized

```

## 게시물 작성

### request

```http request
POST /posts
Authorization: <Bearer JWT>
Content-Type: application/json
```

#### request json body

```json
{
   "title": "json title",     // 게시글의 제목을 의미합니다.
   "content": "json content", // 게시글의 내용을 의미합니다.
   "category": "json"         // 게시글의 카테고리를 의미합니다.
}
```

### response

#### 성공시

```bash
response status: 201 Created
```

#### 실패시

```bash
response status: 401 Unauthorized
```

## 게시물 수정

### request

```http request
PATCH /posts
Authorization: <Bearer JWT>
Content-Type: application/json
```

#### request json body

```json
{
   "id": 1,                   // 수정할 게시물의 식별자를 의미합니다.
   "title": "json title",     // 게시물의 제목의 해당 아이템의 value로 수정됩니다.
   "content": "json content"  // 게시물의 내용이 해당 아이템의 value로 수정됩니다.
}
```

### response

#### 성공시

```bash
response status: 200 OK
```
#### 실패 시 

```bash
# 수정할 게시물을 찾지 못했을 때
response status: 404 NotFound

# 사용자 인증이 되지 않았을 때
response status: 401 Unauthorized
```

## 게시물 삭제

### request 예시

```http request
DELETE /posts
Authorization: <Bearer JWT>
Content-Type: application/json
```

#### request json body

```json
{
    "id"; 1   // 삭제할 게시물의 식별자를 의미합니다.
}
```

### response

#### 성공시

```bash
response status: 204 No Content
```
#### 실패 시 

```bash
# 게시물을 찾지 못했을 경우
response status: 404 NotFound

# 인증 되지 않은 요청일 경우
response status: 401 Unauthorized
```

## 게시물 확인

### request

```http request
GET /posts/<post_id>
Authorization: <Bearer JWT>  (Optional)
```

### response

#### 성공시

```bash
response status: 200 OK
response content:
{
  "id": 1,
  "author": "이지은",
  "title": "before title",
  "content": "before content",
  "category": "before",
  "created_at": "01-11-2021 09:10:32",
  "updated_at": "02-11-2021 09:10:44",
  "hits": 3
}
```

#### 실패 시 

```bash
# 게시물을 찾지 못했을 경우
response status: 404 NotFound
```

## 게시물 리스트

### request

```http request
GET /posts/postings?limit=3&offset=0&category=java&keyword=annotations
```

#### request query params

```bash
offset    # 가져오려는 게시글의 시작 순번을 의미합니다.
limit     # 한 페이지에 최대로 가져올 수 있는 게시글의 수를 의미합니다.
category  # 가져오고 싶은 게시글들의 카테고리를 의미합니다. (카테고리 기능)
keyword   # 게시글의 내용이 포함하고 있는 단어를 의미합니다. (단어 검색 기능)
```

### response

#### 성공시
```bash
response status: 200 OK
response content:
[
   {
     "id": 1,
     "author": "이지은",
     "title": "before title",
     "content": "before content annotations",
     "category": "java",
     "created_at": "01-11-2021 09:10:32",
     "updated_at": "02-11-2021 09:10:32",
     "hits": 3
   },
   {
     "id": 1,
     "author": "이지은",
     "title": "after title",
     "content": "after content annotations",
     "category": "java",
     "created_at": "01-11-2021 09:10:32",
     "updated_at": "02-11-2021 09:10:32",
     "hits": 4
   },
   {
     "id": 1,
     "author": "이지은",
     "title": "after title",
     "content": "later content annotations",
     "category": "java",
     "created_at": "01-11-2021 09:10:32",
     "updated_at": "02-11-2021 09:10:32",
     "hits": 2
   }
]
```
