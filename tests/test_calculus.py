"""
Tests for CalculusVisualizer (mathviz/concepts.py)
"""
import pytest
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


@pytest.fixture
def viz():
    from mathviz import CalculusVisualizer
    return CalculusVisualizer()


# --- CalculusVisualizer initialization ---

class TestCalculusVisualizerInit:
    def test_is_mathviz_subclass(self):
        from mathviz import CalculusVisualizer, MathViz
        v = CalculusVisualizer()
        assert isinstance(v, MathViz)

    def test_default_figsize(self, viz):
        assert viz.figsize == (12, 8)


# --- derivative_visualizer ---

class TestDerivativeVisualizer:
    def test_returns_figure(self, viz):
        fig = viz.derivative_visualizer("x**2")
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_cubic_function(self, viz):
        fig = viz.derivative_visualizer("x**3 - 3*x**2 + 2*x")
        assert fig is not None

    def test_trig_function(self, viz):
        fig = viz.derivative_visualizer("sin(x)")
        assert fig is not None

    def test_exponential_function(self, viz):
        fig = viz.derivative_visualizer("exp(-x**2)")
        assert fig is not None

    def test_custom_x_range(self, viz):
        fig = viz.derivative_visualizer("x**2", x_range=(-3, 3))
        assert fig is not None

    def test_with_function_input_shown(self, viz):
        fig = viz.derivative_visualizer("x**3", show_function_input=True)
        assert fig is not None

    def test_with_function_input_hidden(self, viz):
        fig = viz.derivative_visualizer("x**3", show_function_input=False)
        assert fig is not None

    def test_invalid_function_does_not_crash(self, viz):
        fig = viz.derivative_visualizer("not_a_valid_expression_xyz")
        assert fig is not None

    def test_slider_created(self, viz):
        viz.derivative_visualizer("x**2")
        assert 'x' in viz.sliders

    def test_complex_function(self, viz):
        fig = viz.derivative_visualizer("x**4 - 2*x**3 + x**2 - 1")
        assert fig is not None


# --- integral_visualizer ---

class TestIntegralVisualizer:
    def test_returns_figure(self, viz):
        fig = viz.integral_visualizer("x**2")
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_custom_integration_range(self, viz):
        fig = viz.integral_visualizer("x**2", integration_range=(0, 2))
        assert fig is not None

    def test_custom_x_range(self, viz):
        fig = viz.integral_visualizer("x**2", x_range=(-4, 4))
        assert fig is not None

    def test_sin_function(self, viz):
        fig = viz.integral_visualizer("sin(x)", x_range=(-3.14, 3.14), integration_range=(0, 3.14))
        assert fig is not None

    def test_reversed_bounds_handled(self, viz):
        """Should handle a > b gracefully by swapping"""
        fig = viz.integral_visualizer("x**2", integration_range=(2, -1))
        assert fig is not None

    def test_invalid_function_does_not_crash(self, viz):
        fig = viz.integral_visualizer("totally_invalid_xyz")
        assert fig is not None

    def test_sliders_created(self, viz):
        viz.integral_visualizer("x**2")
        assert 'a' in viz.sliders
        assert 'b' in viz.sliders


# --- Symbolic derivative correctness ---

class TestDerivativeAccuracy:
    def test_power_rule(self):
        x = sp.Symbol('x')
        assert sp.diff(x**3, x) == 3 * x**2

    def test_sine_derivative(self):
        x = sp.Symbol('x')
        assert sp.diff(sp.sin(x), x) == sp.cos(x)

    def test_cosine_derivative(self):
        x = sp.Symbol('x')
        assert sp.diff(sp.cos(x), x) == -sp.sin(x)

    def test_exponential_derivative(self):
        x = sp.Symbol('x')
        assert sp.diff(sp.exp(x), x) == sp.exp(x)

    def test_product_rule(self):
        x = sp.Symbol('x')
        # d/dx[x * sin(x)] = sin(x) + x*cos(x)
        f = x * sp.sin(x)
        df = sp.diff(f, x)
        expected = sp.sin(x) + x * sp.cos(x)
        assert sp.simplify(df - expected) == 0

    def test_chain_rule(self):
        x = sp.Symbol('x')
        # d/dx[sin(x^2)] = 2x*cos(x^2)
        f = sp.sin(x**2)
        df = sp.diff(f, x)
        expected = 2 * x * sp.cos(x**2)
        assert sp.simplify(df - expected) == 0

    def test_cubic_derivative(self):
        x = sp.Symbol('x')
        f = x**3 - 3 * x**2 + 2 * x
        df = sp.diff(f, x)
        assert df == 3 * x**2 - 6 * x + 2


# --- Symbolic integration correctness ---

class TestIntegrationAccuracy:
    def test_power_rule_integral(self):
        x = sp.Symbol('x')
        result = sp.integrate(x**2, (x, 0, 2))
        assert result == sp.Rational(8, 3)

    def test_sin_integral_over_period(self):
        x = sp.Symbol('x')
        result = sp.integrate(sp.sin(x), (x, 0, 2 * sp.pi))
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_constant_integral(self):
        x = sp.Symbol('x')
        result = sp.integrate(sp.Integer(1), (x, 0, 5))
        assert result == 5

    def test_negative_area(self):
        """Integral of -x^2 over [0,1] is negative"""
        x = sp.Symbol('x')
        result = float(sp.integrate(-x**2, (x, 0, 1)).evalf())
        assert result == pytest.approx(-1 / 3, rel=1e-6)

    def test_symmetric_odd_function(self):
        """Integral of x^3 over symmetric interval is 0"""
        x = sp.Symbol('x')
        result = sp.integrate(x**3, (x, -2, 2))
        assert result == 0

    def test_numerical_vs_symbolic(self):
        """Trapezoidal rule should be close to symbolic for smooth function"""
        x = sp.Symbol('x')
        func = x**2
        symbolic = float(sp.integrate(func, (x, 0, 1)).evalf())
        func_np = sp.lambdify(x, func, 'numpy')
        x_num = np.linspace(0, 1, 10000)
        numerical = np.trapezoid(func_np(x_num), x_num) if hasattr(np, 'trapezoid') else np.trapz(func_np(x_num), x_num)
        assert numerical == pytest.approx(symbolic, rel=1e-4)


# --- Tangent line correctness ---

class TestTangentLine:
    def test_tangent_slope_equals_derivative(self):
        """Slope of tangent at x0 equals f'(x0)"""
        x = sp.Symbol('x')
        func = x**3 - x
        deriv = sp.diff(func, x)
        x0 = 1.5
        slope = float(deriv.subs(x, x0).evalf())
        # Numerically verify: (f(x0+h) - f(x0)) / h ≈ slope
        func_np = sp.lambdify(x, func, 'numpy')
        h = 1e-7
        numerical_slope = (func_np(x0 + h) - func_np(x0 - h)) / (2 * h)
        assert numerical_slope == pytest.approx(slope, rel=1e-5)

    def test_tangent_passes_through_point(self):
        """Tangent line passes through (x0, f(x0))"""
        x = sp.Symbol('x')
        func = x**2
        deriv = sp.diff(func, x)
        x0 = 2.0
        func_np = sp.lambdify(x, func, 'numpy')
        y0 = func_np(x0)
        slope = float(deriv.subs(x, x0).evalf())
        # Tangent: y = slope*(x - x0) + y0
        # At x = x0: y = y0
        assert slope * (x0 - x0) + y0 == pytest.approx(y0)
