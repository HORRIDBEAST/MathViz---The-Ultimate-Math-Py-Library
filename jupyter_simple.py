"""
Simple Jupyter-compatible visualizations for MathViz
"""

import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display
import sympy as sp

class JupyterSimpleMathViz:
    """Simplified MathViz for Jupyter notebooks without complex matplotlib widgets"""
    
    def __init__(self):
        # Set inline plotting
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def interactive_quadratic(self):
        """Create an interactive quadratic function explorer"""
        
        def plot_quadratic(a=1.0, b=0.0, c=0.0):
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.linspace(-8, 8, 1000)
            y = a * x**2 + b * x + c
            
            ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a:.2f}x² + {b:.2f}x + {c:.2f}')
            
            # Add vertex if a != 0
            if abs(a) > 1e-10:
                vertex_x = -b / (2 * a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                ax.plot(vertex_x, vertex_y, 'ro', markersize=8, 
                       label=f'Vertex: ({vertex_x:.2f}, {vertex_y:.2f})')
                
                # Add roots if they exist
                discriminant = b**2 - 4*a*c
                if discriminant > 0:
                    root1 = (-b + np.sqrt(discriminant)) / (2*a)
                    root2 = (-b - np.sqrt(discriminant)) / (2*a)
                    ax.plot([root1, root2], [0, 0], 'go', markersize=8, label='Roots')
                elif abs(discriminant) < 1e-10:
                    root = -b / (2*a)
                    ax.plot(root, 0, 'go', markersize=8, label='Root (repeated)')
            
            ax.set_xlim(-8, 8)
            ax.set_ylim(-15, 15)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_title('Interactive Quadratic Function Explorer')
            plt.show()
        
        # Create interactive widget
        return widgets.interactive(
            plot_quadratic,
            a=widgets.FloatSlider(min=-3, max=3, step=0.1, value=1, description='a:'),
            b=widgets.FloatSlider(min=-5, max=5, step=0.1, value=0, description='b:'),
            c=widgets.FloatSlider(min=-5, max=5, step=0.1, value=0, description='c:')
        )
    
    def interactive_function_plotter(self):
        """Interactive function plotter with text input"""
        
        def plot_function(func_str="x**2", x_min=-5, x_max=5):
            fig, ax = plt.subplots(figsize=(10, 6))
            
            try:
                x = sp.Symbol('x')
                func = sp.sympify(func_str)
                func_np = sp.lambdify(x, func, 'numpy')
                
                x_vals = np.linspace(x_min, x_max, 1000)
                y_vals = func_np(x_vals)
                
                ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.set_title(f'Function Plot: f(x) = {func}')
                
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {str(e)}', transform=ax.transAxes, 
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round", facecolor="lightcoral"))
                ax.set_title('Function Plot - Error')
            
            plt.show()
        
        return widgets.interactive(
            plot_function,
            func_str=widgets.Text(value="x**2", description="f(x) ="),
            x_min=widgets.FloatSlider(min=-20, max=0, value=-5, description="x min:"),
            x_max=widgets.FloatSlider(min=0, max=20, value=5, description="x max:")
        )
    
    def interactive_parametric(self):
        """Interactive parametric curve plotter"""
        
        def plot_parametric(x_func="cos(t)", y_func="sin(t)", t_min=0, t_max=6.28):
            fig, ax = plt.subplots(figsize=(10, 6))
            
            try:
                t = sp.Symbol('t')
                x_expr = sp.sympify(x_func)
                y_expr = sp.sympify(y_func)
                
                x_func_np = sp.lambdify(t, x_expr, 'numpy')
                y_func_np = sp.lambdify(t, y_expr, 'numpy')
                
                t_vals = np.linspace(t_min, t_max, 1000)
                x_vals = x_func_np(t_vals)
                y_vals = y_func_np(t_vals)
                
                ax.plot(x_vals, y_vals, 'b-', linewidth=2)
                ax.plot(x_vals[0], y_vals[0], 'go', markersize=8, label='Start')
                ax.plot(x_vals[-1], y_vals[-1], 'ro', markersize=8, label='End')
                
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.axis('equal')
                ax.set_title(f'Parametric Plot: x(t)={x_expr}, y(t)={y_expr}')
                
            except Exception as e:
                ax.text(0.5, 0.5, f'Error: {str(e)}', transform=ax.transAxes,
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round", facecolor="lightcoral"))
                ax.set_title('Parametric Plot - Error')
            
            plt.show()
        
        return widgets.interactive(
            plot_parametric,
            x_func=widgets.Text(value="cos(t)", description="x(t) ="),
            y_func=widgets.Text(value="sin(t)", description="y(t) ="),
            t_min=widgets.FloatSlider(min=-10, max=10, value=0, description="t min:"),
            t_max=widgets.FloatSlider(min=-10, max=20, value=6.28, description="t max:")
        )

# Convenience functions for direct use in notebooks
def create_quadratic_explorer():
    """Create interactive quadratic explorer"""
    viz = JupyterSimpleMathViz()
    return viz.interactive_quadratic()

def create_function_plotter():
    """Create interactive function plotter"""
    viz = JupyterSimpleMathViz()
    return viz.interactive_function_plotter()

def create_parametric_plotter():
    """Create interactive parametric plotter"""
    viz = JupyterSimpleMathViz()
    return viz.interactive_parametric()