## 작업 워크플로우 (TDD)

모든 작업은 다음 순서로 진행한다:

1. **Planner** — 요구사항 분석, 구현 계획 수립, 파일/의존성 파악
2. **TDD-Guide** — 테스트 먼저 작성 (RED), 실패 확인
3. **Executor** — 테스트를 통과하는 최소 구현 (GREEN)
4. **Fixer** — 실패한 테스트 수정, 버그 해결
5. **Reviewer** — 코드 품질/보안/성능 검토, 리팩터 (IMPROVE)

각 단계는 이전 단계 완료 후 진행. Fixer는 테스트 전부 통과 시 건너뜀.
테스트 커버리지 80% 이상 유지.

# Project: Korea-US Integrated Market Dashboard

## 1. Project Overview

이 프로젝트는 한국 투자자가 국장과 미국장을 함께 해석할 수 있도록 돕는 통합 시장 대시보드 웹 애플리케이션을 구축하는 것을 목표로 한다.

단순히 시세를 나열하는 서비스가 아니라, 다음 질문에 빠르게 답할 수 있는 판단 보조 도구를 만든다.

1. 지금 한국 주식과 미국 주식은 어떤 상태인가?
2. 간밤 미국장, 환율, 유가, 금리 변화가 오늘 국장에 어떤 영향을 줄 가능성이 있는가?
3. 오늘 어떤 섹터가 강하고 어떤 섹터가 약한가?
4. 오늘과 이번 주에 반드시 챙겨야 할 한국/미국 핵심 일정은 무엇인가?
5. 미국 주식 가격을 원화 기준으로 보면 실제 체감 가격과 손익은 얼마인가?

핵심 목표는 “정보를 많이 보여주는 것”이 아니라,  
**한국 투자자가 국장과 미장을 한 화면에서 빠르게 해석하고 우선순위를 잡게 만드는 것**이다.

---

## 2. Product Vision

이 제품은 단순 시세판이 아니라 다음 역할을 수행해야 한다.

- 국장과 미장을 따로 보지 않고 하나의 문맥 안에서 해석하게 해준다
- 미국장 종료 후, 오늘 국장에서 무엇을 봐야 하는지 빠르게 정리해준다
- 미국 종목을 원화 기준으로 다시 계산하는 번거로움을 줄여준다
- 섹터 단위로 시장 자금 흐름을 시각화한다
- 핵심 일정만 추려서 변동성 이벤트를 미리 대비하게 한다
- AI를 통해 숫자와 이벤트를 짧고 정확하게 해석해준다

---

## 3. Target Users

### Core Users

- 국장과 미국장을 함께 보는 한국 투자자
- 삼성전자, SK하이닉스 같은 국장 대형주와 미국 기술주를 같이 보는 사용자
- 환율 영향을 체감하며 미국 주식을 보는 사용자
- 증권사 HTS/MTS와 TradingView/Investing.com을 같이 쓰는 사용자
- 긴 뉴스보다 핵심 숫자와 일정만 빠르게 보고 싶은 사용자

### User Pain Points

- 미국 종목 가격을 매번 원화로 다시 계산해야 함
- 국장과 미장을 연결해서 해석하는 데 시간이 많이 걸림
- 경제 일정 서비스는 정보가 너무 많아 핵심만 보기 어려움
- 시장 전체 흐름보다 개별 종목만 보게 됨
- 미국장 종료 후 오늘 국장에 중요한 포인트가 뭔지 빠르게 파악하기 어려움

---

## 4. Core Product Principles

### Principle 1. Korea-first interpretation

모든 정보는 한국 투자자 기준으로 해석되어야 한다.  
특히 환율, 국장 개장 시간, 외국인 수급 민감도, 미국 이벤트의 한국 시간 기준 영향을 우선시한다.

### Principle 2. Interpretation over raw data

숫자를 많이 보여주는 것이 아니라,  
**어떤 숫자가 중요한지와 왜 중요한지**가 빠르게 보여야 한다.

### Principle 3. Structured data first

AI보다 먼저 정형 데이터 레이어가 완성되어야 한다.  
데이터 구조가 불안정하면 AI는 쓸모없는 소음 생성기가 된다.

### Principle 4. Signal over noise

정보량을 늘리는 방향이 아니라, 핵심 신호를 남기고 나머지는 버리는 방향으로 설계한다.

### Principle 5. No fake certainty

