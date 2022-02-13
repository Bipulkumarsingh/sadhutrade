from plotter.PlotterIndicator import PlotterIndicator

import plotter.Plotter as Plotter
import matplotlib.patches as ppatches

import matplotlib.pyplot as plt


class PlotterRENKO(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)

    def plot(self, axis):
        self.plot_indicator(
            axis=axis,
            df=self.indicator.df
        )

        return self.plotter

    def plot_indicator(self, axis, df=None, label=None, color=None):

        if color is None:
            color = 'green'

        key_close = "close"
        uptrend_key = "uptrend"
        date_key = "date"

        lim_y_min = min(df[self.ticker].loc[:, key_close]) - 100
        lim_y_max = max(df[self.ticker].loc[:, key_close]) + 100

        prev_num = -1
        y0 = df[self.ticker].loc[0, key_close]

        uptrend = df[self.ticker].loc[:, [uptrend_key]]
        date = df[self.ticker].loc[:, date_key]

        bricks = []

        for index, delta in uptrend.iterrows():
            if delta.loc["uptrend"] == True:
                bricks.extend([1] * 1)
            else:
                bricks.extend([-1] * 1)

        for index, number in enumerate(bricks):
            if number == 1:
                facecolor = color
            else:
                facecolor = 'red'

            prev_num += number

            renko = ppatches.Rectangle(
                (index, prev_num * self.indicator.brick_size + y0),
                1,
                self.indicator.brick_size,
                facecolor=facecolor, alpha=0.5
            )
            axis.add_patch(renko)

        axis.set_ylim(lim_y_min, lim_y_max)

        axis.tick_params(axis='y', labelcolor=color, size=20)

        legend_position = Plotter.Plotter.get_legend_position()

        # Use the pyplot interface to change just one subplot...
        plt.sca(axis)
        plt.xticks(range(date.count()), date.apply(str), rotation=90)

        lim_x_min = 0
        lim_x_max = date.count()

        axis.set_xlim(lim_x_min, lim_x_max)

        axis.legend(["RENKO"], loc=legend_position)

    def plot_renko(self, data, brick_size):

        lim_y_min = min(data.loc[:, "close"]) - 100
        lim_y_max = max(data.loc[:, "close"]) + 100

        prev_num = -1
        y0 = data.loc[0, "close"]

        uptrend = data.loc[:, ["uptrend"]]
        date = data.loc[:, "date"]

        fig = plt.figure(2)
        fig.clf()
        axes = fig.gca()

        bricks = []

        for index, delta in uptrend.iterrows():
            if delta.loc["uptrend"] == True:
                bricks.extend([1] * 1)
            else:
                bricks.extend([-1] * 1)

        for index, number in enumerate(bricks):
            if number == 1:
                facecolor = 'green'
            else:
                facecolor = 'red'

            prev_num += number

            renko = ppatches.Rectangle(
                (index, prev_num * self.indicator.brick_size + y0),
                1,
                self.indicator.brick_size,
                facecolor=facecolor,
                alpha=0.5
            )
            axes.add_patch(renko)

            print("x: {} y:{}, width:{}, height:{} ".format(
                index, prev_num * brick_size, 1, brick_size)
            )

        plt.xticks(range(date.count()), date, rotation=90)
        axes.set_ylim(lim_y_min, lim_y_max)

        lim_x_min = 0
        lim_x_max = date.count()

        axes.set_xlim(lim_x_min, lim_x_max)

        # plt.show()
