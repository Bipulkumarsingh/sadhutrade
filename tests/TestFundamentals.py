import unittest

DEVELOPMENT = True


class TestBasics(unittest.TestCase):
    data_source_type = None
    tickers = None
    fundamentals = True
    historical_data = True

    stock = None

    def test_magic_formula(self):
        pass


if __name__ == '__main__':
    unittest.main()
