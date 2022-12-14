import falcon
from json import loads, dumps


# from src.constants import *
# from datasource.angelone import AngelOne
# from strategy.pattern_scanner import candle_pattern
# from stocks_model.StocksFactory import StocksFactory
# from src.constants import DATASOURCETYPE


class Home:
    @staticmethod
    def on_get(req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = 'working fine!'

    # def on_post(self, req, resp):
    #     temp = req.stream.read()
    #     context = req.context
    #     temp = json.loads(temp)


# class SignificantStock:
#     @staticmethod
#     async def on_get(req, resp):
#         tickers = get_config(key='tickers')
#         smart_api = AngelOne(tickers)
#         data = {}
#         for count, ticker in enumerate(tickers):
#             try:
#                 ohlc = smart_api.historical_data(ticker=ticker[1], interval='FIVE_MINUTE', period=5)
#                 ohlc_day = smart_api.historical_data(ticker=ticker[1], interval='ONE_DAY', period=30)
#                 # ohlc_day = ohlc_day.iloc[:-1, :]
#                 cp = candle_pattern(ohlc, ohlc_day)
#                 print(ticker[0], ": ", cp)
#                 data[ticker[0]] = cp
#             except Exception as ex:
#                 print("skipping for ", ticker[0], f"\n{ex}")
#         resp.status = falcon.HTTP_200
#         # resp.content_type = falcon.MEDIA_TEXT
#         resp.text = data

#
# def yahooFinance():
#     import datetime as dt
#     from dateutil.relativedelta import relativedelta
#     tickers = get_config(key='tickers')
#     tickers = [ticker[0].replace('-EQ', '.NS') for ticker in tickers]
#     tickers = tickers[:5]
#     interval = INTERVAL.DAY
#     conf = {
#         TICKERS_KEY: tickers,
#         HISTORICAL_KEY: DATASOURCETYPE.YFINANCE,
#         FUNDAMENTALS_KEY: None,
#         FUNDAMENTALS_OPTIONS_KEY: [],
#         FORCE_FUNDAMENTALS_KEY: False,
#         INDICATORS_KEY: [],
#         START_DATE_KEY: dt.date.today() - relativedelta(days=32),
#         END_DATE_KEY: dt.date.today() - relativedelta(days=2),
#         INTERVAL_KEY: interval,
#         PERIOD_KEY: None,
#         BULK_KEY: True
#
#     }
#     stocks = StocksFactory.create_stocks(conf=conf)
#     ohlc_day = stocks[0].get_prices_data()
#
#     conf[INTERVAL_KEY] = interval.MINUTE5
#     conf[START_DATE_KEY] = dt.date.today() - relativedelta(days=7)
#     conf[END_DATE_KEY] = dt.date.today() - relativedelta(days=2)
#
#     stocks = StocksFactory.create_stocks(conf=conf)
#     ohlc = stocks[0].get_prices_data()
#
#     for ticker in tickers:
#         cp = candle_pattern(ohlc[ticker], ohlc_day[ticker])
#         print(ticker, ": ", cp)

#
# if __name__ == '__main__':
#     # yahooFinance()
#     pass

# # Continuous execution
# start_time = time.time()
# timeout = time.time() + 60 * 60 * 1  # 60 seconds times 60 meaning the script will run for 1 hr
# while time.time() <= timeout:
#     try:
#         print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#         main()
#         time.sleep(300 - ((time.time() - start_time) % 300.0))  # 300 second interval between each new execution
#     except KeyboardInterrupt:
#         print('\n\nKeyboard exception received. Exiting.')
#         exit()
