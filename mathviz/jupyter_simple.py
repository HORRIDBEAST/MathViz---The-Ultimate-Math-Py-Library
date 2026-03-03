"""
JupyterSimpleMathViz - Native ipywidgets-based visualizations for Jupyter Notebooks.

Why this module exists
----------------------
Matplotlib's native TextBox widget (used by MathViz / AlgebraVisualizer /
CalculusVisualizer) works perfectly in standalone Python scripts.  Inside a
Jupyter Notebook, however, the ipympl (%matplotlib widget) backend often
fails to capture keypresses before they reach the notebook shell.  Because
Jupyter uses single-letter keyboard shortcuts in "Command Mode" (e.g. 'x'
cuts the cell, 'd' deletes, 'b' inserts below), typing a function like
"sin(x)" into a Matplotlib TextBox causes the cell to disappear or other
destructive actions.

This module sidesteps that problem entirely by using ipywidgets.Text and
ipywidgets.FloatSlider — native browser widgets that correctly trap all
keystrokes and never conflict with Jupyter's own shortcuts.

Usage
-----
    from mathviz import JupyterSimpleMathViz   # or from mathviz.jupyter_simple

    viz = JupyterSimpleMathViz()
    viz.interactive_function_plotter()          # type sin(x), x**3, etc.
    viz.interactive_quadratic()
    viz.interactive_parametric()
    viz.interactive_derivative()
    viz.interactive_integral()
"""

try:
    import ipywidgets as widgets
    from IPython.display import display
    JUPYTER_SIMPLE_AVAILABLE = True
