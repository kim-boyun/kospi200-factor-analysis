# KOSPI200 재무지표·팩터 분석

한국 주식 시장(KOSPI/KOSPI200) 데이터를 수집·전처리하고, 재무 지표와 수익률 간 관계를 **팩터 분석** 및 **상관분석**으로 탐색하는 프로젝트입니다.

---

## 프로젝트 구조

```
TeamProject/
├── README.md
├── requirements.txt
├── src/                      # 공통 데이터 로더 모듈
│   ├── __init__.py
│   ├── data_loader.py        # PykrxDataLoader (주가·시총·재무·거래주체·ETF·지수)
│   └── kospi200_loader.py    # Kospi200DataLoader (KOSPI200 종목·수익률)
├── notebooks/                # 분석 노트북 (실행 순서 권장)
│   ├── 01_data_preprocessing.ipynb   # 영업일 보정, KOSPI200 종목·수익률 수집
│   ├── 02_factor_analysis.ipynb      # PCA·요인분석
│   └── 03_correlation_analysis.ipynb  # 재무지표–수익률 상관분석
└── data/                     # 생성·병합 데이터 (CSV/Excel, .gitignore 대상)
    └── .gitkeep
```

---

## 기술 스택

| 구분 | 내용 |
|------|------|
| 데이터 소스 | **pykrx** (한국거래소), 공시·재무 데이터(별도 병합) |
| 분석 | pandas, scikit-learn (PCA), factor_analyzer, scipy |
| 시각화 | matplotlib, seaborn |

---

## 설치 및 실행

### 1. 환경 설정

```bash
cd TeamProject
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 노트북 실행

- Jupyter 또는 VS Code에서 `notebooks/` 폴더를 **프로젝트 루트(TeamProject)** 기준으로 열고 실행하는 것을 권장합니다.
- 루트에서 실행할 경우:
  ```bash
  jupyter notebook notebooks/
  ```
- **02_factor_analysis**, **03_correlation_analysis**는 `data/제조업_수익률.csv`가 필요합니다.  
  - 01에서 KOSPI200 수익률을 수집한 뒤, DART 등에서 가져온 재무·업종 데이터와 병합해 해당 파일을 생성하면 됩니다.

---

## 주요 기능

### `src/data_loader.py` — PykrxDataLoader

- 기간·시장(KOSPI 등) 지정 후 아래 데이터 조회:
  - 티커 리스트, 영업일
  - 시가총액·거래량·거래대금
  - 재무(펀더멘털), 거래주체(기관/외국인/개인)
  - 주가(OHLCV), ETF, 지수

### `src/kospi200_loader.py` — Kospi200DataLoader

- 지정 기간 **KOSPI200 편입 종목 리스트** (중복 제외)
- **다음 영업일** 보정: `get_next_trading_day(date)`
- 종목별·연도별 **시가총액·시총 변화율**
- **연도별 수익률** (시가→종가)

### 노트북 요약

1. **01_data_preprocessing**  
   영업일 보정 함수 정의, KOSPI200 종목 리스트·수익률 수집 예시.

2. **02_factor_analysis**  
   제조업 재무·수익률 데이터 전처리, (원) 단위 컬럼 제거, PCA·요인분석.

3. **03_correlation_analysis**  
   IFRS 재무지표와 수익률 간 상관계수 계산 및 히트맵 시각화.

---

## 라이선스

본 저장소는 포트폴리오 목적으로 정리된 프로젝트입니다.
