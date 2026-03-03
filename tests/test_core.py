"""
Tests for MathViz core module (MathViz base class)
"""
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox


@pytest.fixture(autouse=True)
def close_figures():
    """Close all figures after each test"""
    yield
    plt.close('all')


@pytest.fixture
def viz():
    from mathviz import MathViz
    return MathViz()


# --- Initialization ---

class TestMathVizInit:
    def test_default_figsize(self, viz):
        assert viz.figsize == (12, 8)

    def test_custom_figsize(self):
        from mathviz import MathViz
        v = MathViz(figsize=(10, 6))
        assert v.figsize == (10, 6)

    def test_initial_state(self, viz):
        assert viz.fig is None
        assert viz.ax is None
        assert viz.sliders == {}
        assert viz.widgets == {}


# --- create_figure ---

class TestCreateFigure:
    def test_returns_fig_ax(self, viz):
        fig, ax = viz.create_figure()
        assert fig is not None
        assert ax is not None

    def test_stores_on_instance(self, viz):
        fig, ax = viz.create_figure()
        assert viz.fig is fig
        assert viz.ax is ax

    def test_creates_matplotlib_figure(self, viz):
        fig, ax = viz.create_figure()
        assert isinstance(fig, plt.Figure)


# --- add_slider ---

class TestAddSlider:
    def test_returns_slider(self, viz):
        viz.create_figure()
        s = viz.add_slider('test', 0, 10, 5, [0.2, 0.1, 0.3, 0.03])
        assert isinstance(s, Slider)

    def test_stored_in_sliders_dict(self, viz):
        viz.create_figure()
        viz.add_slider('alpha', -5, 5, 0, [0.2, 0.1, 0.3, 0.03])
        assert 'alpha' in viz.sliders

    def test_initial_value(self, viz):
        viz.create_figure()
        s = viz.add_slider('x', 0, 100, 42, [0.2, 0.1, 0.3, 0.03])
        assert s.val == pytest.approx(42.0)


# --- add_button ---

class TestAddButton:
    def test_returns_button(self, viz):
        viz.create_figure()
        b = viz.add_button('Reset', [0.2, 0.1, 0.1, 0.04])
        assert isinstance(b, Button)

    def test_stored_in_widgets_dict(self, viz):
        viz.create_figure()
        viz.add_button('Go', [0.2, 0.1, 0.1, 0.04])
        assert 'Go' in viz.widgets

    def test_callback_connected(self, viz):
        viz.create_figure()
        called = []
        viz.add_button('Click', [0.2, 0.1, 0.1, 0.04], callback=lambda e: called.append(1))
        # We just verify no exception; actual click simulation not needed


# --- add_textbox ---

class TestAddTextbox:
    def test_returns_textbox(self, viz):
        viz.create_figure()
        tb = viz.add_textbox('f(x)', 'x**2', [0.2, 0.1, 0.4, 0.04])
        assert isinstance(tb, TextBox)

    def test_stored_in_widgets(self, viz):
        viz.create_figure()
        viz.add_textbox('label', 'init', [0.2, 0.1, 0.4, 0.04])
        assert 'label' in viz.widgets


# --- function_explorer ---

class TestFunctionExplorer:
    def test_returns_figure(self, viz):
        fig = viz.function_explorer("x**2")
        assert fig is not None

    def test_custom_range(self, viz):
        fig = viz.function_explorer("sin(x)", x_range=(-3.14, 3.14))
        assert fig is not None

    def test_invalid_function_does_not_crash(self, viz):
        fig = viz.function_explorer("not_a_valid_function_xyz")
        assert fig is not None

    def test_auto_detect_true(self, viz):
        fig = viz.function_explorer("x**3 - x", auto_detect_features=True)
        assert fig is not None

    def test_auto_detect_false(self, viz):
        fig = viz.function_explorer("x**2", auto_detect_features=False)
        assert fig is not None

    def test_trigonometric(self, viz):
        fig = viz.function_explorer("sin(x) + cos(2*x)")
        assert fig is not None

    def test_exponential(self, viz):
        fig = viz.function_explorer("exp(-x**2)")
        assert fig is not None


# --- multi_function_plotter ---

class TestMultiFunctionPlotter:
    def test_single_function(self, viz):
        fig = viz.multi_function_plotter(["x**2"])
        assert fig is not None

    def test_multiple_functions(self, viz):
        fig = viz.multi_function_plotter(["x**2", "sin(x)", "cos(x)"])
        assert fig is not None

    def test_custom_x_range(self, viz):
        fig = viz.multi_function_plotter(["x**2"], x_range=(-3, 3))
        assert fig is not None

    def test_custom_colors(self, viz):
        fig = viz.multi_function_plotter(["x", "x**2"], colors=["red", "blue"])
        assert fig is not None

    def test_empty_list_raises(self, viz):
        with pytest.raises(ValueError):
            viz.multi_function_plotter([])

    def test_handles_invalid_function_gracefully(self, viz):
        # Invalid function mixed with valid should not crash
        fig = viz.multi_function_plotter(["x**2", "invalid_xyz_func"])
        assert fig is not None

    def test_four_functions(self, viz):
        fig = viz.multi_function_plotter(["x**2", "sin(x)", "exp(x/3)", "log(x+5)"])
        assert fig is not None


# --- parametric_plotter ---

class TestParametricPlotter:
    def test_circle(self, viz):
        fig = viz.parametric_plotter("cos(t)", "sin(t)", (0, 6.28))
        assert fig is not None

    def test_default_args(self, viz):
        fig = viz.parametric_plotter()
        assert fig is not None

    def test_lissajous(self, viz):
        fig = viz.parametric_plotter("sin(3*t)", "sin(2*t)", (0, 6.28))
        assert fig is not None

    def test_invalid_xfunc_does_not_crash(self, viz):
        fig = viz.parametric_plotter("invalid_xyz", "sin(t)", (0, 3.14))
        assert fig is not None


# --- save_figure ---

class TestSaveFigure:
    def test_save_raises_without_figure(self, viz):
        with pytest.raises(ValueError):
            viz.save_figure("out.png")

    def test_save_png(self, viz, tmp_path):
        viz.function_explorer("x**2")
        out = str(tmp_path / "test.png")
        viz.save_figure(out, dpi=72)
        import os
        assert os.path.exists(out)
        assert os.path.getsize(out) > 0


# --- close ---

class TestClose:
    def test_close_clears_state(self, viz):
        viz.create_figure()
        assert viz.fig is not None
        viz.close()
        assert viz.fig is None
        assert viz.ax is None
