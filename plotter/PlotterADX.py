from plotter.PlotterIndicator import PlotterIndicator


class PlotterADX(PlotterIndicator):

    def __init__(self, plotter, indicator, ticker, period, color="tab:green"):
        super().__init__(plotter, indicator, ticker, period, color)

    def plot(self, axis):
        self.plot_indicator(axis)
        return self.plotter
