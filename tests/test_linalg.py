"""
Tests for LinAlgVisualizer (mathviz/concepts.py)
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
    from mathviz import LinAlgVisualizer
    return LinAlgVisualizer()


class TestLinAlgVisualizerInit:
    def test_is_mathviz_subclass(self):
        from mathviz import LinAlgVisualizer, MathViz
        v = LinAlgVisualizer()
        assert isinstance(v, MathViz)

    def test_default_figsize(self, viz):
        assert viz.figsize == (10, 10)

    def test_custom_figsize(self):
        from mathviz import LinAlgVisualizer
        v = LinAlgVisualizer(figsize=(8, 8))
        assert v.figsize == (8, 8)

    def test_exported_from_package(self):
        from mathviz import LinAlgVisualizer
        v = LinAlgVisualizer()
        assert v is not None


class TestSpaceTransformer:
    def test_returns_figure(self, viz):
        fig = viz.space_transformer()
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_custom_initial_matrix(self, viz):
        fig = viz.space_transformer(initial_matrix=[[1.5, 0.5], [-0.25, 2.0]])
        assert fig is not None

    def test_invalid_initial_matrix_shape_raises(self, viz):
        with pytest.raises(ValueError, match="2x2"):
            viz.space_transformer(initial_matrix=[1, 2, 3])

    def test_sliders_are_created(self, viz):
        viz.space_transformer()
        expected = {'a (i-hat x)', 'b (j-hat x)', 'c (i-hat y)', 'd (j-hat y)', 'Time (t)'}
        assert expected.issubset(set(viz.sliders.keys()))

    def test_title_contains_determinant(self, viz):
        fig = viz.space_transformer()
        title = fig.axes[0].get_title()
        assert "Det" in title

    def test_time_slider_updates_plot(self, viz):
        fig = viz.space_transformer()
        old_title = fig.axes[0].get_title()
        viz.sliders['Time (t)'].set_val(0.25)
        new_title = fig.axes[0].get_title()
        assert old_title != new_title


class TestEigenvectorDiscoveryMode:
    def test_returns_figure(self, viz):
        fig = viz.eigenvector_discovery_mode()
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_invalid_initial_matrix_shape_raises(self, viz):
        with pytest.raises(ValueError, match="2x2"):
            viz.eigenvector_discovery_mode(initial_matrix=[1, 2, 3])

    def test_expected_sliders_exist(self, viz):
        viz.eigenvector_discovery_mode()
        expected = {'a', 'b', 'c', 'd', 'Time (t)'}
        assert expected.issubset(set(viz.sliders.keys()))

    def test_title_contains_mode_name(self, viz):
        fig = viz.eigenvector_discovery_mode()
        title = fig.axes[0].get_title()
        assert 'Eigenvector' in title