AI는 해석은 해도 되지만, 근거 없는 확신형 매수/매도 조언은 금지한다.

---

## 5. MVP Scope

### Included in MVP

1. 한국/미국 통합 관심종목 보드
2. 실시간 환율 기반 미국 종목 원화 환산 표시
3. 한국/미국 듀얼 섹터 히트맵
4. 한국/미국 통합 경제 일정 캘린더 & D-Day 보드
5. AI 기반 시장 해석 카드
6. 국장 개장 전 브리프 카드
7. 핵심 지수/환율/원자재 상단 요약 바

### Excluded from MVP

1. 자동 매매 기능
2. 증권사 계좌 연동
3. 포트폴리오 자동 동기화
4. 직접적인 매수/매도 추천
5. 고급 차트 분석 도구 복제
6. TradingView 수준의 전체 차트 플랫폼 기능
7. 공포와 탐욕 지수 위젯
8. 뉴스 기사 전문 요약 피드

---

## 6. Primary User Flows

### Flow A. 아침 국장 개장 전 확인

1. 사용자가 대시보드 접속
2. 상단에서 간밤 미국 지수, 환율, 유가 확인
3. AI 개장 전 브리프 확인
4. 한국 히트맵과 미국 히트맵 비교
5. 오늘 핵심 일정 확인
6. 오늘 볼 종목/섹터 우선순위 결정

### Flow B. 장중 시장 해석

1. 한국 섹터 히트맵 확인
2. 미국 히트맵 또는 전일 미국 흐름과 비교
3. AI 장중 해석 카드 확인
4. 관심종목 보드에서 한국 종목/미국 종목 상태 확인

### Flow C. 미국 종목 원화 체감 확인

1. 관심 미국 종목 확인
2. 현재 USD 가격과 KRW 환산가 비교
3. 환율 영향과 주가 영향 분리 해석 확인
4. 체감 손익 판단

### Flow D. 이벤트 체크

1. 오늘/이번 주 핵심 일정 확인
2. 한국 이벤트 / 미국 이벤트 구분 확인
3. D-Day 및 중요도 확인
4. AI 리스크 브리프 확인

---

## 7. Information Architecture

### Top Summary Bar

- KOSPI
- KOSDAQ
- S&P 500
- Nasdaq 100
- Dow or SOX
- USD/KRW
- JPY/KRW
- EUR/KRW
- WTI
- Gold

### Main Section A

- 한국/미국 통합 관심종목 보드

### Main Section B

- 듀얼 섹터 히트맵
  - KOR Heatmap
  - US Heatmap

### Main Section C

- 오늘/이번 주 통합 일정 캘린더
- D-Day 보드

### Main Section D

- AI 시장 해석 카드
- 국장 개장 전 브리프
- 환율 영향 해석 카드

---

## 8. Feature Specification

---

## Feature 1. Korea-US Unified Watch Board

### Goal

한국 종목과 미국 종목을 하나의 관심종목 보드에서 함께 관리하고, 미국 종목은 원화 기준 체감 가격까지 바로 볼 수 있게 한다.

### Why it matters

사용자는 국장과 미장을 따로 보지 않는다.  
실제 판단은 다음처럼 섞여서 일어난다.

- 미국 반도체 강세가 오늘 SK하이닉스에 먹히는가?
- 달러 상승이 미국 주식 체감 수익률에 얼마나 영향을 주는가?
- 지금 국장과 미장 중 어디에 상대적으로 우위가 있는가?

### Functional Requirements

- 한국 종목과 미국 종목 혼합 관심종목 목록 지원
- 종목별 시장 구분 표시
  - KOR
  - US
- 종목별 표시 항목
  - symbol
  - company_name
  - market_type
  - local_price
  - currency
  - krw_converted_price
  - daily_change_percent
  - daily_change_amount_local
  - daily_change_amount_krw
  - market_session_status
- 미국 종목은 실시간 또는 준실시간 환율로 원화 환산가 표시
- 시장 상태 표시
  - 국내장중
  - 장마감
  - 프리마켓
  - 애프터마켓
- 정렬 기능
  - 등락률
  - 원화 체감 변화액
  - 시가총액
  - 사용자 고정순

### Advanced Requirements

- 원화 기준 손익률 계산
- 환율 영향과 주가 영향 분리 표시
- 미국 종목의 원화 체감 수익/손실 설명 텍스트 제공
- 한국 종목과 미국 종목을 섹터별로 묶어 볼 수 있는 옵션 제공

