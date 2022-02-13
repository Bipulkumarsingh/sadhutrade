import unittest
import datetime as dt
from src.constants import *
# import matplotlib.pyplot as plt
# from plotter.Plotter import Plotter
from datasource.datasource import DATASOURCETYPE
from stocks_model.StocksFactory import StocksFactory
from method.PortfolioRebalance import PortfolioRebalance

DEVELOPMENT = True


class TestMethods(unittest.TestCase):

    def test_portfolio_rebalance(self):
        end_date = dt.datetime.now()  # dt.datetime(2021, 3, 7)
        interval = INTERVAL.MONTH

        #  DJI constituent stocks
        tickers = ["MMM", "AXP", "T", "BA", "CAT", "CSCO", "KO", "XOM", "GE",
                   "GS", "HD", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
                   "NKE", "PFE", "PG", "TRV", "UNH", "VZ", "V", "WMT", "DIS"]

        ref_tickers = ["^DJI"]

        conf = {
            TICKERS_KEY: tickers,
            HISTORICAL_KEY: DATASOURCETYPE.YFINANCE,
            FUNDAMENTALS_KEY: None,
            FUNDAMENTALS_OPTIONS_KEY: [],
            FORCE_FUNDAMENTALS_KEY: False,
            INDICATORS_KEY: [],
            START_DATE_KEY: end_date - dt.timedelta(3650),
            END_DATE_KEY: end_date,
            INTERVAL_KEY: interval,
            PERIOD_KEY: None,
            BULK_KEY: True
        }

        stocks = StocksFactory.create_stocks(conf=conf)

        conf[TICKERS_KEY] = ref_tickers

        stocks_ref = StocksFactory.create_stocks(conf=conf)

        prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})
        ref_prices_df = stocks_ref[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})

        pr = PortfolioRebalance()
        params = {"m": 6, "x": 3, INTERVAL_KEY: conf[INTERVAL_KEY]}
        pr.backtest(prices_df, ref_prices_df, params)

        # self.assertEqual(0.7093784038450781, result['TSLA'][cagr_key()][0])

    # def test_intra_day(self):
    #     end_date = dt.datetime.now()  # dt.datetime(2021, 3, 7)
    #     interval = INTERVAL.MONTH
    #
    #     conf = {
    #         TICKERS_KEY: tickers,
    #         HISTORICAL_KEY: DATASOURCETYPE.YFINANCE,
    #         FUNDAMENTALS_KEY: None,
    #         FUNDAMENTALS_OPTIONS_KEY: [],
    #         FORCE_FUNDAMENTALS_KEY: False,
    #         INDICATORS_KEY: [],
    #         START_DATE_KEY: end_date - dt.timedelta(3650),
    #         END_DATE_KEY: end_date,
    #         INTERVAL_KEY: interval,
    #         PERIOD_KEY: None,
    #         BULK_KEY: True
    #     }
    #
    #     stocks = StocksFactory.create_stocks(conf=conf)
    #
    #     conf[TICKERS_KEY] = ref_tickers
    #
    #     stocks_ref = StocksFactory.create_stocks(conf=conf)
    #
    #     prices_df = stocks[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})
    #     ref_prices_df = stocks_ref[0].get_prices_data(keys={ADJ_CLOSE_KEY: True})
    #
    #     pr = PortfolioRebalance()
    #     params = {"m": 6, "x": 3, INTERVAL_KEY: conf[INTERVAL_KEY]}
    #     pr.backtest(prices_df, ref_prices_df, params)


if __name__ == '__main__':
    unittest.main()
