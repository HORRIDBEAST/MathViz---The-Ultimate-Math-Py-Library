"""
Tests for StatsVisualizer (mathviz/concepts.py)
"""
import pytest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


@pytest.fixture
def viz():
    from mathviz import StatsVisualizer
    return StatsVisualizer()


class TestStatsVisualizerInit:
    def test_is_mathviz_subclass(self):
        from mathviz import StatsVisualizer, MathViz
        v = StatsVisualizer()
        assert isinstance(v, MathViz)

    def test_default_figsize(self, viz):
        assert viz.figsize == (12, 8)


class TestHypothesisTester:
    def test_returns_figure(self, viz):
        fig = viz.hypothesis_tester()
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_expected_sliders_exist(self, viz):
        viz.hypothesis_tester()
        expected = {'sample size n', 'effect size d', 'alpha'}
        assert expected.issubset(set(viz.sliders.keys()))

    def test_title_is_set(self, viz):
        fig = viz.hypothesis_tester()
        assert 'Hypothesis Tester' in fig.axes[0].get_title()


class TestBayesianUpdater:
    def test_returns_figure(self, viz):
        fig = viz.bayesian_updater()
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_expected_sliders_exist(self, viz):
        viz.bayesian_updater()
        expected = {'prior α', 'prior β', 'flips n', 'heads k'}
        assert expected.issubset(set(viz.sliders.keys()))

    def test_title_is_set(self, viz):
        fig = viz.bayesian_updater()
        assert 'Bayesian Updater' in fig.axes[0].get_title()