except ImportError:
    JUPYTER_SIMPLE_AVAILABLE = False
    widgets = None

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class JupyterSimpleMathViz:
    """
    MathViz visualizations that use native ipywidgets for Jupyter Notebooks.

    All text inputs are ``ipywidgets.Text`` boxes, so you can safely type
    any letter (including 'x', 'd', 'b', etc.) without triggering Jupyter
    keyboard shortcuts.
    """

    def __init__(self):
        if not JUPYTER_SIMPLE_AVAILABLE:
            raise ImportError(
                "JupyterSimpleMathViz requires ipywidgets. "
                "Install with: pip install ipywidgets"
            )
        plt.rcParams['figure.figsize'] = (10, 6)

    # ------------------------------------------------------------------
    # Generic function plotter
    # ------------------------------------------------------------------
    def interactive_function_plotter(self, initial_func="x**2",
                                     x_range=(-5, 5)):
        """Interactive single-function plotter with native text input.

        Type any expression in x (e.g. ``sin(x)``, ``x**3 - 2*x``) into the
        text box.  Adjusting x-range sliders updates the plot immediately.
        """
        def plot_function(func_str=initial_func,
                          x_min=float(x_range[0]),
                          x_max=float(x_range[1])):
            fig, ax = plt.subplots(figsize=(10, 6))
            try:
                x = sp.Symbol('x')
                func = sp.sympify(func_str)
                func_np = sp.lambdify(x, func, 'numpy')
                x_vals = np.linspace(x_min, x_max, 1000)
                y_vals = func_np(x_vals)
                ax.plot(x_vals, y_vals, 'b-', linewidth=2,
                        label=f'f(x) = {func}')
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.set_title(f'f(x) = {func}')
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {e}', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12,
                        bbox=dict(boxstyle="round", facecolor="lightcoral"))
                ax.set_title('Error — check your expression')
            plt.tight_layout()
            plt.show()

        return widgets.interactive(
            plot_function,
            func_str=widgets.Text(value=initial_func, description='f(x) =',
                                  layout=widgets.Layout(width='300px')),
            x_min=widgets.FloatSlider(min=-20, max=0,  value=float(x_range[0]),
                                      step=0.5, description='x min:'),
            x_max=widgets.FloatSlider(min=0,   max=20, value=float(x_range[1]),
                                      step=0.5, description='x max:'),
        )

    # ------------------------------------------------------------------
    # Quadratic explorer
    # ------------------------------------------------------------------
    def interactive_quadratic(self):
        """Interactive quadratic y = ax² + bx + c with vertex and roots."""
        def plot_quadratic(a=1.0, b=0.0, c=0.0):
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.linspace(-8, 8, 1000)
            y = a * x**2 + b * x + c
            ax.plot(x, y, 'b-', linewidth=2,
                    label=f'y = {a:.2f}x² + {b:.2f}x + {c:.2f}')
            if abs(a) > 1e-10:
                vx = -b / (2 * a)
                vy = a * vx**2 + b * vx + c
                ax.plot(vx, vy, 'ro', markersize=8,
                        label=f'Vertex ({vx:.2f}, {vy:.2f})')
                disc = b**2 - 4 * a * c
                if disc > 0:
                    r1 = (-b + np.sqrt(disc)) / (2 * a)
                    r2 = (-b - np.sqrt(disc)) / (2 * a)
                    ax.plot([r1, r2], [0, 0], 'go', markersize=8, label='Roots')
                elif abs(disc) < 1e-10:
                    ax.plot(-b / (2 * a), 0, 'go', markersize=8,
                            label='Root (repeated)')
            ax.set_xlim(-8, 8)
            ax.set_ylim(-15, 15)
            ax.axhline(0, color='k', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_title('Quadratic Explorer')
            plt.tight_layout()
            plt.show()

        return widgets.interactive(
            plot_quadratic,
            a=widgets.FloatSlider(min=-3, max=3,  step=0.1, value=1,
                                  description='a:'),
            b=widgets.FloatSlider(min=-5, max=5,  step=0.1, value=0,
                                  description='b:'),
            c=widgets.FloatSlider(min=-5, max=5,  step=0.1, value=0,
                                  description='c:'),
        )

    # ------------------------------------------------------------------
    # Derivative visualizer
    # ------------------------------------------------------------------
    def interactive_derivative(self, initial_func="x**3", x_range=(-4, 4)):
        """Plot f(x) and f'(x) side by side with a movable tangent point."""
        def plot_derivative(func_str=initial_func, x_point=0.0):
            fig, ax = plt.subplots(figsize=(10, 6))
            try:
                x = sp.Symbol('x')
                func = sp.sympify(func_str)
                deriv = sp.diff(func, x)
                fn = sp.lambdify(x, func,  'numpy')
                dn = sp.lambdify(x, deriv, 'numpy')
                xs = np.linspace(x_range[0], x_range[1], 1000)
                ax.plot(xs, fn(xs), 'b-', linewidth=2, label=f'f(x) = {func}')
                ax.plot(xs, dn(xs), 'r--', linewidth=2,
                        label=f"f'(x) = {deriv}")
                # tangent line
                y0 = float(fn(x_point))
                s  = float(dn(x_point))
                xt = np.linspace(x_point - 1.5, x_point + 1.5, 100)
                ax.plot(xt, s * (xt - x_point) + y0, 'g-', linewidth=2,
                        alpha=0.8, label=f'Tangent (slope={s:.3f})')
                ax.plot(x_point, y0, 'ko', markersize=9)
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.set_title(f'Derivative: tangent at x = {x_point:.2f}')
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {e}', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12,
                        bbox=dict(boxstyle="round", facecolor="lightcoral"))
            plt.tight_layout()
            plt.show()

        return widgets.interactive(
            plot_derivative,
            func_str=widgets.Text(value=initial_func, description='f(x) =',
                                  layout=widgets.Layout(width='300px')),
            x_point=widgets.FloatSlider(min=float(x_range[0]),
                                        max=float(x_range[1]),
                                        step=0.05, value=0.0,
                                        description='x point:'),
        )

    # ------------------------------------------------------------------
    # Integral visualizer
    # ------------------------------------------------------------------
    def interactive_integral(self, initial_func="x**2", x_range=(-3, 3)):
        """Visualise the definite integral with adjustable limits a and b."""
        def plot_integral(func_str=initial_func,
                          a=float(x_range[0]) / 2,
                          b=float(x_range[1]) / 2):
            fig, ax = plt.subplots(figsize=(10, 6))
            lo, hi = (a, b) if a <= b else (b, a)
            try:
                x   = sp.Symbol('x')
                sym = sp.sympify(func_str)
                fn  = sp.lambdify(x, sym, 'numpy')
                xs  = np.linspace(x_range[0], x_range[1], 1000)
                ax.plot(xs, fn(xs), 'b-', linewidth=2,
                        label=f'f(x) = {sym}')
                xf = np.linspace(lo, hi, 400)
                ax.fill_between(xf, 0, fn(xf), alpha=0.3, color='green',
                                label=f'∫[{lo:.2f}, {hi:.2f}]')
                ax.axvline(lo, color='red', linestyle='--', alpha=0.6)
                ax.axvline(hi, color='red', linestyle='--', alpha=0.6)
                try:
                    val = float(sp.integrate(sym, (x, lo, hi)).evalf())
                    ax.set_title(f'∫[{lo:.2f},{hi:.2f}] f(x)dx = {val:.4f}')
                except Exception:
                    yn  = fn(np.linspace(lo, hi, 1000))
                    val = float(np.trapz(yn, np.linspace(lo, hi, 1000)))
                    ax.set_title(f'∫[{lo:.2f},{hi:.2f}] f(x)dx ≈ {val:.4f}  (numerical)')
                ax.axhline(0, color='k', linewidth=0.5)
                ax.grid(True, alpha=0.3)
                ax.legend()
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {e}', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12,
                        bbox=dict(boxstyle="round", facecolor="lightcoral"))
            plt.tight_layout()
            plt.show()

        return widgets.interactive(
            plot_integral,
            func_str=widgets.Text(value=initial_func, description='f(x) =',
                                  layout=widgets.Layout(width='300px')),
            a=widgets.FloatSlider(min=float(x_range[0]),
                                  max=float(x_range[1]),
                                  step=0.1, value=float(x_range[0]) / 2,
                                  description='a (lower):'),
            b=widgets.FloatSlider(min=float(x_range[0]),
                                  max=float(x_range[1]),
                                  step=0.1, value=float(x_range[1]) / 2,
                                  description='b (upper):'),
        )

    # ------------------------------------------------------------------
    # Parametric plotter
    # ------------------------------------------------------------------
    def interactive_parametric(self):
        """Interactive parametric curve plotter (x(t), y(t))."""
        def plot_parametric(x_func="cos(t)", y_func="sin(t)",
                            t_min=0.0, t_max=6.28):
            fig, ax = plt.subplots(figsize=(8, 8))
            try:
                t    = sp.Symbol('t')
                xexpr = sp.sympify(x_func)
                yexpr = sp.sympify(y_func)
                xn   = sp.lambdify(t, xexpr, 'numpy')
                yn   = sp.lambdify(t, yexpr, 'numpy')
                ts   = np.linspace(t_min, t_max, 2000)
                xs, ys = xn(ts), yn(ts)
                ax.plot(xs, ys, 'b-', linewidth=2)
                ax.plot(xs[0],  ys[0],  'go', markersize=9, label='Start')
                ax.plot(xs[-1], ys[-1], 'ro', markersize=9, label='End')
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.axis('equal')
                ax.set_title(f'Parametric: x={xexpr}, y={yexpr}')
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {e}', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12,
                        bbox=dict(boxstyle="round", facecolor="lightcoral"))
            plt.tight_layout()
            plt.show()

        return widgets.interactive(
            plot_parametric,
            x_func=widgets.Text(value="cos(t)", description='x(t) =',
                                layout=widgets.Layout(width='250px')),
            y_func=widgets.Text(value="sin(t)", description='y(t) =',
                                layout=widgets.Layout(width='250px')),
            t_min=widgets.FloatSlider(min=-10, max=10,  value=0,    step=0.1,
                                       description='t min:'),
            t_max=widgets.FloatSlider(min=-10, max=20, value=6.28, step=0.1,
                                       description='t max:'),
        )
