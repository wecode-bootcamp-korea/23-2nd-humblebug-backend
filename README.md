# 험블벅 (텀블벅 클론코딩)

## Tango Plate Project Family

![Image from iOS](https://user-images.githubusercontent.com/8315252/131079623-28e4e6ff-aa57-46cd-a9ed-542c52a912ff.jpg)


- F.E<br>
  [황도윤](https://github.com/tec-motive) : 할배도윤 / 본투비리더<br>
  [김다슬](https://github.com/cocacollllla) : 실세다슬 / 험블벅 실력자이자 실세 눈치 챙겨 눈치<br>
  [김로운](https://github.com/lownk) : 갓기로운 / 살리고 살리고 분위기 살살 살리고<br>
  <br>
- B.E<br>
  [고유영](https://github.com/lunayyko) : 깃천유영 / 리베이스의 늪에서 다시 태어남 <br>
  [한상웅](https://github.com/tkddnd82) : 서윗상웅 / 침착하고 은근한 개그캐<br> 
  [최혜림](https://github.com/rimi0108) : 천재혜림 / 우분투 마스터<br> 
  <br>

## 험블벅이란?

- 크라우드펀딩 텀블벅 클론 프로젝트
- 개발은 초기 세팅부터 직접 구현했으며, 프론트와 백을 연결해 실제 사용 가능한 수준으로 개발했습니다.

### 개발 인원 및 기간

- 개발기간 : 2021/8/17 ~ 2021/8/31
- 개발 인원 : 프론트엔드 3명, 백엔드 3명

### 프로젝트 선정이유

- 디자인이 깔끔하고 크라우드 펀딩 프로젝트 CRUD와 후원 부분이 구현하면서 배울 점이 좋을 것 같아서 선정되었습니다.

## 적용 기술 및 구현 기능

### 적용 기술

> -Front-End : javascript, React.js framwork, sass<br>
> -Back-End : Python, Django web framework, MySQL, Bcrypt, pyjwt, AWS, S3<br>
> -Common : POSTMAN, RESTful API

### 구현 기능

#### 회원가입 / 로그인페이지

- 회원가입 / 로그인을 소셜 로그인(카카오) 통해 구현
  카카오 API 통한 access token을 통해 유저 정보 획득 뒤 다시 새로운 access_token 부여하여 유저 관리

#### 메인페이지, 프로젝트 더보기 리스트 페이지

- 카테고리별 분류 필터

#### 프로젝트 상세페이지

- 프로젝트 이름, 목표 후원 금액, 메인 이미지, 사용자 후원 금액과 목표 후원 금액 퍼센트 계산
- 각 프로젝트에 따른 옵션 후원
- 프로젝트 댓글 작성, 삭제 기능 구현

#### S3를 이용한 이미지 업로드
AWS 정책생성기를 활용하여 객체에 대한 엑세스 권한을 제공하는 버킷 정책 작성 <업로드 관련 사항 정리>
가상환경에 boto3, django-storages 설치
이때 setting.py 의 INSTALLED_APP 에 'storages'추가
파일과 텍스트를 multipart/form-data 형식으로 한번에 수신
request.FILES 를 통해 파일을,
request.POST 를 통해 텍스트를 수신
전달받은 파일은 랜덤한 값을 붙여 S3로 저장
전달받은 텍스트와 s3 에 저장한 파일의 url 을 테이블에 저장
이미지 수정시 S3 서버에서 이미지 삭제

#### 리팩토리 예정


#### 데이터 입력 및 배포
- RDS DB 통해 멤버 데이터베이스 일원화
- csv 파일 제작 후 api 구성하여 데이터 한 번에 입력
- AWS 배포 통한 데이터베이스 배포 완료

<br>

## Reference

- 이 프로젝트는 [텀블벅](https://www.tumblebug.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
