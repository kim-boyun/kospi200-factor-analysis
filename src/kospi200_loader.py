"""KOSPI200 종목 리스트·시가총액·수익률 수집 로더."""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pykrx import stock


class Kospi200DataLoader:
    """지정 기간 KOSPI200 편입 종목 리스트, 시가총액, 연도별 수익률을 조회하는 로더."""

    def __init__(self, start_year: int, end_year: int):
        self.start_year = start_year
        self.end_year = end_year

    @staticmethod
    def get_next_trading_day(date: str) -> str:
        """
        입력 날짜가 휴장일이면 다음 영업일을 반환.
        date: 'YYYYMMDD' 형식 문자열.
        """
        while True:
            df = stock.get_market_ohlcv_by_date(date, date, "005930")
            if not df.empty:
                return date
            dt = datetime.strptime(date, "%Y%m%d") + timedelta(days=1)
            date = dt.strftime("%Y%m%d")

    def kospi200_list(self):
        """지정 기간 동안 KOSPI200 편입 종목 코드 리스트(중복 제외) 반환."""
        records = []
        for year in range(self.start_year, self.end_year + 1):
            df = stock.get_index_portfolio_deposit_file("1028", f"{year}1231", alternative=True)
            for code in df:
                records.append({'연도': year, '주식코드': code})

        result_df = pd.DataFrame(records)
        frequency = result_df['주식코드'].value_counts()
        frequency_df = frequency.reset_index()
        frequency_df.columns = ['주식코드', '빈도수']
        code_list = frequency_df['주식코드'].tolist()
        return code_list

    def get_market_caps(self, codes: pd.DataFrame):
        """종목별·연도별 시가총액 및 시총 변화율 데이터프레임 반환."""
        records = []
        for year in range(self.start_year - 1, self.end_year + 1):
            date = f"{year}0401"
            trading_date = self.get_next_trading_day(date)
            cap_df = stock.get_market_cap_by_ticker(trading_date)
            for code in codes["주식코드"]:
                if code in cap_df.index:
                    market_cap = cap_df.loc[code, '시가총액']
                    records.append({
                        '주식코드': code,
                        '연도': year,
                        '날짜': trading_date,
                        '시가총액': market_cap
                    })
                else:
                    records.append({
                        '주식코드': code,
                        '연도': year,
                        '날짜': trading_date,
                        '시가총액': None
                    })
        df = pd.DataFrame(records)
        df = df.sort_values(by=['주식코드', '연도']).reset_index(drop=True)
        df['시총변화율'] = df.groupby('주식코드')['시가총액'].pct_change()
        df = df[df['연도'] >= 2015].reset_index(drop=True)
        return df

    def kospi200_rtn(self, codes: pd.DataFrame) -> pd.DataFrame:
        """종목 리스트에 대한 연도별 수익률(시가→종가) 데이터프레임 반환."""
        records = []
        for code in codes['주식코드']:
            df = stock.get_market_ohlcv_by_date(
                f"{self.start_year}0101", f"{self.end_year}1231", code, freq='y'
            )
            if not df.empty:
                df = df[['시가', '종가']].reset_index()
                df['연도'] = df['날짜'].dt.year
                df['수익률'] = ((df['종가'] - df['시가']) / df['시가'])
                records.append(df.assign(주식코드=code))

        result_df = pd.concat(records)[['주식코드', '연도', '수익률']]
        result_df = result_df.replace([np.inf, -np.inf], np.nan)
        result_df.dropna(inplace=True)
        return result_df