### UX Rules

- 미국 종목만 원화 환산을 강조한다
- 한국 종목은 불필요한 환산 로직 없이 KRW 그대로 표시한다
- 종목이 너무 많아지면 가치가 떨어지므로 기본 워치리스트는 10~20개 수준으로 제한하는 방향을 우선한다

### Example Columns

- 시장
- 종목명
- 심볼
- 현재가
- 통화
- 원화환산
- 등락률
- 원화변화액
- 상태

---

## Feature 2. FX Layer for KRW Conversion

### Goal

미국 종목 가격을 한국 사용자 기준으로 즉시 해석할 수 있도록 주요 환율을 캐싱 기반으로 제공한다.

### Functional Requirements

- 상단 환율 바 제공
  - USD/KRW
  - JPY/KRW
  - EUR/KRW
- 환율 데이터 캐싱
  - 기본 갱신 주기: 1~5분
- 환율 갱신 시 관련 원화 환산값 자동 재계산
- 환율 변화율 표시
- 전일 대비 표시

### Advanced Requirements

- 환율 변화만으로 발생한 원화 체감 손익 분리 계산
- 달러 강세 / 약세에 따른 미국 종목 체감 성과 해석
- 미국 종목의 주가 변화와 환율 변화의 기여도 분리

### Example Interpretation

- 주가는 보합이지만 달러 강세로 원화 기준 체감 가격은 상승
- 주가는 상승했지만 달러 약세 때문에 원화 체감 수익은 일부 상쇄
- 종목 하락에도 환율 상승이 손실을 일부 완충

---

## Feature 3. Dual Sector Heatmap

### Goal

한국과 미국 시장의 섹터 강약을 한눈에 파악할 수 있도록 국가별 히트맵을 제공한다.

### Why it matters

개별 종목만 보면 시장의 자금 흐름이 보이지 않는다.  
섹터 히트맵은 “오늘 돈이 어디로 가는지”를 빠르게 보여준다.

### Functional Requirements

- KOR / US 분리 히트맵 제공
- 각 섹터 내부 대표 종목 기반 treemap 구성
- 사각형 크기 = 시가총액
- 사각형 색 = 등락률
- 툴팁 제공
  - 종목명
  - 심볼
  - 등락률
  - 시가총액
  - 섹터
- 섹터 요약 제공
  - strongest sectors
  - weakest sectors

### Korea Sector Examples

- 반도체
- 2차전지
- 자동차
- 인터넷
- 바이오
- 금융
- 조선
- 방산
- 에너지
- 화학

### US Sector Examples

- Big Tech
- Semiconductors
- Energy
- Finance
- Consumer
- Healthcare
- Industrials
- Communication Services

### UX Rules

- 종목 수를 과도하게 늘리지 않는다
- 섹터 grouping이 명확해야 한다
- 색 기준은 직관적이어야 하며 과장되면 안 된다
- 인터랙션보다 가독성을 우선한다
- “국장 강세 섹터 vs 미장 강세 섹터” 비교가 바로 보이게 한다

### AI Interpretation Opportunities

- 미국 반도체 강세가 한국 반도체에 우호적인 흐름인지
- 미장 기술주 약세인데 국장은 독립적으로 강한 섹터가 있는지
- 환율/유가/금리와 연결해서 특정 섹터 강약을 해석할 수 있는지

---

## Feature 4. Unified Event Calendar & D-Day Board

### Goal

한국과 미국의 핵심 매크로 일정, 정책 일정, 실적 발표 일정을 한 화면에서 간결하게 보여준다.

### Problem

일반 경제 캘린더는 정보가 너무 많아서 실제 중요한 이벤트만 빠르게 보기 어렵다.

### Functional Requirements

- 오늘 / 이번 주 / 이번 달 보기 제공
- 국가별 구분
  - Korea
  - US
- 이벤트별 표시 항목
  - event_name
  - country
  - category
  - event_time
  - D-Day
  - importance
  - previous
  - forecast
  - related_assets
- 중요 이벤트만 선별 노출
- 카테고리 필터
  - macro
  - earnings
  - central_bank
  - tech
  - policy
- 시간순 정렬
- D-Day 강조 표시

### Korea Event Examples

