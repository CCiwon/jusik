# Korea-US Integrated Market Dashboard

한국/미국 통합 시장 대시보드 - 국장과 미장을 한 화면에서 해석하는 판단 보조 도구

## 실행 방법

### 1. 사전 준비

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 필요

### 2. 레포 클론

```bash
git clone https://github.com/CCiwon/jusik.git
cd jusik
```

### 3. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어서 아래 값 입력:

```env
DB_PASSWORD=원하는DB비밀번호

# Finnhub API 키 (https://finnhub.io 무료 가입)
FINNHUB_API_KEY=발급받은키

# 한국은행 ECOS API 키 (https://ecos.bok.or.kr 무료 가입)
ECOS_API_KEY=발급받은키
```

### 4. 실행

```bash
docker compose up -d
```

### 5. 초기 데이터 시드

```bash
docker exec snp-backend-1 python -m app.seed_runner
```

### 6. 접속

브라우저에서 http://localhost:3001 접속

---

## API 키 발급

| 서비스 | 용도 | 발급 링크 | 비용 |
|--------|------|-----------|------|
| Finnhub | 미국 주식 시세, 경제 일정 | https://finnhub.io | 무료 |
| 한국은행 ECOS | 환율 (USD/KRW, JPY/KRW, EUR/KRW) | https://ecos.bok.or.kr | 무료 |

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis, APScheduler
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, React Query, D3.js
- **Data**: yfinance (한국 주식), Finnhub (미국 주식), ECOS (환율)
- **Infra**: Docker Compose
