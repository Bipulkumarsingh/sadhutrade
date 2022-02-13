import datetime as dt
from src.constants import *
from library.kpi import *
from library.indicators import *
from library.candlesticks import *
from strategy.strategy import Strategy
from reports.BasicReport import BasicReport
from datasource.datasource import DATASOURCETYPE


class StrategyBuilder(Strategy):
    def __init__(self):
        super().__init__()
        self.set_data_source_types()
        self.set_date_parameters()
        # self.set_indicators()
        # self.set_kpi()
        # self.set_report()

    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = None

    # If period is not None it will precede over date
    def set_date_parameters(self):
        self.period = None
        self.end_date = dt.datetime.today()
        date_str = "11/07/2019"
        self.start_date = dt.datetime.strptime(date_str, "%d/%m/%Y")
        self.interval = INTERVAL.DAY

    def strategyC(self):
        macd_obj = MACD(fast_period=12, slow_period=26, signal_period=9)
        atr_obj = ATR(n=14)
        self.indicators = [macd_obj, atr_obj]

    def strategyCI(self):
        macd_obj = MACD(fast_period=12, slow_period=26, signal_period=9)
        rsi_obj = RSI(n=14)
        self.indicators = [rsi_obj, macd_obj]

    def strategyCII(self):
        macd_obj = MACD(fast_period=12, slow_period=26, signal_period=9)
        rsi_obj = RSI(n=14)
        bb_obj = BollingerBands(n=20)
        atr_obj = ATR(n=14)
        adx_obj = ADX(n=14)
        obv_obj = OBV(n=14)
        self.indicators = [bb_obj, macd_obj, rsi_obj, atr_obj, adx_obj, obv_obj]

    def strategyCIII(self):
        renko_obj = RENKOIND(n=120)
        macd_obj = MACD(fast_period=12, slow_period=26, signal_period=9)
        self.indicators = [macd_obj, renko_obj]

    def strategyII(self):
        bb_obj = BollingerBands(n=20)
        self.indicators = [bb_obj]

    def strategyIII(self):
        macd_obj = MACD(fast_period=12, slow_period=26, signal_period=9)
        self.indicators = [macd_obj]

    def strategyIV(self):
        atr_obj = ATR(n=14)
        self.indicators = [atr_obj]

    def strategyV(self):
        rsi_obj = RSI(n=14)
        self.indicators = [rsi_obj]

    def strategyVI(self):
        adx_obj = ADX(n=14)

        self.indicators = [adx_obj]

    def strategyVII(self):
        obv_obj = OBV(n=14)

        self.indicators = [obv_obj]

    def strategyVIII(self):
        renko_obj = RENKOIND(n=120)

        self.indicators = [renko_obj]

    def strategyIX(self):
        rsi_obj = RSI(n=14)
        slope_obj = Slope(n=5)
        self.indicators = [rsi_obj, slope_obj]

    def strategyX(self):
        renko_obj = RENKOIND(n=120)

        self.indicators = [renko_obj]

    def strategyXI(self):
        self.indicators = []

    def kpi_XX(self):
        params_cagr = {'period': self.interval}
        cagr_obj = CAGR(params_cagr)

        params_calmar = {'period': self.interval}
        calmar_obj = Calmar(params_calmar)

        md_obj = MaxDrawDown()

        params_sharpe = {'rf': 0.0144, 'period': self.interval}
        sharpe_obj = Sharpe(params_sharpe)

        params_sortino = {'rf': 0.0144, 'period': self.interval}
        sortino_obj = Sortino(params_sortino)

        params_volatility = {'negative': False, 'period': self.interval}
        volatility_obj = Volatility(params_volatility)

        self.kpis = [cagr_obj, calmar_obj, md_obj, sharpe_obj, sortino_obj, volatility_obj]

    def kpi_XXII(self):
        calmar_obj = Calmar()
        self.kpis = [calmar_obj]

    def kpi_XXIII(self):
        md_obj = MaxDrawDown()
        self.kpis = [md_obj]

    def kpi_XXIV(self):
        sharpe_obj = Sharpe()
        self.kpis = [sharpe_obj]

    def kpi_XXV(self):
        sortino_obj = Sortino()
        self.kpis = [sortino_obj]

    def kpi_XXVI(self):
        volatility_obj = Volatility()
        self.kpis = [volatility_obj]

    def set_report(self):
        report = BasicReport()
        self.reports = [report]
