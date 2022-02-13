import copy
import pandas as pd
from stocks_model.Stock import Stock
from datasource import DataCollector
from src.constants import *


class StocksFactory:

    @staticmethod
    def create_stocks(conf):

        tickers = conf[TICKERS_KEY]

        data_source_historical = None
        data_source_fundamentals = None

        data_sources = DataCollector.get_data_sources(conf[HISTORICAL_KEY], conf[FUNDAMENTALS_KEY])

        if DataCollector.HISTORICAL in data_sources.keys():
            data_source_historical = data_sources[DataCollector.HISTORICAL]

            if data_source_historical is not None:
                data_source_historical.extract_historical_data(
                    tickers=tickers,
                    start_date=conf[START_DATE_KEY],
                    end_date=conf[END_DATE_KEY],
                    period=conf[PERIOD_KEY],
                    interval=conf[INTERVAL_KEY]

                )

        if DataCollector.FUNDAMENTALS in data_sources.keys():
            data_source_fundamentals = data_sources[DataCollector.FUNDAMENTALS]

            if data_source_fundamentals is not None:
                data_source_fundamentals.extract_fundamentals(
                    tickers=tickers,
                    date=conf[START_DATE_KEY],
                    required_elements=conf[FUNDAMENTALS_OPTIONS_KEY],
                    force_server_data=conf[FORCE_FUNDAMENTALS_KEY]
                )

        stocks = StocksFactory.load_stocks(
            tickers=tickers,
            data_source_historical=data_source_historical,
            data_source_fundamentals=data_source_fundamentals,
            bulk=conf[BULK_KEY],
            indicators=conf[INDICATORS_KEY]
        )

        return stocks

    @staticmethod
    def load_stocks(tickers=None,
                    data_source_historical=None,
                    data_source_fundamentals=None,
                    bulk=False,
                    indicators=None
                    ):

        stocks = []
        if data_source_historical is None and data_source_fundamentals is None:
            print("Error: Define your data sources first !!!.")
            return

        if bulk is True:  # print("This option has not been already programmed! wait for next release")

            stock = Stock(tickers=tickers,
                          data_source_historical=data_source_historical,
                          data_source_fundamentals=data_source_fundamentals)

            stock = StocksFactory.load_indicators(stock, indicators)
            stocks.append(stock)

        else:
            for ticker in tickers:

                if ticker.startswith("^"):
                    continue

                data_source_stock = None
                if data_source_historical is not None:
                    data_source_stock = copy.copy(data_source_historical)
                    data_source_stock.prices = pd.DataFrame()

                    data_source_stock.prices = pd.concat([data_source_historical.prices[ticker]], axis=1, keys=[ticker])

                if data_source_fundamentals is not None:
                    data_source_fundamentals_stock = copy.copy(data_source_fundamentals)

                    data_source_fundamentals_stock.fundamentals = copy.copy(data_source_fundamentals.fundamentals)

                    data_source_fundamentals_stock.fundamentals.overview_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.income_statement_ar_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.balance_sheet_ar_df = pd.DataFrame()
                    data_source_fundamentals_stock.fundamentals.cashflow_ar_df = pd.DataFrame()

                    data_source_fundamentals_stock.fundamentals.overview_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.overview_df, ticker)

                    data_source_fundamentals_stock.fundamentals.balance_sheet_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.balance_sheet_ar_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.balance_sheet_qr_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.balance_sheet_qr_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.income_statement_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.income_statement_ar_df,
                                                        ticker)

                    data_source_fundamentals_stock.fundamentals.income_statement_qr_df = \
                        StocksFactory.set_df_per_ticker(
                            data_source_fundamentals_stock.fundamentals.income_statement_qr_df, ticker)

                    data_source_fundamentals_stock.fundamentals.cashflow_ar_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.cashflow_ar_df, ticker)

                    data_source_fundamentals_stock.fundamentals.cashflow_qr_df = \
                        StocksFactory.set_df_per_ticker(data_source_fundamentals.fundamentals.cashflow_qr_df, ticker)

                else:
                    data_source_fundamentals_stock = None

                stock = Stock(tickers=[ticker],
                              data_source_historical=data_source_stock,
                              data_source_fundamentals=data_source_fundamentals_stock)

                stock = StocksFactory.load_indicators(stock, indicators)

                stocks.append(stock)

        return stocks

    @staticmethod
    def set_df_per_ticker(df, ticker):
        if df is not None:
            return pd.concat([df[ticker]], axis=1, keys=[ticker])

    @staticmethod
    def load_indicators(stock, indicators):

        if indicators is None:
            indicators = []

        for indicator in indicators:
            stock.append_indicator(indicator)

        return stock


if __name__ == '__main__':
    import datetime as dt
    from datasource.datasource import DATASOURCETYPE
    ticker_list = ["TSLA", "SPY"]
    interval = INTERVAL.DAY
    confs = {
        TICKERS_KEY: ticker_list,
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

    stock_data = StocksFactory.create_stocks(conf=confs)
    print("Final Result:\n", stock_data, stock_data[0].get_prices_data(keys={ADJ_CLOSE_KEY: True}))
