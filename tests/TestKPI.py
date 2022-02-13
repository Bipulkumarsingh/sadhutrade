import unittest
import datetime as dt
from datasource.datasource import DATASOURCETYPE
from stocks_model.StocksFactory import StocksFactory
from src.constants import *
from library.kpi import CAGR, Calmar, MaxDrawDown, Volatility, Sharpe, Sortino
from data_analysis.financials import Financials

DEVELOPMENT = True

tickers = ["TSLA", "SPY"]
interval = INTERVAL.DAY
conf = {
    TICKERS_KEY: tickers,
    HISTORICAL_KEY: DATASOURCETYPE.YFINANCE,
    FUNDAMENTALS_KEY: None,
    FUNDAMENTALS_OPTIONS_KEY: [],
    FORCE_FUNDAMENTALS_KEY: False,
    INDICATORS_KEY: [],
    START_DATE_KEY: dt.datetime(2021, 3, 7) - dt.timedelta(1825),
    END_DATE_KEY: dt.datetime(2021, 3, 7),
    INTERVAL_KEY: interval,
    PERIOD_KEY: None,
    BULK_KEY: True

}

stocks = StocksFactory.create_stocks(conf=conf)


class TestKPI(unittest.TestCase):

    def test_KPI_cagr(self):
        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        params = {INTERVAL_KEY: interval}
        cagr = CAGR()
        result = cagr.calculate(df, params)

        self.assertEqual(0.7093784038450781, result[CAGR_KEY]['TSLA'])
        # self.assertEqual(0.1608091728848835, result[CAGR_KEY]['SPY'])
        self.assertEqual(0.1608, round(result[CAGR_KEY]['SPY'], 4))

    def test_KPI_max_drawdown(self):

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        md = MaxDrawDown()
        result = md.calculate(df)

        self.assertEqual(0.6062653645917145, result[MAX_DRAWDOWN_KEY]['TSLA'])
        # self.assertEqual(0.3371725544013077, result[MAX_DRAWDOWN_KEY]['SPY'])
        self.assertEqual(0.3372, round(result[MAX_DRAWDOWN_KEY]['SPY'], 4))

    def test_KPI_calmar(self):

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        params = {INTERVAL_KEY: interval}
        calmar = Calmar()
        result = calmar.calculate(df, params)

        self.assertEqual(1.1700790532917946, result[CALMR_KEY]['TSLA'])

    def test_KPI_volatility(self):

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        params = {INTERVAL_KEY: interval}
        volatility = Volatility()
        result = volatility.calculate(df, params)
        self.assertEqual(0.5807261171106989, result[VOLATILITY_KEY]['TSLA'])

    def test_KPI_sharpe(self):

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        params = {INTERVAL_KEY: interval, "rf": 0.0144}
        sharpe = Sharpe()
        result = sharpe.calculate(df, params)
        self.assertEqual(1.1967403968377064, result[SHARPE_KEY]['TSLA'])

    def test_KPI_sortino(self):

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        df = Financials.pct_change(prices_df)

        params = {INTERVAL_KEY: interval, "rf": 0.0144}
        sortino = Sortino()
        result = sortino.calculate(df, params)
        self.assertEqual(2.071479016783677, result[SORTINO_KEY]['TSLA'])

    # @staticmethod
    # def print_report(reports):
    #     for report in reports:
    #         report.print()


if __name__ == '__main__':
    unittest.main()