- 한국은행 금통위
- 한국 CPI
- 수출입 동향
- GDP
- 옵션 만기일
- MSCI 리밸런싱 일정
- 주요 대형주 실적
- 정책 이벤트

### US Event Examples

- CPI
- PPI
- FOMC
- Nonfarm Payrolls
- GDP
- major tech earnings
- Treasury-related events
- options expiration

### UX Rules

- 인베스팅닷컴식 과잉 정보 구조를 피한다
- 핵심 일정만 남긴다
- 국장 기준 영향 / 미장 기준 영향 요약이 있어야 한다
- 시간대는 한국 시간 기준으로 우선 노출한다

### Output Blocks

- 오늘 국장 영향 이벤트
- 오늘 미장 영향 이벤트
- 이번 주 핵심 이벤트
- D-1 / D-Day 이벤트 강조

---

## Feature 5. AI Interpretation Layer

### Goal

정형 데이터를 바탕으로 시장 상황을 짧고 정확하게 해석해 사용자의 판단 부담을 줄인다.

### AI must do

- 핵심 변수 간 관계 해석
- 간밤 미국장이 오늘 국장에 줄 수 있는 영향 요약
- 환율이 미국 종목 체감 수익률에 미친 영향 설명
- 섹터 강약 구조 요약
- 이벤트 전 리스크 포인트 요약

### AI must not do

- 직접적인 매수/매도 추천
- 허위 확신 표현
- 데이터에 없는 내용 단정
- 목표가 제시
- 루머성 해석

### AI Output Types

1. 개장 전 브리프
2. 장중 요약
3. 환율 체감 해석
4. 일정 리스크 브리프
5. 섹터 로테이션 해석

---

## 9. AI Use Cases

### Use Case 1. Opening Brief for Korean Market

입력:

- 간밤 미국 지수 변동
- 필라델피아 반도체지수 또는 주요 기술주 흐름
- USD/KRW 변화
- 유가, 금, 금리 관련 핵심 변화
- 오늘 일정

출력 예시:

- 간밤 미국 반도체 강세가 나타났고, 이는 오늘 국장 반도체 대형주에 우호적일 수 있다.
- 달러원 상승 압력으로 외국인 수급은 다소 보수적으로 볼 필요가 있다.
- 오늘 밤 미국 CPI 발표가 예정되어 있어 장중 경계 심리가 유지될 가능성이 있다.

### Use Case 2. KRW Impact Explanation

입력:

- 미국 종목 가격 변화
- USD/KRW 변화
- 원화 환산가 변화

출력 예시:

- 종목 자체는 -1.0% 하락했지만 달러 강세로 원화 기준 체감 손실은 일부 완화되었다.
- 주가 상승분보다 환율 하락폭이 커서 원화 기준 체감 수익은 제한적이다.

### Use Case 3. Sector Rotation Insight

입력:

- 한국/미국 섹터별 평균 등락률
- 시가총액 가중 변동
- 이전 세션 대비 변화

출력 예시:

- 미국에서는 반도체와 빅테크 중심의 위험선호 흐름이 나타났고, 한국에서는 반도체와 조선이 상대 강세를 보이고 있다.
- 에너지 상승에도 성장주가 버티는 구조로, 시장이 완전한 위험회피로 보기는 어렵다.

### Use Case 4. Event Risk Brief

입력:

- 오늘/이번 주 이벤트
- 중요도
- 관련 자산
- 최근 시장 상태

출력 예시:

- 오늘 밤 FOMC 관련 발언 이벤트가 있어 금리민감 성장주 변동성이 확대될 수 있다.
- 한국시장에서는 옵션 만기와 겹쳐 장중 변동성이 커질 수 있다.

### Use Case 5. Midday Market Interpretation

입력:

- 국장 장중 지수
- 섹터별 흐름
- 환율 변화
- 외국인 수급 대체 지표 또는 가능한 범위 내 시장 폭 정보

출력 예시:

- 지수는 보합권이지만 반도체와 조선 중심으로 상승이 집중되고 있다.
- 환율 상승에도 대형주가 버티고 있어 지수 하단은 비교적 지지되는 흐름이다.

---

## 10. AI System Design Principles

### Principle 1. Retrieval-first / Data-first

AI는 반드시 구조화된 데이터 스냅샷을 기반으로 동작해야 한다.

### Principle 2. Explanation over prediction

예측보다 해석을 우선한다.

### Principle 3. Controlled output

