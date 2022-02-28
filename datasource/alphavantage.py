import os
import time
import json
import datetime
import pandas as pd
from src.logger import set_up_logging
from src.request_handler import get_data
from src.constants import ROOT_DIR, INTERVAL
from fundamentals.fundamentals import Fundamentals


log = set_up_logging()


class AlphaAPIDataSource:
    _AV_API_URL = "https://www.alphavantage.co/query"
    _FUNCTION = "function"
    _SYMBOL = "symbol"
    _API_KEY = "apikey"

    # TODO: replace API KEY with your key
    _AV_API_KEY = "########"
    _AV_KEY_INDICATOR = 0

    def __init__(self, proxy=None):

        super().__init__()

        self.prices = pd.DataFrame()
        self.fundamentals = None

        self.proxy = proxy

        self.url = None
        self.current_api_key = None

    @staticmethod
    def get_max_rate_per_min():
        return 5

    # Form the base url, the original function called must return
    # the function name defined in the alpha vantage api and the data
    # key for it and for its metadata.
    @staticmethod
    def calculate_url(ticker, function):

        url = "{}?{}={}&{}={}&{}={}".format(
            AlphaAPIDataSource._AV_API_URL,
            AlphaAPIDataSource._FUNCTION,
            function.name,
            AlphaAPIDataSource._SYMBOL,
            ticker,
            AlphaAPIDataSource._API_KEY,
            AlphaAPIDataSource._AV_API_KEY

        )
        log.info(url)
        return url

    @staticmethod
    def save_record(ticker, element, response):

        folder_path = os.path.join(ROOT_DIR, 'data', 'av_cache')
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        file_path = os.path.join(folder_path, '{}_{}.txt'.format(ticker, element))
        with open(file_path, 'w') as outfile:
            json.dump(response, outfile)

    @staticmethod
    def load_cached_data(ticker, element):

        file_path = os.path.join(ROOT_DIR, 'data', 'av_cache', '{}_{}.txt'.format(ticker, element))
        try:
            with open(file_path, 'r') as json_data_file:
                response = json.load(json_data_file)

        except FileNotFoundError:
            log.info("File Not Found")
            response = None
        except Exception as ex:
            log.exception(ex)
            response = None
        return response
        # Todo: return true if successful and if false do http request to get the data from the server

    def extract_fundamentals(self, tickers, date, required_elements=None, force_server_data=0):

        num_requests = 1
        fix_data = 0

        if required_elements is None:
            raise ValueError("No fundamentals selected, please check your code")

        self.fundamentals = Fundamentals()

        for ticker in tickers:

            i = 0
            while i < len(required_elements):
                element = required_elements[i]

                if ticker.startswith("^"):
                    i += 1
                    continue

                response = None
                if force_server_data == 0 and fix_data == 0:
                    response = self.load_cached_data(ticker, element)
                    if response is not None:
                        result = self.fundamentals.process_data(ticker, element, response)

                        # This means that the file loaded is not correct and the correct file
                        # should be picked from the server
                        if result is False:
                            fix_data = 1
                            continue

                if response is None:
                    url = self.calculate_url(ticker, element)
                    try:
                        response = get_data(url=url, proxy=self.proxy, treat_info_as_error=True)

                        AlphaAPIDataSource.save_record(ticker, element, response)

                    except Exception as ex:
                        log.exception(ex)

                        time.sleep(61)

                    # TODO: This can be severely optimized and in a thread run and with a production api key
                    if num_requests >= AlphaAPIDataSource.get_max_rate_per_min():
                        time.sleep(61)
                        num_requests = 0

                    num_requests += 1

                    self.fundamentals.process_data(ticker, element, response)

                log.info(response)

                i += 1
                fix_data = 0

    def extract_historical_data(self, tickers=None, start_date=None, end_date=(datetime.date.today()),
                                time_delta=None, period=None, interval=INTERVAL.DAY):

        pass

    def validate_parameters(self):
        pass

    def get_prices(self, tickers, key_titles):
        pass
