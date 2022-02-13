import pandas as pd


class IncomeStatement:

    def __init__(self, ticker, data):
        self.quarterly_reports = pd.DataFrame()
        self.annual_reports = pd.DataFrame()

        for report in data["quarterlyReports"]:
            self.quarterly_reports[report['fiscalDateEnding']] = \
                pd.DataFrame.from_dict(report, orient='index', columns=["data"])["data"]

        for report in data["annualReports"]:
            self.annual_reports[report['fiscalDateEnding']] = \
                pd.DataFrame.from_dict(report, orient='index', columns=["data"])["data"]

        self.quarterly_reports.columns = pd.MultiIndex.from_product([[ticker], self.quarterly_reports.columns])
        self.annual_reports.columns = pd.MultiIndex.from_product([[ticker], self.annual_reports.columns])

        self.set_data()

    def set_data(self):
        pass
