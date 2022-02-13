import abc
import pandas as pd


class ValueInvestmentMetric(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        self.tickers = None
        self.data_df = None
        self.metric_df = pd.DataFrame()
        ValueInvestmentMetric.set_ui()

    @abc.abstractmethod
    def set_input_data(self, fundamentals):
        if fundamentals is None:
            raise ValueError("Error: data not found")

    @abc.abstractmethod
    def calculate(self):
        """function to calculate the indicator"""
        if self.data_df is None or self.data_df.empty is True:
            raise ValueError("Error: Data has not been set, there is no data to calculate the metric. "
                             "Please verify the metric constructor")

    @staticmethod
    def set_ui():
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
