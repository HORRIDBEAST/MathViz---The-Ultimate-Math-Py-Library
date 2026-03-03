"""
Tests for AlgebraVisualizer (mathviz/concepts.py)
"""
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


@pytest.fixture
def viz():
    from mathviz import AlgebraVisualizer
    return AlgebraVisualizer()


# --- AlgebraVisualizer initialization ---

class TestAlgebraVisualizerInit:
    def test_is_mathviz_subclass(self):
        from mathviz import AlgebraVisualizer, MathViz
        v = AlgebraVisualizer()
        assert isinstance(v, MathViz)

    def test_default_figsize(self, viz):
        assert viz.figsize == (12, 8)

    def test_custom_figsize(self):
        from mathviz import AlgebraVisualizer
        v = AlgebraVisualizer(figsize=(8, 5))
        assert v.figsize == (8, 5)


# --- quadratic_explorer ---

class TestQuadraticExplorer:
    def test_returns_figure(self, viz):
        fig = viz.quadratic_explorer()
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_custom_a_range(self, viz):
        fig = viz.quadratic_explorer(a_range=(-2, 2))
        assert fig is not None

    def test_custom_b_range(self, viz):
        fig = viz.quadratic_explorer(b_range=(-3, 3))
        assert fig is not None

    def test_custom_c_range(self, viz):
        fig = viz.quadratic_explorer(c_range=(-4, 4))
        assert fig is not None

    def test_custom_x_range(self, viz):
        fig = viz.quadratic_explorer(x_range=(-8, 8))
        assert fig is not None

    def test_custom_y_range(self, viz):
        fig = viz.quadratic_explorer(y_range=(-15, 15))
        assert fig is not None

    def test_all_custom_ranges(self, viz):
        fig = viz.quadratic_explorer(
            a_range=(-3, 3),
            b_range=(-5, 5),
            c_range=(-5, 5),
            x_range=(-8, 8),
            y_range=(-10, 15)
        )
        assert fig is not None

    def test_sliders_created(self, viz):
        viz.quadratic_explorer()
        # Should have sliders for a, b, c
        assert 'a' in viz.sliders
        assert 'b' in viz.sliders
        assert 'c' in viz.sliders

    def test_figure_has_axes(self, viz):
        fig = viz.quadratic_explorer()
        assert len(fig.axes) > 0


# --- Quadratic math correctness ---

class TestQuadraticMath:
    def test_vertex_formula_positive_a(self):
        """Test vertex x = -b / (2a)"""
        a, b, c = 1.0, -4.0, 3.0  # (x-1)(x-3), vertex at x=2
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        assert vertex_x == pytest.approx(2.0)
        assert vertex_y == pytest.approx(-1.0)

    def test_vertex_formula_negative_a(self):
        a, b, c = -1.0, 2.0, 0.0  # vertex at x=1
        vertex_x = -b / (2 * a)
        assert vertex_x == pytest.approx(1.0)

    def test_discriminant_two_roots(self):
        """b^2 - 4ac > 0 => two real roots"""
        a, b, c = 1.0, -5.0, 6.0  # roots at 2 and 3
        disc = b**2 - 4 * a * c
        assert disc > 0
        root1 = (-b + np.sqrt(disc)) / (2 * a)
        root2 = (-b - np.sqrt(disc)) / (2 * a)
        assert sorted([root1, root2]) == pytest.approx([2.0, 3.0])

    def test_discriminant_one_root(self):
        a, b, c = 1.0, -2.0, 1.0  # (x-1)^2
        disc = b**2 - 4 * a * c
        assert disc == pytest.approx(0.0)

    def test_discriminant_no_roots(self):
        a, b, c = 1.0, 0.0, 1.0  # x^2 + 1
        disc = b**2 - 4 * a * c
        assert disc < 0

    def test_parabola_values(self):
        """Values of quadratic match formula"""
        a, b, c = 2.0, -3.0, 1.0
        x_vals = np.array([-2, -1, 0, 1, 2], dtype=float)
        expected = a * x_vals**2 + b * x_vals + c
        computed = np.polyval([a, b, c], x_vals)
        np.testing.assert_allclose(computed, expected)


# --- polynomial_explorer ---

class TestPolynomialExplorer:
    @pytest.mark.parametrize("degree", [2, 3, 4, 5])
    def test_valid_degrees(self, viz, degree):
        fig = viz.polynomial_explorer(degree=degree)
        assert fig is not None

    def test_degree_too_low_raises(self, viz):
        with pytest.raises(ValueError):
            viz.polynomial_explorer(degree=1)

    def test_degree_too_high_raises(self, viz):
        with pytest.raises(ValueError):
            viz.polynomial_explorer(degree=6)

    def test_degree_zero_raises(self, viz):
        with pytest.raises(ValueError):
            viz.polynomial_explorer(degree=0)

    def test_custom_x_range(self, viz):
        fig = viz.polynomial_explorer(degree=3, x_range=(-3, 3))
        assert fig is not None

    def test_custom_y_range(self, viz):
        fig = viz.polynomial_explorer(degree=3, y_range=(-20, 20))
        assert fig is not None

    def test_sliders_count(self, viz):
        """Should have degree+1 coefficient sliders"""
        degree = 3
        viz.polynomial_explorer(degree=degree)
        coef_sliders = [k for k in viz.sliders if k.startswith('a')]
        assert len(coef_sliders) == degree + 1

    def test_returns_matplotlib_figure(self, viz):
        fig = viz.polynomial_explorer(degree=4)
        assert isinstance(fig, plt.Figure)


# --- Polynomial math ---

class TestPolynomialMath:
    def test_degree_2_evaluation(self):
        a2, a1, a0 = 1.0, -2.0, 1.0
        x = 3.0
        expected = a2 * x**2 + a1 * x + a0
        assert expected == pytest.approx(4.0)

    def test_degree_3_evaluation(self):
        a3, a2, a1, a0 = 1.0, 0.0, -1.0, 0.0  # x^3 - x
        x = 2.0
        result = a3 * x**3 + a2 * x**2 + a1 * x + a0
        assert result == pytest.approx(6.0)

    def test_zero_polynomial(self):
        x = np.linspace(-5, 5, 100)
        y = np.zeros_like(x)
        assert np.all(y == 0)

    def test_coefficient_effect_leading_term(self):
        """Doubling leading coefficient doubles values far from origin"""
        x = 10.0
        assert 2 * x**4 == pytest.approx(20000.0)
