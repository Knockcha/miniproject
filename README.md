# Mini Web Application

Flask, HTML/JavaScript, MySQL, and Docker based starter project.

## Stack

- Backend: Flask
- Frontend: HTML, CSS, Vanilla JavaScript
- Database: MySQL 8
- Runtime: Docker Compose

## Run

1. Copy `.env.example` to `.env`
2. Start services:

```bash
docker compose up --build
```

3. Open `http://localhost:5000`

## Structure

```text
app/
  static/
    css/
    js/
  templates/
  __init__.py
  config.py
  db.py
  routes.py
database/
  init/
app.py
Dockerfile
docker-compose.yml
requirements.txt
```

 ## DataBase - 테이블 생성 
```sql
 CREATE TABLE TB_CS_MEMBERS (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,              -- 회원 고유 ID
    username VARCHAR(50) NOT NULL UNIQUE,              -- 로그인 아이디
    password VARCHAR(255) NOT NULL,                    -- 암호화된 비밀번호
    email VARCHAR(100) NOT NULL UNIQUE,                -- 이메일 (중복 방지)
    phone VARCHAR(20) UNIQUE,                          -- 휴대폰 번호
    -- nickname VARCHAR(50),                              -- 서비스 내 표시 이름
    birthdate DATE,                                    -- 생년월일
    gender ENUM('male','female','other') DEFAULT 'other', -- 성별
    -- role ENUM('user','admin','manager') DEFAULT 'user',   -- 권한
    -- profile_image_url VARCHAR(255),                    -- 프로필 이미지 경로
    status ENUM('active','inactive','deleted') DEFAULT 'active', -- 회원 상태
    last_login TIMESTAMP NULL,                         -- 마지막 로그인 시각
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- 가입일시
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 수정일시
)
; 



INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee1',  '1234', 'lee1@gmail.com',  '001024561111', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee2',  '1234', 'lee2@gmail.com',  '001024561112', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee3',  '1234', 'lee3@gmail.com',  '001024561113', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee4',  '1234', 'lee4@gmail.com',  '001024561114', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee5',  '1234', 'lee5@gmail.com',  '001024561115', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee6',  '1234', 'lee6@gmail.com',  '001024561116', '20000101', 'male', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee7',  '1234', 'lee7@gmail.com',  '001024561117', '20000101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee8',  '1234', 'lee8@gmail.com',  '001024561118', '20000101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee9',  '1234', 'lee9@gmail.com',  '001024561119', '20000101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'lee10', '1234', 'lee10@gmail.com', '001024561120', '20000101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim1',  '1234', 'kim1@gmail.com',  '001024562111', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim2',  '1234', 'kim2@gmail.com',  '001024562112', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim3',  '1234', 'kim3@gmail.com',  '001024562113', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim4',  '1234', 'kim4@gmail.com',  '001024562114', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim5',  '1234', 'kim5@gmail.com',  '001024562115', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim6',  '1234', 'kim6@gmail.com',  '001024562116', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim7',  '1234', 'kim7@gmail.com',  '001024562117', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim8',  '1234', 'kim8@gmail.com',  '001024562118', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim9',  '1234', 'kim9@gmail.com',  '001024562119', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO minipjt_db.TB_CS_MEMBERS  (id, username, password, email, phone, birthdate, gender, status, last_login, created_at, updated_at) VALUES(0, 'kim10', '1234', 'kim10@gmail.com', '001024562120', '20010101', 'female', 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

```

