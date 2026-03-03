# MathViz

**Interactive Mathematical Visualization Library for Python**

MathViz makes it easy to explore mathematical concepts through interactive plots, real-time parameter sliders, hover tooltips, and full Jupyter Notebook support.

---

## Features

- **Algebra Visualizer** — quadratic & polynomial explorers with live sliders (vertex, roots, discriminant)
- **Calculus Visualizer** — derivative + tangent-line visualizer; definite integral with shaded area and symbolic result
- **General-purpose tools** — multi-function plotter, parametric curves, function explorer with auto feature detection
- **Hover tooltips** via `mplcursors` — see exact x/y values and slope on hover
- **Jupyter support** — two integration layers:
  - `JupyterMathViz` — ipywidgets slider-only interface
  - `JupyterSimpleMathViz` — fully native ipywidgets (safe text input, no keyboard shortcut conflicts)
- **Widget wrappers** — thin `Slider`, `Button`, `InputBox` classes over `matplotlib.widgets`
- **Example gallery** — built-in algebra, calculus, and advanced demos
- **Save figures** — export any visualization as PNG at arbitrary DPI

---

## Installation

### From PyPI

```bash
pip install mathvizpro
```

### With Jupyter support

```bash
pip install mathvizpro[jupyter]
```

### From source (development)

```bash
git clone https://github.com/HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library.git
cd MathViz---The-Ultimate-Math-Py-Library
pip install -e .
```

### Requirements

| Package | Version |
|---|---|
| Python | ≥ 3.8 |
| numpy | ≥ 1.21.0 |
| matplotlib | ≥ 3.5.0 |
| sympy | ≥ 1.9.0 |
| mplcursors | ≥ 0.5.0 |
| ipywidgets *(optional)* | ≥ 7.6.0 |

---

## Quick Start

```python
import mathviz
mathviz.print_info()   # version check
mathviz.quick_start()  # usage guide
```

---

## Usage

### Algebra — Quadratic Explorer

```python
from mathviz import AlgebraVisualizer
import matplotlib.pyplot as plt

viz = AlgebraVisualizer()
viz.quadratic_explorer(
    a_range=(-3, 3),
    b_range=(-5, 5),
    c_range=(-5, 5),
    x_range=(-8, 8)
)
plt.show()
```

Sliders control `a`, `b`, `c`. The vertex and roots update in real-time. Hover over the curve for exact values.

### Algebra — Polynomial Explorer

```python
viz.polynomial_explorer(degree=4, x_range=(-3, 3))
plt.show()
```

Supports degree 2–5. One slider per coefficient.

### Calculus — Derivative Visualizer

```python
from mathviz import CalculusVisualizer

calc = CalculusVisualizer()
calc.derivative_visualizer(
    func_str="x**3 - 3*x**2 + 2*x",
    x_range=(-1, 4),
    show_function_input=True   # text box to change the function
)
plt.show()
```

Shows `f(x)` and `f'(x)`. Drag the `x` slider to move the tangent line.

### Calculus — Integral Visualizer

```python
calc.integral_visualizer(
    func_str="x**2 - 4",
    x_range=(-4, 4),
    integration_range=(-2, 3)
)
plt.show()
```

Sliders `a` and `b` adjust the integration bounds. The exact symbolic result (via SymPy) is shown in the title.

### General — Multi-Function Plotter

```python
from mathviz import MathViz

core = MathViz()
core.multi_function_plotter(
    functions=["x**2", "sin(x)", "cos(x)", "2*x - 1"],
    x_range=(-5, 5)
)
plt.show()
```

Each function gets its own labeled text box. Hover tooltips show exact values.

### General — Parametric Curves

```python
import numpy as np

core.parametric_plotter(
    x_func="sin(3*t)",
    y_func="sin(2*t)",
    t_range=(0, 2 * np.pi)
)
plt.show()
```

### General — Function Explorer

```python
core.function_explorer(
    initial_func="x**4 - 2*x**2 + 1",
    x_range=(-3, 3),
    auto_detect_features=True
)
plt.show()
```

Automatically marks roots and critical points.

### Save a Figure

```python
viz = AlgebraVisualizer()
fig = viz.quadratic_explorer()
viz.save_figure("output.png", dpi=300)
```

---

## Jupyter Notebook Usage

### Important — Text Input in Notebooks

Matplotlib's native `TextBox` widget works perfectly in standalone Python scripts. Inside a Jupyter Notebook, the `%matplotlib widget` (ipympl) backend often fails to trap letter keypresses before Jupyter's own keyboard shortcuts intercept them (`x` = cut cell, `d` = delete, `b` = insert below, etc.).

**Rule of thumb:**

