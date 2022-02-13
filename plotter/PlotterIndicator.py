import abc
import plotter.Plotter as Plotter


class PlotterIndicator(metaclass=abc.ABCMeta):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):

        self.indicator = indicator
        self.ticker = ticker

        if plotter is None:
            print("Error: plotter Object not found, please Select the main stock first.")
            raise IOError

        self.plotter = plotter
        self.main_color = color
        self.tick_y_color = color
        self.period = period

    def plot_indicator(self, axis, df=None, label=None, color=None):

        print("Plotting Indicator")

        if color is None:
            color = self.main_color

        if df is None:
            df = self.indicator.df[self.ticker][[self.indicator.indicator_key]].iloc[-self.period:, :]
        else:
            df = df.iloc[-self.period:, :]

        if label is None:
            label = self.indicator.indicator_key

        limit_y = self.calculate_limit_y(df)
        ymin = int(limit_y[0]) - 1
        ymax = int(limit_y[1]) + 1
        axis.set_ylim(ymin=ymin, ymax=ymax)

        #  Set the layout of the indicators plot
        #  Indicator plot layout
        axis.tick_params(axis='y', labelcolor=color, size=20)
        axis.grid(alpha=.4)
        axis.spines["top"].set_alpha(0.0)
        axis.spines["bottom"].set_alpha(1)
        axis.spines["right"].set_alpha(0.0)
        axis.spines["left"].set_alpha(1)

        axis.plot(
            df.index,
            df,
            color=color,
            label=label
        )

        legend_position = Plotter.Plotter.get_legend_position()
        axis.legend(loc=legend_position)

        axis.set_xlim(
            df.iloc[[0]].index,
            df.iloc[[-1]].index
        )

        return self.plotter

    def calculate_limit_y(self, series):

        max_value = series.max()
        min_value = series.min()

        return [min_value, max_value]
