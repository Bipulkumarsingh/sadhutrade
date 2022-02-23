import abc
import datetime
from src.constants import INTERVAL
from src.logger import set_up_logging

log = set_up_logging()


class DataSource(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @staticmethod
    def validate_dates(dates=None):

        if dates is None:
            raise ValueError("Wrong input parameters, Verify your code!!!")

        if dates["end_date"] is None:
            raise ValueError("Error: end_date is None, Set a valid end date.")

        if dates["period"] is None and dates["start_date"] is None:
            raise ValueError("Error: Please set start_date or period")

        if dates["period"] is None:
            dates["period"] = "max"
        else:
            dates["start_date"] = None
            dates["end_date"] = None

        if dates["start_date"] is not None:
            if dates["start_date"] > dates["end_date"]:
                raise ValueError("Error:  Start_date should be earlier than end date")

        elif dates["time_delta"] is not None and dates["time_delta"] > 0:
            dates["start_date"] = datetime.datetime.today() - datetime.timedelta(dates["time_delta"])
        else:
            raise ValueError("Error: Neither the Start_date nor the time_delta were defined ")

        return True

    @staticmethod
    def get_tickers_str(tickers):

        tickers_str = ""
        for ticker in tickers:
            tickers_str = tickers_str + " " + ticker

        return tickers_str

    @abc.abstractmethod
    def extract_historical_data(self, tickers=None, start_date=None, end_date=(datetime.date.today()),
                                period=None, interval=INTERVAL.DAY, time_delta=None):

        if tickers is None:
            log.info("Tickers are None, please define your tickers")
            raise AttributeError

    @abc.abstractmethod
    def get_prices(self, tickers, key_titles):
        pass

    @abc.abstractmethod
    def extract_fundamentals(self, tickers, required_elements):
        pass
