import unittest

from plotter.Plotter import Plotter


class TestPlotter(unittest.TestCase):

    def test_legend(self):
        plotter = Plotter()
        assert plotter.get_legend_position() == "upper left"
        assert plotter.get_legend_position() == "upper center"
        assert plotter.get_legend_position() == "upper right"
        assert plotter.get_legend_position() == "center left"
        assert plotter.get_legend_position() == "lower left"
        assert plotter.get_legend_position() == "lower center"
        assert plotter.get_legend_position() == "lower right"
        assert plotter.get_legend_position() == "center right"
        assert plotter.get_legend_position() == "center"
        assert plotter.get_legend_position() == "right"
        assert plotter.get_legend_position() == "upper left"
        assert plotter.get_legend_position() == "upper center"


if __name__ == '__main__':
    unittest.main()
