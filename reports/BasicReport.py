from reports.Report import Report
import pprint


class BasicReport(Report):

    def __init__(self):
        super().__init__()

    def generate(self, data):
        report_data = {}
        ticker_kpi_data = {}

        for stock in data:
            for ticker in stock.tickers:
                ticker_kpi_data[ticker] = dict()

                for kpi_result in stock.kpis:
                    ticker_kpi_data[ticker][kpi_result.name] = kpi_result.result[ticker]

        report_data["kpi"] = ticker_kpi_data

        return report_data

    def print(self, data):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
