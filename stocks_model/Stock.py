from src.constants import HIGH_KEY, LOW_KEY, OPEN_KEY, CLOSE_KEY, ADJ_CLOSE_KEY, VOLUME_KEY


class Stock:

    # Put here an enum and a case with the enum
    def __init__(self,
                 tickers=None,
                 data_source_historical=None,
                 data_source_fundamentals=None):

        if tickers is None:
            print("Error: Define your tickers first !!!.")
            raise ValueError

        self.tickers = tickers

        self.error = None
        self.fundamentals = None
        self.data_source_historical = data_source_historical

        self.price_info = None

        self.indicators = []
        self.value_investing_metrics = []
        self.kpis = []

        if data_source_historical is not None:
            self.get_prices_data()

        self.data_source_fundamentals = data_source_fundamentals
        if data_source_fundamentals is not None:
            self.get_fundamentals()

        print("Stock {} created".format(tickers))

    def get_fundamentals(self):

        self.fundamentals = self.data_source_fundamentals.fundamentals

    @staticmethod
    def get_key_titles(keys):

        key_titles = []
        for key in keys:
            if keys[key] is True:
                key_titles.append(key)

        return key_titles

    # Tickers parameter should be a sub-set of self.tickers
    def get_prices_data(self, keys=None):

        if keys is None or len(keys) == 0:
            print("No keys has been specified. All keys were selected. ")

            keys = {HIGH_KEY: True,
                    LOW_KEY: True,
                    OPEN_KEY: True,
                    CLOSE_KEY: True,
                    ADJ_CLOSE_KEY: True,
                    VOLUME_KEY: True
                    }

        method_tag = "get_prices_data"

        if self.data_source_historical is not None:
            if self.data_source_historical.prices is None or self.data_source_historical.prices.empty is True:
                raise ValueError("No historical data available, call method self.get_historical_data() first")

            key_titles = self.get_key_titles(keys)

            if len(key_titles) > 0:
                prices = self.data_source_historical.get_prices(self.tickers, key_titles)
            else:
                print("{} - There are no prices information, for ticker:{}".format(method_tag, self.tickers))
                raise ValueError

        else:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        # Validate Price dataframe
        if prices.empty:
            print("There has been an error in {}".format(method_tag))
            raise ValueError

        self.price_info = prices
        return prices

    def append_indicator(self, new_indicator=None, params=None):

        # if get_historical_data has already been called it returns the cached data
        if params is None:
            params = []

        new_indicator.set_input_data(self.price_info, params)
        new_indicator.calculate()

        self.indicators.append(new_indicator)

    def append_value_investing_metric(self, new_metric=None):

        # if get_historical_data has already been called it returns the cached data
        new_metric.set_input_data(self.fundamentals)
        new_metric.calculate()

        self.value_investing_metrics.append(new_metric)

    def append_kpis(self, new_kpis=None):

        # if get_historical_data has already been called it returns the cached data
        kpi_value = new_kpis.calculate(self.price_info)

        self.kpis.append(kpi_value)

    def get_statistical_data(self, period):
        pass

    def print(self):
        for kpi in self.kpis:
            kpi.print()
