from plotter.PlotterIndicator import PlotterIndicator
import plotter.Plotter as Plotter


class PlotterPortfolio(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)
        self.signal_color = "tab:orange"

    def plot(self, axis):

        print("Plotting Portfolio")

        self.plot_indicator(
            axis=axis,
            df=self.indicator.df[self.ticker][[self.indicator.signal_key]],
            label=self.indicator.signal_key,
            color=self.signal_color
        )

        Plotter.Plotter.legend_id -= 1
        self.plot_indicator(
            axis=axis
        )

        return self.plotter

    def plot_indicator(self, axis, df=None, label=None, color=None):

        print("Plotting Indicator")

        if color is None:
            color = self.main_color

        if df is None:
            df = \
                self.indicator.df[self.ticker][[self.indicator.indicator_key]].iloc[-self.period:, :]
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
