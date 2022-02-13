# from stocks_model.StocksFactory import StocksFactory


class StrategyManager:

    @staticmethod
    def run_strategy(strategy, stocks):
        results = {}
        if not strategy.methods:
            return stocks

        for method in strategy.methods:
            results[method.name] = method.back_test(stocks, strategy.methods_kpis)

        return strategy.methods

    @staticmethod
    def run_report(strategy, results):

        reports_data = {}
        if not strategy.reports:
            return results

        for report in strategy.reports:
            reports_data = report.generate(results)

        return reports_data
