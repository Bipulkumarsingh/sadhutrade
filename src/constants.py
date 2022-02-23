import json
from enum import Enum
from requests import get as req_get
from os.path import dirname, abspath

ROOT_DIR = dirname(dirname(abspath(__file__)))

PRICES_KEY = 'prices'
TICKERS_KEY = 'tickers'
INPUT_DF_KEY = 'input_df'
ADJ_CLOSE_KEY = 'Adj Close'
HIGH_KEY = 'High'
LOW_KEY = 'Low'
OPEN_KEY = 'Open'
CLOSE_KEY = 'Close'
VOLUME_KEY = 'Volume'
RET_KEY = 'Ret'
START_DATE_KEY = 'start_date'
END_DATE_KEY = 'end_date'
CUM_RETURN_KEY = 'cum_return'
HISTORICAL_KEY = 'has_historical_data'
FUNDAMENTALS_KEY = 'has_fundamentals_data'
PERIOD_KEY = 'period'
INTERVAL_KEY = 'interval'
INDICATORS_KEY = 'indicators'
BULK_KEY = 'bulk'
FUNDAMENTALS_OPTIONS_KEY = 'fundamentals_options'
FORCE_FUNDAMENTALS_KEY = 'force_fundamentals'

# KPIS KEYS
CAGR_KEY = 'cagr'
CALMR_KEY = 'calmar'
MAX_DRAWDOWN_KEY = 'max_drawdown'
VOLATILITY_KEY = 'volatility'
NEG_VOLATILITY_KEY = 'neg_volatility'
SHARPE_KEY = 'sharpe'
SORTINO_KEY = 'sortino'
ATR_KEY = 'ATR'


class DATASOURCETYPE(Enum):
    YFINANCE = 1
    SMARTAPI = 2
    ALPHA = 3


# intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
class INTERVAL(Enum):
    MINUTE = '1m'
    MINUTE2 = '2m'
    MINUTE5 = '5m'
    MINUTE15 = '15m'
    MINUTE30 = '30m'
    MINUTE60 = '60m'
    MINUTE90 = '90m'
    HOUR = '1h'
    DAY = '1d'
    DAY5 = '5d'
    WEEK = '1wk'
    MONTH = '1mo'
    MONTH3 = '3mo'


# periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
class PERIOD(Enum):
    DAY = '1d'
    DAY5 = '5d'
    MONTH = '1mo'
    MONTH3 = '3mo'
    MONTH6 = '6mo'
    YEAR = '1y'
    YEAR2 = '2y'
    YEAR5 = '5y'
    YEAR10 = '10y'
    YTD = 'ytd'
    MAX = 'max'


def get_config(key: str) -> dict:
    """
        Return configuration which contains user cred, api token or other sensitive information for selected key.
        Parameter:
            key: int (Ex: angelOne)
        Return:
            config in the form of dict.
    """
    json_filename = f"{ROOT_DIR}/config/config.json"
    with open(json_filename, "r") as f:
        return json.load(f)[key]


def get_instruments():
    instrument_dump = req_get(
        url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")
    instrument_dump = instrument_dump.json()
    with open(f"{ROOT_DIR}/config/instruments.json", 'w') as file:
        json.dump(instrument_dump, file)


def instrument_records(key: str):
    with open(f'{key}.json', 'r') as file:
        instrument_dump = json.load(file)
        return instrument_dump
