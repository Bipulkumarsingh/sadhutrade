import pandas as pd


class Overview:

    def __init__(self, ticker, data):
        self.data = pd.DataFrame.from_dict(data, orient='index', columns=["data"])

        self.data.columns = pd.MultiIndex.from_product([[ticker], self.data.columns])

        self.set_data()

    def set_data(self):
        self.get_ticker()

    def get_ticker(self):
        return self.data.loc["Symbol"][0]

    def get_AssetType(self):
        return self.data["AssetType"]

    def get_Name(self):
        return self.data["Name"]

    def get_Description(self):
        return self.data["Description"]

    def get_Exchange(self):
        return self.data["Exchange"]

    def get_Currency(self):
        return self.data["Currency"]

    def get_Country(self):
        return self.data["Country"]

    def get_Sector(self):
        return self.data["Sector"]

    def get_Industry(self):
        return self.data["Industry"]

    def get_Address(self):
        return self.data["Address"]

    def get_FullTimeEmployees(self):
        return self.data["FullTimeEmployees"]

    def get_FiscalYearEnd(self):
        return self.data["FiscalYearEnd"]

    def get_LatestQuarter(self):
        return self.data["LatestQuarter"]

    def get_MarketCapitalization(self):
        return self.data["MarketCapitalization"]

    def get_EBITDA(self):
        return self.data["EBITDA"]

    def get_PERatio(self):
        return self.data["PERatio"]

    def get_PEGRatio(self):
        return self.data["PEGRatio"]

    def get_BookValue(self):
        return self.data["BookValue"]

    def get_DividendPerShare(self):
        return self.data["DividendPerShare"]

    def get_DividendYield(self):
        return self.data["DividendYield"]

    def get_EPS(self):
        return self.data["EPS"]

    def get_RevenuePerShareTTM(self):
        return self.data["RevenuePerShareTTM"]

    def get_ProfitMargin(self):
        return self.data["ProfitMargin"]

    def get_OperatingMarginTTM(self):
        return self.data["OperatingMarginTTM"]

    def get_ReturnOnAssetsTTM(self):
        return self.data["ReturnOnAssetsTTM"]

    def get_ReturnOnEquityTTM(self):
        return self.data["ReturnOnEquityTTM"]

    def get_RevenueTTM(self):
        return self.data["RevenueTTM"]

    def get_GrossProfitTTM(self):
        return self.data["GrossProfitTTM"]

    def get_DilutedEPSTTM(self):
        return self.data["DilutedEPSTTM"]

    def get_QuarterlyEarningsGrowthYOY(self):
        return self.data["QuarterlyEarningsGrowthYOY"]

    def get_QuarterlyRevenueGrowthYOY(self):
        return self.data["QuarterlyRevenueGrowthYOY"]

    def get_AnalystTargetPrice(self):
        return self.data["AnalystTargetPrice"]

    def get_TrailingPE(self):
        return self.data["TrailingPE"]

    def get_ForwardPE(self):
        return self.data["ForwardPE"]

    def get_PriceToSalesRatioTTM(self):
        return self.data["PriceToSalesRatioTTM"]

    def get_PriceToBookRatio(self):
        return self.data["PriceToBookRatio"]

    def get_EVToRevenue(self):
        return self.data["EVToRevenue"]

    def get_EVToEBITDA(self):
        return self.data["EVToEBITDA"]

    def get_Beta(self):
        return self.data["Beta"]

    def get_52WeekHigh(self):
        return self.data["52WeekHigh"]

    def get_52WeekLow(self):
        return self.data["52WeekLow"]

    def get_50DayMovingAverage(self):
        return self.data["50DayMovingAverage"]

    def get_200DayMovingAverage(self):
        return self.data["200DayMovingAverage"]

    def get_SharesOutstanding(self):
        return self.data["SharesOutstanding"]

    def get_SharesFloat(self):
        return self.data["SharesFloat"]

    def get_SharesShort(self):
        return self.data["SharesShort"]

    def get_SharesShortPriorMonth(self):
        return self.data["SharesShortPriorMonth"]

    def get_ShortRatio(self):
        return self.data["ShortRatio"]

    def get_ShortPercentOutstanding(self):
        return self.data["ShortPercentOutstanding"]

    def get_ShortPercentFloat(self):
        return self.data["ShortPercentFloat"]

    def get_PercentInsiders(self):
        return self.data["PercentInsiders"]

    def get_PercentInstitutions(self):
        return self.data["PercentInstitutions"]

    def get_ForwardAnnualDividendRate(self):
        return self.data["ForwardAnnualDividendRate"]

    def get_ForwardAnnualDividendYield(self):
        return self.data["ForwardAnnualDividendYield"]

    def get_PayoutRatio(self):
        return self.data["PayoutRatio"]

    def get_DividendDate(self):
        return self.data["DividendDate"]

    def get_ExDividendDate(self):
        return self.data["ExDividendDate"]

    def get_LastSplitFactor(self):
        return self.data["LastSplitFactor"]

    def get_LastSplitDate(self):
        return self.data["LastSplitDate"]
