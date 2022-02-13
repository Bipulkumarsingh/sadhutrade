# import matplotlib.pyplot as plt
# from pandas.plotting import register_matplotlib_converters
from plotter.PlotterIndicator import PlotterIndicator


class PlotterBollingerBands(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)

    def plot(self, axis):
        print("Plotting Bollinger Bands")

        self.plot_indicator(
            axis=axis,
            df=self.indicator.df[self.ticker][[self.indicator.bb_down_key]],
            label="BB",
            color="tab:red"
        )

        self.plot_indicator(
            axis=axis,
            df=self.indicator.df[self.ticker][[self.indicator.bb_up_key]],
            label="BB",
            color="tab:red"
        )

    def plot_indicator(self, axis, df=None, label=None, color=None):
        print("Plotting Indicator")

        if color is None:
            color = self.main_color

        df = df.iloc[-self.period:, :]

        axis.plot(
            df.index,
            df,
            color=color
        )

        return self.plotter