| Environment | Use |
|---|---|
| Standalone script / `demo.py` | `MathViz`, `AlgebraVisualizer`, `CalculusVisualizer` |
| Jupyter — sliders only | `JupyterMathViz` |
| Jupyter — text input needed | `JupyterSimpleMathViz` ✅ |

### JupyterSimpleMathViz (recommended for notebooks)

Uses native `ipywidgets.Text` boxes — all keystrokes are trapped correctly.

```python
%matplotlib inline   # or widget — both work
from mathviz import JupyterSimpleMathViz

viz = JupyterSimpleMathViz()

viz.interactive_function_plotter(initial_func="x**2")  # type sin(x), x**3, etc.
viz.interactive_derivative(initial_func="x**3")
viz.interactive_integral(initial_func="sin(x)")
viz.interactive_quadratic()
viz.interactive_parametric()
```

### JupyterMathViz (slider-only fallback)

```python
from mathviz import JupyterMathViz

jv = JupyterMathViz()
jv.interactive_quadratic()
```

---

## Example Gallery

```python
from mathviz import ExampleGallery

gallery = ExampleGallery()

gallery.algebra_examples()    # quadratic & polynomial demos
gallery.calculus_examples()   # derivative & integral demos
gallery.advanced_examples()   # parametric, multi-function demos

# List all available examples
for category, items in gallery.get_example_list().items():
    print(f"{category}: {items}")
```

---

## Supported Function Syntax

All text inputs accept standard SymPy / NumPy expressions:

| Math | Python syntax |
|---|---|
| x² | `x**2` |
| sin x | `sin(x)` |
| eˣ | `exp(x)` |
| ln x | `log(x)` |
| √x | `sqrt(x)` |
| \|x\| | `Abs(x)` |
| π | `pi` |

---

## Project Structure

```
mathviz/
├── __init__.py           # Public API, get_info(), print_info(), quick_start()
├── core.py               # MathViz base class — all general-purpose tools
├── concepts.py           # AlgebraVisualizer, CalculusVisualizer
├── widgets.py            # Slider, Button, InputBox wrappers
├── examples.py           # ExampleGallery
├── jupyter_integration.py# JupyterMathViz (ipywidgets.interact, sliders only)
├── jupyter_simple.py     # JupyterSimpleMathViz (ipywidgets.Text, full input)
└── utils.py              # export_to_data_url and helpers

notebooks/
├── getting_started.ipynb # Full walkthrough — run this first
├── algebra_examples.ipynb
├── calculus_examples.ipynb
└── test_mathviz.ipynb    # Manual integration test notebook

tests/
├── test_core.py          # 45 tests — MathViz base class
├── test_algebra.py       # 38 tests — AlgebraVisualizer
├── test_calculus.py      # 37 tests — CalculusVisualizer
└── test_integration.py   # 37 tests — package metadata, widgets, utils, gallery
```

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=mathviz --cov-report=term-missing

# Quick smoke test
pytest test_mathviz.py -v
```

Current status: **172 tests, 0 failures**.

---

## Architecture

```
MathViz (core.py)
├── create_figure() / show() / close() / save_figure()
├── add_slider() / add_button() / add_textbox()
├── function_explorer()
├── multi_function_plotter()
└── parametric_plotter()

AlgebraVisualizer(MathViz)       — concepts.py
├── quadratic_explorer()
└── polynomial_explorer()

CalculusVisualizer(MathViz)      — concepts.py
├── derivative_visualizer()
└── integral_visualizer()

JupyterSimpleMathViz             — jupyter_simple.py (standalone, no MathViz inheritance)
├── interactive_function_plotter()
├── interactive_derivative()
├── interactive_integral()
├── interactive_quadratic()
└── interactive_parametric()
```

Key design decisions:
- All visualizer methods return `self.fig` — composable and testable
- Invalid function strings display an error inside the axes; they never raise to the caller
- Widgets are stored in `self.widgets[label]` so Python's GC cannot destroy them mid-session
- `mplcursors` and `ipywidgets` are optional — guarded by `try/except ImportError`
- SymPy handles symbolic differentiation and integration; `lambdify` converts to NumPy for plotting

---

## Known Limitations

- Matplotlib `TextBox` in Jupyter Notebooks intercepts letter keypresses → use `JupyterSimpleMathViz` instead
- `JupyterSimpleMathViz` redraws the full figure on every widget change (ipywidgets constraint) — hover tooltips not available
- `polynomial_explorer` supports degree 2–5 only; degree outside this range raises `ValueError`
- Very large x-ranges with discontinuous functions (e.g. `tan(x)`) may show visual spikes

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Run tests: `pytest tests/`
4. Submit a pull request to [HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library](https://github.com/HORRIDBEAST/MathViz---The-Ultimate-Math-Py-Library)

Please ensure all existing tests pass and add tests for new functionality.
