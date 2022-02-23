import abc
from src.constants import DATASOURCETYPE
from fundamentals.fundamentals import FUNDAMENTALSTYPE


class Strategy(metaclass=abc.ABCMeta):

    def __init__(self):
        self.dst_historical = None
        self.dst_fundamentals = None
        self.period = None
        self.start_date = None
        self.end_date = None
        self.interval = None
        self.indicators = []
        self.kpis = []
        self.methods_kpis = []
        self.methods = []
        self.reports = []
        self.fundamentals_options = [FUNDAMENTALSTYPE.BALANCE_SHEET,
                                     FUNDAMENTALSTYPE.INCOME_STATEMENT,
                                     FUNDAMENTALSTYPE.CASH_FLOW]
        self.value_investing_metrics = []

        self.kpis = []
        self.methods = []

        # 0: run the normal flow
        # 1: force new data to be requested from server
        # 2. force cached data
        self.force_fundamentals = 0

        # Force bulk- i.e. Magic formula
        self.bulk = None

    @abc.abstractmethod
    def set_data_source_types(self):
        self.dst_historical = DATASOURCETYPE.YFINANCE
        self.dst_fundamentals = DATASOURCETYPE.ALPHA

    def set_date_parameters(self):
        pass
