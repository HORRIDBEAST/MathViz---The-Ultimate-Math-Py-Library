"""
Integration and component tests for MathViz:
  - Package metadata & imports
  - Widget wrappers
  - Utility functions
  - ExampleGallery
  - Jupyter integration availability
"""
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO
from contextlib import redirect_stdout


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


# --- Package metadata ---

class TestPackageMetadata:
    def test_version_string(self):
        import mathviz
        assert hasattr(mathviz, '__version__')
        assert isinstance(mathviz.__version__, str)
        # Should follow semver loosely: X.Y.Z
        parts = mathviz.__version__.split('.')
        assert len(parts) >= 2

    def test_author_present(self):
        import mathviz
        assert hasattr(mathviz, '__author__')
        assert len(mathviz.__author__) > 0

    def test_all_exports_importable(self):
        from mathviz import (
            MathViz,
            AlgebraVisualizer,
            CalculusVisualizer,
            Slider,
            Button,
            InputBox,
            ExampleGallery,
            export_to_data_url,
        )
        for obj in [MathViz, AlgebraVisualizer, CalculusVisualizer,
                    Slider, Button, InputBox, ExampleGallery, export_to_data_url]:
            assert obj is not None

    def test_get_info_returns_dict(self):
        import mathviz
        info = mathviz.get_info()
        assert isinstance(info, dict)

    def test_get_info_has_version(self):
        import mathviz
        info = mathviz.get_info()
        assert 'version' in info
        assert info['version'] == mathviz.__version__

    def test_get_info_has_jupyter_flag(self):
        import mathviz
        info = mathviz.get_info()
        assert 'jupyter_available' in info
        assert isinstance(info['jupyter_available'], bool)

    def test_print_info_outputs_mathviz(self, capsys):
        import mathviz
        mathviz.print_info()
        captured = capsys.readouterr()
        assert 'MathViz' in captured.out

    def test_quick_start_outputs_guide(self, capsys):
        import mathviz
        mathviz.quick_start()
        captured = capsys.readouterr()
        assert 'Quick Start' in captured.out


# --- Widget wrappers ---

class TestWidgetWrappers:
    def test_slider_instantiation(self):
        from mathviz.widgets import Slider
        fig, ax = plt.subplots()
        s = Slider(ax, 'test', 0, 10, valinit=5.0)
        assert s.val == pytest.approx(5.0)

    def test_slider_with_callback(self):
        from mathviz.widgets import Slider
        fig, ax = plt.subplots()
        log = []
        s = Slider(ax, 'cb', 0, 10, valinit=1.0, callback=lambda v: log.append(v))
        assert s is not None  # callback connected without error

    def test_button_instantiation(self):
        from mathviz.widgets import Button
        fig, ax = plt.subplots()
        b = Button(ax, 'Click Me')
        assert b is not None

    def test_button_with_callback(self):
        from mathviz.widgets import Button
        fig, ax = plt.subplots()
        log = []
        b = Button(ax, 'OK', callback=lambda e: log.append(1))
        assert b is not None

    def test_inputbox_instantiation(self):
        from mathviz.widgets import InputBox
        fig, ax = plt.subplots()
        ib = InputBox(ax, 'label', initial='hello')
        assert ib is not None

    def test_inputbox_text_property(self):
        from mathviz.widgets import InputBox
        fig, ax = plt.subplots()
        ib = InputBox(ax, 'f(x)', initial='x**2')
        assert ib.text == 'x**2'

    def test_inputbox_with_callback(self):
        from mathviz.widgets import InputBox
        fig, ax = plt.subplots()
        log = []
        ib = InputBox(ax, 'fn', initial='', callback=lambda t: log.append(t))
        assert ib is not None

    def test_slider_val_property(self):
        from mathviz.widgets import Slider
        fig, ax = plt.subplots()
        s = Slider(ax, 'x', -10, 10, valinit=3.5)
        assert s.val == pytest.approx(3.5, abs=1e-6)


# --- Utility functions ---

