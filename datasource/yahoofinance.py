import datetime
import pandas as pd
import yfinance as yf
from src.constants import INTERVAL, PERIOD


class YFinanceDataSource:

    def __init__(self):
        super().__init__()
        self.prices = pd.DataFrame()

    def extract_historical_data(self, tickers=None, start_date=None, end_date=(datetime.date.today()),
                                period=None, interval=INTERVAL.DAY, time_delta=None):

        valid_parameters = YFinanceDataSource.validate_parameters(
                start_date=start_date,
                end_date=end_date,
                time_delta=time_delta,
                period=period,
                interval=interval
            )

        if valid_parameters is False:
            raise ValueError("The proposed dates are not correct, Verify your code!!!")

        tickers_str = self.get_tickers_str(tickers)
        self.prices = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers=tickers_str,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period=period,

            start=start_date,

            end=end_date,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval=interval.value,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by='ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust=False,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost=True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads=True,

            # proxy URL scheme use when downloading?
            # (optional, default is None)
            proxy=None
        )
        self.prices.dropna(axis='columns', how="all", inplace=True)
        self.prices.dropna(axis='rows', how="all", inplace=True)

        self.prices.bfill(axis=0, inplace=True)

        if len(tickers) == 1:
            self.prices.columns = pd.MultiIndex.from_product([tickers, self.prices.columns])

        return self.prices

    @staticmethod
    def validate_parameters(start_date=None,
                            end_date=datetime.date.today(),
                            time_delta=None,
                            period=None,
                            interval=None):

        dates = {"start_date": start_date,
                 "end_date": end_date,
                 "time_delta": time_delta,
                 "period": period,
                 "error": None}

        result = \
            DataSource.validate_dates(dates)

        # Intra-day intervals
        if interval is INTERVAL.MINUTE or \
                interval is INTERVAL.MINUTE2 or \
                interval is INTERVAL.MINUTE5 or \
                interval is INTERVAL.MINUTE15 or \
                interval is INTERVAL.MINUTE30 or \
                interval is INTERVAL.MINUTE60 or \
                interval is INTERVAL.MINUTE90 or \
                interval is INTERVAL.HOUR:

            if start_date is None and end_date is None:

                if period is not PERIOD.DAY or \
                        period is not PERIOD.DAY5 or \
                        period is not PERIOD.MONTH:
                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    result = False
            else:
                delta = (end_date - start_date).seconds

                max_days = 60 * 24 * 60 * 60
                if delta > max_days:
                    print("For Intra-day you have a maximum of 60 days of data, please adjust your dates!")
                    result = False

        return result

    def extract_fundamentals(self, tickers, date, required_elements=None, force_server_data=0):
        pass

    def get_prices(self, tickers, key_titles):

        if len(key_titles) == 0:
            print("No valid keys were requested returning empty dataframe")
            return pd.DataFrame()

        bool_titles = self.prices.columns.get_level_values(1).isin(key_titles)
        return self.prices.loc[:, bool_titles]
