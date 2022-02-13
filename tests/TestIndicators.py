import unittest

# import datetime
# import matplotlib.pyplot as plt
# from plotter.Plotter import Plotter
# from strategy.strategy_manager import StrategyManager
# from strategy.strategy_builder import StrategyBuilder


DEVELOPMENT = True


class TestIndicators(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True
    stock = None
    stocks_factory = None

    @staticmethod
    def truncate(n):
        return int(n * 1000) / 1000


if __name__ == '__main__':
    unittest.main()