출력 길이, 톤, 금지 표현을 통제한다.

### Principle 4. Korea market context

모든 출력은 한국 투자자 체감 기준을 우선한다.

### Principle 5. Time-aware interpretation

미국 이벤트는 한국 시간대 기준 영향 시점을 함께 설명한다.

---

## 11. Suggested AI Input Schema

```json
{
  "timestamp": "2026-04-02T08:30:00+09:00",
  "summary_bar": {
    "KOSPI": {"change_percent": 0.4},
    "KOSDAQ": {"change_percent": -0.2},
    "SP500": {"change_percent": -0.8},
    "NASDAQ100": {"change_percent": -1.1},
    "USDKRW": {"value": 1452.3, "change_percent": 0.5},
    "WTI": {"change_percent": 1.4},
    "GOLD": {"change_percent": 0.6}
  },
  "watchlist": [
    {
      "symbol": "005930",
      "company_name": "Samsung Electronics",
      "market_type": "KOR",
      "price_local": 84200,
      "currency": "KRW",
      "change_percent": 1.2
    },
    {
      "symbol": "NVDA",
      "company_name": "NVIDIA",
      "market_type": "US",
      "price_local": 122.4,
      "currency": "USD",
      "price_krw": 177724,
      "change_percent": -0.9,
      "fx_impact_percent": 0.5
    }
  ],
  "sectors": {
    "KOR": [
      {"name": "Semiconductors", "change_percent": 1.8},
      {"name": "Biotech", "change_percent": -0.7}
    ],
    "US": [
      {"name": "Big Tech", "change_percent": -1.2},
      {"name": "Energy", "change_percent": 1.1}
    ]
  },
  "events": [
    {
      "country": "US",
      "name": "US CPI",
      "time": "2026-04-03T21:30:00+09:00",
      "importance": "high",
      "related_assets": ["NASDAQ", "USD", "Treasury"]
    },
    {
      "country": "KOR",
      "name": "BOK Rate Decision",
      "time": "2026-04-04T10:00:00+09:00",
      "importance": "high",
      "related_assets": ["KOSPI", "KRW", "Banks"]
    }
  ]
}
12. AI Output Rules

Good Output
	•	짧다
	•	데이터 기반이다
	•	한국 투자자 관점이다
	•	과장하지 않는다
	•	변수 간 관계를 설명한다
	•	읽고 바로 행동 우선순위를 정할 수 있다

Bad Output
	•	지금 무조건 매수해야 한다
	•	곧 폭등 가능성이 높다
	•	시장 반등이 확실하다
	•	이유 없는 낙관/비관 표현
	•	구조화 데이터에 없는 주장

Style Guide
	•	2~5문장 중심
	•	문장은 짧고 단정하되 확신 과잉 금지
	•	설명은 해석 중심, 조언 중심 아님
	•	한국 시간과 한국 시장 체감 포인트를 우선

⸻

13. Technical Architecture

Frontend
	•	Next.js
	•	TypeScript
	•	Tailwind CSS
	•	React Query or SWR
	•	D3.js for treemap heatmap
	•	lightweight-charts optionally for mini trend charts

Backend
	•	FastAPI or Node.js
	•	Scheduler / cron jobs
	•	Redis for caching
	•	PostgreSQL for normalized storage
	•	Optional worker queue for data polling and AI summary generation

Data Pipeline
	1.	환율 데이터 수집
	2.	한국 주식/미국 주식 시세 수집
	3.	섹터 메타데이터 정규화
	4.	일정 데이터 수집 및 정규화
	5.	최신 snapshot 저장
	6.	AI summary input snapshot 생성
	7.	AI summary 생성 및 캐싱
	8.	프론트에 통합 응답 제공

Cache Strategy
	•	FX: 1~5 min
	•	quotes: provider 정책에 맞춘 짧은 주기
	•	events: 10~60 min
	•	sector aggregation: 1~5 min
	•	AI summary: 의미 있는 변화 발생 시 또는 일정 주기 재생성

⸻

14. Suggested External Data Sources

FX
	•	한국은행 ECOS API
	•	ExchangeRate-API
	•	기타 신뢰 가능한 환율 제공 API

Market Quotes
	•	한국 주식 시세 API
	•	미국 주식 시세 API
	•	ETF / 지수 / 원자재 / 환율 관련 시세 API

Events
	•	경제 일정 API
	•	실적 발표 일정 API
	•	정책/중앙은행 일정 데이터 소스

Sector Metadata
	•	종목-섹터 매핑 데이터
	•	시가총액 데이터
	•	대표 종목 선정용 메타데이터

⸻

15. Internal Data Models

fx_rates
	•	id
	•	base_currency
	•	target_currency
	•	rate
	•	change_percent
	•	updated_at

instruments
	•	id
	•	symbol
	•	company_name
	•	market_type
	•	country
	•	currency
	•	sector
	•	industry
	•	market_cap
	•	is_active

market_quotes
	•	id
	•	instrument_id
	•	price_local
	•	price_krw
	•	daily_change_percent
	•	daily_change_amount_local
	•	daily_change_amount_krw
	•	session_status
	•	updated_at

sector_snapshots
	•	id
	•	country
	•	sector_name
	•	weighted_change_percent
	•	strongest_symbol
	•	weakest_symbol
	•	updated_at

market_events
	•	id
	•	country
	•	category
	•	event_name
	•	event_time
	•	importance
	•	previous_value
	•	forecast_value
	•	related_assets
	•	source
	•	updated_at

ai_summaries
	•	id
	•	summary_type
	•	input_snapshot_hash
	•	content
	•	generated_at

⸻

16. API Design (Suggested)

GET /api/summary-bar

상단 요약 바 데이터 반환

Response:
	•	KOSPI
	•	KOSDAQ
	•	S&P500
	•	Nasdaq100
	•	USD/KRW
	•	JPY/KRW
	•	EUR/KRW
	•	WTI
	•	Gold

GET /api/watchlist

통합 관심종목 보드 데이터 반환

Query params:
	•	market=all|kor|us
	•	sort=change|krw_delta|market_cap
	•	sector=optional

GET /api/sectors/heatmap

듀얼 히트맵 데이터 반환

Response:
	•	KOR sectors
	•	US sectors
	•	top movers
	•	bottom movers

GET /api/events

통합 경제 일정 반환

Query params:
	•	range=today|week|month
	•	country=all|kor|us
	•	category=all|macro|earnings|policy

GET /api/ai/opening-brief

국장 개장 전 브리프 반환

GET /api/ai/market-summary

현재 시장 요약 반환

GET /api/ai/krw-impact?symbol=NVDA

특정 미국 종목의 원화 체감 영향 해석 반환

⸻

17. MVP UI Layout

Top Bar
	•	KOSPI
	•	KOSDAQ
	•	S&P500
	•	Nasdaq100
	•	USD/KRW
	•	WTI
	•	Gold

Section 1

좌측:
	•	AI 개장 전 브리프 카드

우측:
	•	오늘 핵심 이벤트 카드
	•	이번 주 D-Day 카드

Section 2
	•	한국/미국 통합 관심종목 보드

Section 3

좌측:
	•	KOR Heatmap

우측:
	•	US Heatmap

Section 4

좌측:
	•	AI 시장 해석 카드

우측:
	•	환율 체감 영향 카드
	•	strongest sectors / weakest sectors

⸻

18. Phased Roadmap

Phase 1 - MVP
	•	상단 요약 바
	•	통합 관심종목 보드
	•	환율 원화 환산
	•	듀얼 히트맵
	•	통합 일정 보드
	•	기본 AI 요약 카드
	•	개장 전 브리프

Phase 2
	•	사용자 맞춤 워치리스트
	•	원화 기준 손익 추적
	•	섹터 5D / 1M 비교
	•	일정 알림
	•	환율 임계치 알림

Phase 3
	•	AI 장중 해석 강화
	•	미장 → 국장 전이 해석 고도화
	•	이벤트 영향 사전 브리프 강화
	•	히스토리 비교 기반 설명

Phase 4
	•	사용자별 관심 섹터 기반 개인화
	•	오늘 볼 섹터 Top 3 자동 선정
	•	국장/미장 비중 기반 맞춤 해석
	•	개인화 리스크 알림

⸻

19. AI Evolution Plan

Stage A. Rule-based summaries

초기에는 룰 기반 템플릿으로 시작한다.

Examples:
	•	달러 상승 + 나스닥 하락 → risk-off 경계 템플릿
	•	미국 반도체 강세 + 한국 반도체 강세 → 반도체 주도 템플릿
	•	CPI D-1 → 이벤트 경계 템플릿

Why:
	•	일관성 확보
	•	비용 절감
	•	헛소리 방지

Stage B. Structured LLM summaries

정형 snapshot 기반으로 LLM 요약을 도입한다.

Requirements:
	•	입력은 JSON snapshot
	•	출력 길이 제한
	•	투자 추천 금지
	•	데이터 밖 추론 금지

Stage C. Historical context summaries

과거 5일 / 20일 / 유사 이벤트 전후 패턴을 함께 붙인다.

Examples:
	•	최근 5거래일 동안 달러 강세와 기술주 약세 조합이 반복됨
	•	FOMC 전날에는 반도체 변동성이 확대되는 경향

Stage D. Personalized AI

사용자 관심종목 / 관심섹터 / 투자 스타일에 맞춘 요약 제공

Examples:
	•	반도체 비중이 높은 사용자는 반도체 관련 브리프를 우선 노출
	•	미국 종목 비중이 높은 사용자는 환율 해석을 더 크게 노출
	•	국장 단기 트레이더는 장중 섹터 순환 해석을 우선 노출

⸻

20. Non-goals

이 프로젝트는 아래를 목표로 하지 않는다.
	•	자동 투자 자문 서비스
	•	법적 규제가 걸릴 수 있는 투자 추천
	•	증권사 주문 실행 기능
	•	모든 뉴스의 실시간 요약
	•	차트 분석 도구 풀세트 복제
	•	복잡한 금융 터미널 대체

⸻

21. Success Metrics

MVP Success Metrics
	•	사용자가 5초 내에 오늘 시장 핵심 포인트를 파악할 수 있는가
	•	미국 종목의 원화 체감 가격 이해가 쉬운가
	•	오늘 중요 일정이 빠르게 보이는가
	•	개장 전 브리프가 실질적으로 유용한가
	•	국장과 미장의 연결 해석이 자연스러운가

Product Metrics
	•	dashboard first meaningful paint
	•	cache hit ratio
	•	watchlist interaction rate
	•	opening brief click/view rate
	•	repeat visit rate
	•	AI summary usefulness feedback
	•	event card interaction rate

⸻

22. Implementation Priorities

Priority 1

통합 관심종목 보드 + 환율 환산 레이어

Priority 2

상단 요약 바

Priority 3

통합 일정 보드

Priority 4

듀얼 히트맵

Priority 5

룰 기반 AI 개장 전 브리프

Priority 6

구조화 LLM 요약

주의:
AI를 먼저 만들지 않는다.
먼저 데이터 수집, 정규화, 캐싱, 화면 구조를 완성한다.
데이터 레이어가 엉망이면 AI는 똑똑한 척하는 쓰레기 기능이 된다.

⸻

23. Developer Notes for Claude

Build priorities
	1.	데이터 모델 설계
	2.	API 스키마 정의
	3.	더미 데이터 기반 UI 구현
	4.	실제 데이터 연결
	5.	캐싱 및 갱신 전략 적용
	6.	룰 기반 요약 구현
	7.	LLM summary 레이어 추가

Coding priorities
	•	타입 안정성 확보
	•	데이터 정규화 우선
	•	UI는 한눈에 읽히는 구조 우선
	•	복잡한 애니메이션보다 빠른 로딩과 명확한 정보 위계 우선
	•	한국 시간 기준 표기 통일
	•	market session status 정확도 확보

Quality bar
	•	화면이 화려한 것보다 빠르게 읽히는 것이 더 중요하다
	•	숫자는 많아도 되지 않는다. 중요한 숫자만 남겨라
	•	AI는 말 많은 해설자가 아니라 짧고 정확한 해석기여야 한다
	•	미국 정보가 오늘 국장에 어떻게 번역되는지가 이 제품의 핵심 가치다

⸻

24. Final Product Definition

이 제품은 “국장과 미장을 동시에 보는 한국 투자자”를 위한
통합 시장 판단 보조 대시보드다.

좋은 제품은 다음을 만족해야 한다.
	•	국장과 미장을 하나의 흐름으로 보여준다
	•	미국 종목을 원화 기준 체감으로 바로 보여준다
	•	오늘 강한 섹터와 약한 섹터를 빠르게 보여준다
	•	한국과 미국의 핵심 일정만 추려서 보여준다
	•	AI가 근거 없는 예측이 아니라, 정량 데이터를 바탕으로 짧고 정확하게 해석해준다
```
