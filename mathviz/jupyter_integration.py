try:
    from IPython.display import display
    import ipywidgets as widgets
    from ipywidgets import interact
    JUPYTER_AVAILABLE = True
except ImportError:
    JUPYTER_AVAILABLE = False
    widgets = None

class JupyterMathViz:
    """MathViz integration for Jupyter notebooks"""
    def __init__(self):
        if not JUPYTER_AVAILABLE:
            raise ImportError("Jupyter integration requires ipywidgets. Install with: pip install ipywidgets")

    def interactive_quadratic(self):
        """Interactive quadratic function for Jupyter"""
        def plot_quadratic(a=1.0, b=0.0, c=0.0):
            import matplotlib.pyplot as plt
            import numpy as np
            fig, ax = plt.subplots(figsize=(10, 6))

            x = np.linspace(-10, 10, 1000)
            y = a * x**2 + b * x + c

            ax.plot(x, y, 'b-', linewidth=2, label=f'y = {a}x² + {b}x + {c}')

            # Add vertex
            if a != 0:
                vertex_x = -b / (2 * a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                ax.plot(vertex_x, vertex_y, 'ro', markersize=8, label=f'Vertex: ({vertex_x:.2f}, {vertex_y:.2f})')

                # Add roots if they exist
                discriminant = b**2 - 4*a*c
                if discriminant >= 0:
                    root1 = (-b + np.sqrt(discriminant)) / (2*a)
                    root2 = (-b - np.sqrt(discriminant)) / (2*a)
                    ax.plot([root1, root2], [0, 0], 'go', markersize=8, label='Roots')

            ax.set_xlim(-10, 10)
            ax.set_ylim(-25, 25)
            ax.grid(True, alpha=0.3)
            ax.legend()
            ax.set_title('Interactive Quadratic Function')
            plt.show()

        return interact(plot_quadratic,
                        a=widgets.FloatSlider(min=-5, max=5, step=0.1, value=1, description='a'),
                        b=widgets.FloatSlider(min=-10, max=10, step=0.1, value=0, description='b'),
                        c=widgets.FloatSlider(min=-10, max=10, step=0.1, value=0, description='c'))