class TestUtils:
    def test_export_to_data_url_returns_string(self):
        from mathviz.utils import export_to_data_url
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        url = export_to_data_url(fig)
        assert isinstance(url, str)

    def test_export_to_data_url_starts_correctly(self):
        from mathviz.utils import export_to_data_url
        fig, ax = plt.subplots()
        url = export_to_data_url(fig)
        assert url.startswith('data:image/png;base64,')

    def test_export_to_data_url_non_empty_payload(self):
        from mathviz.utils import export_to_data_url
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        url = export_to_data_url(fig)
        # Strip the prefix and check there's real base64 data
        payload = url.split(',', 1)[1]
        assert len(payload) > 100

    def test_export_jpg_format(self):
        from mathviz.utils import export_to_data_url
        fig, ax = plt.subplots()
        url = export_to_data_url(fig, format='jpg')
        assert url.startswith('data:image/jpg;base64,')

    def test_export_multiple_figures_independent(self):
        from mathviz.utils import export_to_data_url
        fig1, ax1 = plt.subplots()
        ax1.plot([1, 2], [1, 2])
        fig2, ax2 = plt.subplots()
        ax2.plot([1, 2], [2, 1])
        url1 = export_to_data_url(fig1)
        url2 = export_to_data_url(fig2)
        # Two different plots should produce different data
        assert url1 != url2


# --- ExampleGallery ---

class TestExampleGallery:
    def test_instantiation(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        assert g is not None

    def test_examples_attribute_is_dict(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        assert isinstance(g.examples, dict)

    def test_get_example_list_returns_dict(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        assert isinstance(result, dict)

    def test_get_example_list_has_algebra_key(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        assert 'algebra' in result

    def test_get_example_list_has_calculus_key(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        assert 'calculus' in result

    def test_get_example_list_values_are_lists(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        for v in result.values():
            assert isinstance(v, list)

    def test_algebra_examples_list_non_empty(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        assert len(result['algebra']) > 0

    def test_calculus_examples_list_non_empty(self):
        from mathviz import ExampleGallery
        g = ExampleGallery()
        result = g.get_example_list()
        assert len(result['calculus']) > 0


# --- Jupyter integration ---

class TestJupyterIntegration:
    def test_jupyter_mathviz_is_importable(self):
        """JupyterMathViz should be importable (may be None without ipywidgets)"""
        from mathviz import JupyterMathViz
        # It's either a class or None — both are acceptable
        assert JupyterMathViz is None or callable(JupyterMathViz)

    def test_jupyter_flag_in_get_info(self):
        import mathviz
        from mathviz.jupyter_integration import JUPYTER_AVAILABLE
        info = mathviz.get_info()
        assert info['jupyter_available'] == JUPYTER_AVAILABLE

    def test_jupyter_mathviz_raises_on_instantiation_without_ipywidgets(self):
        """Without ipywidgets, instantiating JupyterMathViz should raise ImportError."""
        try:
            import ipywidgets  # noqa: F401
            pytest.skip("ipywidgets is installed — skip this test")
        except ImportError:
            from mathviz import JupyterMathViz
            # Class is still importable; but instantiation raises ImportError
            assert JupyterMathViz is not None
            with pytest.raises(ImportError):
                JupyterMathViz()


# --- Cross-module consistency ---

class TestCrossModuleConsistency:
    def test_algebra_uses_core_base(self):
        from mathviz.concepts import AlgebraVisualizer
        from mathviz.core import MathViz
        assert issubclass(AlgebraVisualizer, MathViz)

    def test_calculus_uses_core_base(self):
        from mathviz.concepts import CalculusVisualizer
        from mathviz.core import MathViz
        assert issubclass(CalculusVisualizer, MathViz)

    def test_algebra_create_figure_initialises_fig(self):
        from mathviz import AlgebraVisualizer
        v = AlgebraVisualizer()
        fig, ax = v.create_figure()
        assert v.fig is fig

    def test_calculus_close_clears_state(self):
        from mathviz import CalculusVisualizer
        v = CalculusVisualizer()
        v.create_figure()
        v.close()
        assert v.fig is None
        assert v.ax is None

    def test_algebra_save_without_figure_raises(self):
        from mathviz import AlgebraVisualizer
        v = AlgebraVisualizer()
        with pytest.raises(ValueError):
            v.save_figure("output.png")

    def test_calculus_save_without_figure_raises(self):
        from mathviz import CalculusVisualizer
        v = CalculusVisualizer()
        with pytest.raises(ValueError):
            v.save_figure("output.png")
