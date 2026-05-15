import numpy as np
import sympy as sp
from .core import MathViz
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from statistics import NormalDist
from math import lgamma

# Try to import mplcursors for hover tooltips
try:
    import mplcursors
    MPLCURSORS_AVAILABLE = True
except ImportError:
    MPLCURSORS_AVAILABLE = False
    print("Note: Install mplcursors for hover tooltips: pip install mplcursors")

class AlgebraVisualizer(MathViz):
    """Visualizations for algebraic concepts with hover tooltips"""
    def __init__(self, figsize=(12, 8)):
        super().__init__(figsize=figsize)

    def quadratic_explorer(self, a_range=(-5, 5), b_range=(-10, 10), c_range=(-10, 10),
                          x_range=(-10, 10), y_range=(-25, 25)):
        """
        Interactive quadratic function explorer with hover tooltips
        Args:
            a_range: Range for coefficient 'a' (min, max)
            b_range: Range for coefficient 'b' (min, max) 
            c_range: Range for coefficient 'c' (min, max)
            x_range: X-axis range (min, max)
            y_range: Y-axis range (min, max)
        """
        self.create_figure()

        # Add sliders with user-defined ranges
        slider_a = self.add_slider('a', a_range[0], a_range[1], 1, [0.2, 0.15, 0.2, 0.03])
        slider_b = self.add_slider('b', b_range[0], b_range[1], 0, [0.2, 0.10, 0.2, 0.03])
        slider_c = self.add_slider('c', c_range[0], c_range[1], 0, [0.2, 0.05, 0.2, 0.03])

        # Initial plot
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = x**2
        line, = self.ax.plot(x, y, 'b-', linewidth=2, label='y = ax² + bx + c')
        vertex_point, = self.ax.plot([], [], 'ro', markersize=10, label='Vertex', picker=5)
        roots_points, = self.ax.plot([], [], 'go', markersize=10, label='Roots', picker=5)

        self.ax.set_xlim(x_range[0], x_range[1])
        self.ax.set_ylim(y_range[0], y_range[1])
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        tooltip_text = " (Hover over points)" if MPLCURSORS_AVAILABLE else ""
        self.ax.set_title(f'Interactive Quadratic Function Explorer{tooltip_text}')

        def update(val):
            a = slider_a.val
            b = slider_b.val
            c = slider_c.val

            if abs(a) < 1e-10:
                y = b * x + c
                vertex_point.set_data([], [])
                if abs(b) > 1e-10:
                    root = -c / b
                    if x_range[0] <= root <= x_range[1]:
                        roots_points.set_data([root], [0])
                    else:
                        roots_points.set_data([], [])
                else:
                    roots_points.set_data([], [])
                self.ax.set_title(f'y = {b:.1f}x + {c:.1f} (Linear){tooltip_text}')
            else:
                y = a * x**2 + b * x + c
                
                vertex_x = -b / (2 * a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                vertex_point.set_data([vertex_x], [vertex_y])

                discriminant = b**2 - 4*a*c
                if discriminant >= 0:
                    root1 = (-b + np.sqrt(discriminant)) / (2*a)
                    root2 = (-b - np.sqrt(discriminant)) / (2*a)
                    visible_roots = []
                    if x_range[0] <= root1 <= x_range[1]:
                        visible_roots.append(root1)
                    if x_range[0] <= root2 <= x_range[1] and abs(root1 - root2) > 1e-10:
                        visible_roots.append(root2)
                    
                    if visible_roots:
                        roots_points.set_data(visible_roots, [0] * len(visible_roots))
                    else:
                        roots_points.set_data([], [])
                else:
                    roots_points.set_data([], [])
                
                self.ax.set_title(f'y = {a:.2f}x² + {b:.2f}x + {c:.2f}{tooltip_text}')

            line.set_ydata(y)
            self.fig.canvas.draw()

        slider_a.on_changed(update)
        slider_b.on_changed(update)
        slider_c.on_changed(update)
        update(0)
        
        # Add hover tooltips
        if MPLCURSORS_AVAILABLE:
            cursor_vertex = mplcursors.cursor(vertex_point, hover=True)
            @cursor_vertex.connect("add")
            def on_vertex_add(sel):
                x_val, y_val = sel.target
                sel.annotation.set_text(f'Vertex\nx = {x_val:.3f}\ny = {y_val:.3f}')
                sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.9)
                sel.annotation.arrow_patch.set(color="yellow", linewidth=2)
            
            cursor_roots = mplcursors.cursor(roots_points, hover=True)
            @cursor_roots.connect("add")
            def on_roots_add(sel):
                x_val = sel.target[0]
                sel.annotation.set_text(f'Root\nx = {x_val:.3f}\ny = 0.000')
                sel.annotation.get_bbox_patch().set(fc="lightgreen", alpha=0.9)
                sel.annotation.arrow_patch.set(color="green", linewidth=2)

        return self.fig

    def polynomial_explorer(self, degree=3, x_range=(-5, 5), y_range=(-10, 10)):
        """
        Interactive polynomial explorer with hover tooltips
        Args:
            degree: Degree of polynomial (2-5 supported)
            x_range: X-axis range
            y_range: Y-axis range
        """
        if degree < 2 or degree > 5:
            raise ValueError("Degree must be between 2 and 5")
            
        self.create_figure()
        
        sliders = {}
        slider_positions = [
            [0.15, 0.15, 0.15, 0.03],
            [0.35, 0.15, 0.15, 0.03], 
            [0.55, 0.15, 0.15, 0.03],
            [0.15, 0.10, 0.15, 0.03],
            [0.35, 0.10, 0.15, 0.03],
            [0.55, 0.10, 0.15, 0.03]
        ]
        
        for i in range(degree + 1):
            coef_name = f'a{degree-i}'
            initial_val = 1 if i == 0 else 0
            sliders[coef_name] = self.add_slider(
                coef_name, -5, 5, initial_val, slider_positions[i]
            )

        x = np.linspace(x_range[0], x_range[1], 1000)
        y = x**degree
        line, = self.ax.plot(x, y, 'b-', linewidth=2, label=f'Polynomial (degree {degree})')

        self.ax.set_xlim(x_range[0], x_range[1])
        self.ax.set_ylim(y_range[0], y_range[1])
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        self.ax.set_title(f'Interactive Polynomial Explorer (Degree {degree})')

        def update(val):
            y = np.zeros_like(x)
            equation_parts = []
            
            for i in range(degree + 1):
                coef_name = f'a{degree-i}'
                coef_val = sliders[coef_name].val
                power = degree - i
                
                if abs(coef_val) > 1e-10:
                    y += coef_val * (x ** power)
                    
                    if power == 0:
                        equation_parts.append(f"{coef_val:.2f}")
                    elif power == 1:
                        equation_parts.append(f"{coef_val:.2f}x")
                    else:
                        equation_parts.append(f"{coef_val:.2f}x^{power}")
            
            equation = " + ".join(equation_parts).replace("+ -", "- ")
            line.set_ydata(y)
            self.ax.set_title(f'y = {equation}')
            self.fig.canvas.draw()

        for slider in sliders.values():
            slider.on_changed(update)
        update(0)
        
        # Add hover for the line itself
        if MPLCURSORS_AVAILABLE:
            cursor = mplcursors.cursor(line, hover=True)
            @cursor.connect("add")
            def on_add(sel):
                x_val, y_val = sel.target
                sel.annotation.set_text(f'x = {x_val:.3f}\ny = {y_val:.3f}')

        return self.fig

class CalculusVisualizer(MathViz):
    """Visualizations for calculus concepts with hover tooltips"""
    def __init__(self, figsize=(12, 8)):
        super().__init__(figsize=figsize)

    def derivative_visualizer(self, func_str="x**3 - 3*x**2 + 2*x", x_range=(-3, 5), 
                            point_range=None, show_function_input=True):
        """
        Visualize function and derivative with hover tooltips
        """
        if point_range is None:
            point_range = x_range
            
        self.create_figure()
        
        if show_function_input:
            self.fig.subplots_adjust(bottom=0.35)
            textbox = self.add_textbox('f(x) = ', func_str, [0.2, 0.25, 0.5, 0.03])

        current_func_str = func_str
        self.current_elements = {}

        def plot_function(func_string):
            try:
                self.ax.clear()
                
                x = sp.Symbol('x')
                func = sp.sympify(func_string)
                derivative = sp.diff(func, x)

                func_np = sp.lambdify(x, func, 'numpy')
                deriv_np = sp.lambdify(x, derivative, 'numpy')

                x_vals = np.linspace(x_range[0], x_range[1], 1000)
                y_func = func_np(x_vals)
                y_deriv = deriv_np(x_vals)

                func_line, = self.ax.plot(x_vals, y_func, 'b-', linewidth=2, label=f'f(x) = {func}')
                deriv_line, = self.ax.plot(x_vals, y_deriv, 'r--', linewidth=2, label=f"f'(x) = {derivative}")

                tangent_line, = self.ax.plot([], [], 'g-', linewidth=2, alpha=0.7, label='Tangent Line')
                point_marker, = self.ax.plot([], [], 'ko', markersize=10, picker=5)

                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                tooltip_text = " (Hover over point)" if MPLCURSORS_AVAILABLE else ""
                self.ax.set_title(f'Function and Derivative Visualization{tooltip_text}')
                
                self.current_elements = {
                    'func_np': func_np,
                    'deriv_np': deriv_np,
                    'tangent_line': tangent_line,
                    'point_marker': point_marker,
                    'func_line': func_line,
                    'deriv_line': deriv_line
                }
                
                # Add hover to function and derivative lines
                if MPLCURSORS_AVAILABLE:
                    cursor_func = mplcursors.cursor(func_line, hover=True)
                    @cursor_func.connect("add")
                    def on_func_add(sel):
                        x_val, y_val = sel.target
                        slope = deriv_np(x_val)
                        sel.annotation.set_text(f'f({x_val:.2f}) = {y_val:.3f}\nf\'({x_val:.2f}) = {slope:.3f}')
                        sel.annotation.get_bbox_patch().set(fc="lightblue", alpha=0.9)
                    
                    cursor_deriv = mplcursors.cursor(deriv_line, hover=True)
                    @cursor_deriv.connect("add")
                    def on_deriv_add(sel):
                        x_val, y_val = sel.target
                        sel.annotation.set_text(f"f'({x_val:.2f}) = {y_val:.3f}\n(slope at x={x_val:.2f})")
                        sel.annotation.get_bbox_patch().set(fc="lightcoral", alpha=0.9)
                
                return True
                
            except Exception as e:
                self.ax.clear()
                self.ax.text(0.5, 0.5, f"Error: Invalid function '{func_string}'\n{str(e)}", 
                           transform=self.ax.transAxes, ha='center', va='center', 
                           fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
                self.current_elements = {}
                return False

        plot_function(current_func_str)

        slider_point = self.add_slider('x', point_range[0], point_range[1], 
                                     (point_range[0] + point_range[1])/2, 
                                     [0.2, 0.1, 0.5, 0.03])

        def update_tangent(val):
            if not self.current_elements:
                return
                
            x_point = slider_point.val
            try:
                func_np = self.current_elements['func_np']
                deriv_np = self.current_elements['deriv_np']
                tangent_line = self.current_elements['tangent_line']
                point_marker = self.current_elements['point_marker']
                
                y_point = func_np(x_point)
                slope = deriv_np(x_point)

                point_marker.set_data([x_point], [y_point])

                x_tangent = np.linspace(x_point - 1, x_point + 1, 100)
                y_tangent = slope * (x_tangent - x_point) + y_point
                tangent_line.set_data(x_tangent, y_tangent)

                self.ax.set_title(f'Tangent at x={x_point:.2f}, slope={slope:.3f}')
                self.fig.canvas.draw()
            except Exception as e:
                print(f"Error updating tangent: {e}")

        def update_function(text):
            nonlocal current_func_str
            current_func_str = text
            if plot_function(text):
                update_tangent(slider_point.val)
            self.fig.canvas.draw()

        slider_point.on_changed(update_tangent)
        if show_function_input:
            textbox.on_submit(update_function)
        
        update_tangent(slider_point.val)
        
        # Add hover to tangent point
        if MPLCURSORS_AVAILABLE and 'point_marker' in self.current_elements:
            cursor_point = mplcursors.cursor(self.current_elements['point_marker'], hover=True)
            @cursor_point.connect("add")
            def on_point_add(sel):
                x_val, y_val = sel.target
                slope = self.current_elements['deriv_np'](x_val)
                sel.annotation.set_text(f'Tangent Point\nx = {x_val:.3f}\ny = {y_val:.3f}\nslope = {slope:.3f}')
                sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.9)

        return self.fig

    def integral_visualizer(self, func_str="x**2", x_range=(-2, 2), 
                          integration_range=(-1, 1)):
        """
        Visualize definite integral with hover tooltips
        """
        self.create_figure()
        self.fig.subplots_adjust(bottom=0.35)
        
        textbox = self.add_textbox('f(x) = ', func_str, [0.2, 0.25, 0.5, 0.03])
        
        slider_a = self.add_slider('a', x_range[0], x_range[1], integration_range[0], 
                                 [0.15, 0.15, 0.2, 0.03])
        slider_b = self.add_slider('b', x_range[0], x_range[1], integration_range[1], 
                                 [0.15, 0.10, 0.2, 0.03])

        current_func_str = func_str
        self.integral_elements = {}

        def plot_integral(func_string):
            try:
                self.ax.clear()
                
                x = sp.Symbol('x')
                func = sp.sympify(func_string)
                func_np = sp.lambdify(x, func, 'numpy')

                x_vals = np.linspace(x_range[0], x_range[1], 1000)
                y_vals = func_np(x_vals)
                func_line, = self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')

                self.integral_elements = {
                    'func': func,
                    'func_np': func_np,
                    'x_vals': x_vals,
                    'y_vals': y_vals,
                    'func_line': func_line
                }
                
                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                self.ax.set_title('Definite Integral Visualization')
                
                # Add hover to function line
                if MPLCURSORS_AVAILABLE:
                    cursor = mplcursors.cursor(func_line, hover=True)
                    @cursor.connect("add")
                    def on_add(sel):
                        x_val, y_val = sel.target
                        sel.annotation.set_text(f'x = {x_val:.3f}\nf(x) = {y_val:.3f}')
                
                return True
                
            except Exception as e:
                self.ax.clear()
                self.ax.text(0.5, 0.5, f"Error: Invalid function '{func_string}'", 
                           transform=self.ax.transAxes, ha='center', va='center')
                self.integral_elements = {}
                return False

        def update_integral(val):
            """Update the shaded integral region"""
            if not self.integral_elements:
                return
                
            a = slider_a.val
            b = slider_b.val
            
            if a > b:
                a, b = b, a
            
            try:
                func = self.integral_elements['func']
                func_np = self.integral_elements['func_np']
                
                # Clear previous fill
                self.ax.clear()
                
                # Replot function
                x_vals = self.integral_elements['x_vals']
                y_vals = self.integral_elements['y_vals']
                func_line, = self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
                
                # RE-ADD HOVER AFTER CLEARING
                if MPLCURSORS_AVAILABLE:
                    cursor = mplcursors.cursor(func_line, hover=True)
                    @cursor.connect("add")
                    def on_add(sel):
                        x_val, y_val = sel.target
                        sel.annotation.set_text(f'x = {x_val:.3f}\nf(x) = {y_val:.3f}')
                
                # Create integral region
                x_fill = np.linspace(a, b, 200)
                y_fill = func_np(x_fill)
                self.ax.fill_between(x_fill, 0, y_fill, alpha=0.3, color='green', 
                                   label=f'∫[{a:.2f}, {b:.2f}] f(x)dx')
                
                # Calculate numerical integral
                try:
                    x_sym = sp.Symbol('x')
                    integral_result = sp.integrate(func, (x_sym, a, b))
                    integral_value = float(integral_result.evalf())
                    
                    self.ax.set_title(f'∫[{a:.2f}, {b:.2f}] f(x)dx = {integral_value:.3f}')
                except:
                    x_num = np.linspace(a, b, 1000)
                    y_num = func_np(x_num)
                    integral_value = np.trapz(y_num, x_num)
                    self.ax.set_title(f'∫[{a:.2f}, {b:.2f}] f(x)dx ≈ {integral_value:.3f}')
                
                self.ax.axvline(x=a, color='red', linestyle='--', alpha=0.7, label=f'a = {a:.2f}')
                self.ax.axvline(x=b, color='red', linestyle='--', alpha=0.7, label=f'b = {b:.2f}')
                
                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                self.fig.canvas.draw()
                
            except Exception as e:
                print(f"Error updating integral: {e}")
                
        def update_function(text):
            nonlocal current_func_str
            current_func_str = text
            if plot_integral(text):
                update_integral(None)

        plot_integral(current_func_str)
        
        slider_a.on_changed(update_integral)
        slider_b.on_changed(update_integral)
        textbox.on_submit(update_function)
        
        update_integral(None)
        
        return self.fig


class LinAlgVisualizer(MathViz):
    """Visualizations for linear algebra concepts."""

    def __init__(self, figsize=(10, 10)):
        super().__init__(figsize=figsize)

    def space_transformer(self, initial_matrix=None,
                          grid_range=(-5, 5),
                          axis_limit=8):
        """
        Visualize a continuous 2D matrix transformation.

        Interpolation uses M(t) = (1 - t)I + tA, where A is the user matrix.

        Args:
            initial_matrix: 2x2 matrix [[a, b], [c, d]].
            grid_range: Integer grid extent as (min, max).
            axis_limit: Plot axis limit for both x and y.
        Returns:
            Matplotlib figure.
        """
        if initial_matrix is None:
            initial_matrix = [[2, 1], [-1, 1]]

        # Validate matrix shape early for clear errors.
        arr = np.array(initial_matrix, dtype=float)
        if arr.shape != (2, 2):
            raise ValueError("initial_matrix must be a 2x2 matrix, e.g. [[2, 1], [-1, 1]].")

        self.create_figure()
        self.fig.subplots_adjust(bottom=0.35)

        # Matrix element sliders for A = [[a, b], [c, d]].
        slider_a = self.add_slider('a (i-hat x)', -4, 4, arr[0, 0], [0.15, 0.25, 0.3, 0.03])
        slider_b = self.add_slider('b (j-hat x)', -4, 4, arr[0, 1], [0.60, 0.25, 0.3, 0.03])
        slider_c = self.add_slider('c (i-hat y)', -4, 4, arr[1, 0], [0.15, 0.20, 0.3, 0.03])
        slider_d = self.add_slider('d (j-hat y)', -4, 4, arr[1, 1], [0.60, 0.20, 0.3, 0.03])
        slider_t = self.add_slider('Time (t)', 0, 1, 1, [0.2, 0.10, 0.6, 0.04])

        # Build reference grid.
        g_min, g_max = int(grid_range[0]), int(grid_range[1])
        grid_lines = []
        for i in range(g_min, g_max + 1):
            grid_lines.append(np.array([[i, i], [g_min, g_max]], dtype=float))
            grid_lines.append(np.array([[g_min, g_max], [i, i]], dtype=float))

        self.ax.set_xlim(-axis_limit, axis_limit)
        self.ax.set_ylim(-axis_limit, axis_limit)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2)

        plotted_lines = []
        for _ in grid_lines:
            line, = self.ax.plot([], [], color='gray', alpha=0.45, linewidth=1)
            plotted_lines.append(line)

        # Basis vectors and determinant parallelogram.
        i_vec = self.ax.quiver(0, 0, 1, 0, angles='xy', scale_units='xy', scale=1,
                               color='green', zorder=5, label='i-hat')
        j_vec = self.ax.quiver(0, 0, 0, 1, angles='xy', scale_units='xy', scale=1,
                               color='red', zorder=5, label='j-hat')
        det_poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], closed=True,
                           facecolor='yellow', edgecolor='goldenrod', alpha=0.3,
                           label='Determinant Area', zorder=2)
        self.ax.add_patch(det_poly)
        self.ax.legend(loc='upper right')

        def update(val=None):
            a, b = slider_a.val, slider_b.val
            c, d = slider_c.val, slider_d.val
            t = slider_t.val

            # M(t) = (1 - t)I + tA
            m11 = (1 - t) + t * a
            m12 = t * b
            m21 = t * c
            m22 = (1 - t) + t * d

            for original_line, plot_line in zip(grid_lines, plotted_lines):
                x = original_line[0]
                y = original_line[1]
                new_x = m11 * x + m12 * y
                new_y = m21 * x + m22 * y
                plot_line.set_data(new_x, new_y)

            i_vec.set_UVC(m11, m21)
            j_vec.set_UVC(m12, m22)

            poly = np.array([[0, 0], [m11, m21], [m11 + m12, m21 + m22], [m12, m22]], dtype=float)
            det_poly.set_xy(poly)

            current_det = (m11 * m22) - (m12 * m21)
            self.ax.set_title(f"Space Transformer | Det = {current_det:.3f}")
            self.fig.canvas.draw_idle()

        for slider in [slider_a, slider_b, slider_c, slider_d, slider_t]:
            slider.on_changed(update)

        update()
        return self.fig

    def eigenvector_discovery_mode(self, initial_matrix=None,
                                   vectors_count=48,
                                   axis_limit=3):
        """
        Highlight vectors that stay on their span after transformation.

        Args:
            initial_matrix: 2x2 matrix [[a, b], [c, d]].
            vectors_count: Number of unit vectors sampled on the circle.
            axis_limit: Plot axis limit for both x and y.
        Returns:
            Matplotlib figure.
        """
        if initial_matrix is None:
            initial_matrix = [[2, 1], [1, 2]]

        arr = np.array(initial_matrix, dtype=float)
        if arr.shape != (2, 2):
            raise ValueError("initial_matrix must be a 2x2 matrix, e.g. [[2, 1], [1, 2]].")

        self.create_figure()
        self.fig.subplots_adjust(bottom=0.35)

        slider_a = self.add_slider('a', -4, 4, arr[0, 0], [0.15, 0.25, 0.3, 0.03])
        slider_b = self.add_slider('b', -4, 4, arr[0, 1], [0.60, 0.25, 0.3, 0.03])
        slider_c = self.add_slider('c', -4, 4, arr[1, 0], [0.15, 0.20, 0.3, 0.03])
        slider_d = self.add_slider('d', -4, 4, arr[1, 1], [0.60, 0.20, 0.3, 0.03])
        slider_t = self.add_slider('Time (t)', 0, 1, 1, [0.2, 0.10, 0.6, 0.04])

        self.ax.set_xlim(-axis_limit, axis_limit)
        self.ax.set_ylim(-axis_limit, axis_limit)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2)

        theta = np.linspace(0, 2 * np.pi, 400)
        unit_circle, = self.ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.4, label='Unit Circle')
        transformed_shape, = self.ax.plot([], [], color='tab:blue', linewidth=2, label='Transformed Circle')

        unit_angles = np.linspace(0, 2 * np.pi, vectors_count, endpoint=False)
        unit_vecs = np.stack([np.cos(unit_angles), np.sin(unit_angles)], axis=1)

        # Keep references to many line artists for fast updates.
        candidate_lines = []
        for _ in range(vectors_count):
            line, = self.ax.plot([], [], color='lightgray', linewidth=1.2, alpha=0.8)
            candidate_lines.append(line)

        eig_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                va='top', ha='left', fontsize=10,
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

        self.ax.legend(loc='upper right')

        def update(val=None):
            a, b = slider_a.val, slider_b.val
            c, d = slider_c.val, slider_d.val
            t = slider_t.val

            m11 = (1 - t) + t * a
            m12 = t * b
            m21 = t * c
            m22 = (1 - t) + t * d
            m = np.array([[m11, m12], [m21, m22]], dtype=float)

            # Transform unit circle.
            circle_pts = np.stack([np.cos(theta), np.sin(theta)], axis=1)
            transformed_pts = (m @ circle_pts.T).T
            transformed_shape.set_data(transformed_pts[:, 0], transformed_pts[:, 1])

            # Parallel test: cross(u, v) ~= 0 where v = M u.
            tol = 0.06
            for i, u in enumerate(unit_vecs):
                v = m @ u
                cross_mag = abs(u[0] * v[1] - u[1] * v[0])
                line = candidate_lines[i]
                line.set_data([0, v[0]], [0, v[1]])
                if cross_mag <= tol:
                    line.set_color('crimson')
                    line.set_linewidth(2.6)
                    line.set_alpha(0.95)
                else:
                    line.set_color('lightgray')
                    line.set_linewidth(1.2)
                    line.set_alpha(0.8)

            # Exact eigensystem from matrix (for labels).
            eigvals, eigvecs = np.linalg.eig(m)
            if np.all(np.isreal(eigvals)):
                eigvals = np.real(eigvals)
                det_val = np.linalg.det(m)
                eig_text.set_text(
                    f"Eigenvalues: λ1={eigvals[0]:.3f}, λ2={eigvals[1]:.3f}\n"
                    f"det(M)={det_val:.3f}, tr(M)={np.trace(m):.3f}"
                )
            else:
                det_val = np.linalg.det(m)
                eig_text.set_text(
                    f"Eigenvalues are complex\n"
                    f"det(M)={det_val:.3f}, tr(M)={np.trace(m):.3f}"
                )

            self.ax.set_title('Eigenvector Discovery Mode')
            self.fig.canvas.draw_idle()

        for slider in [slider_a, slider_b, slider_c, slider_d, slider_t]:
            slider.on_changed(update)

        update()
        return self.fig


class StatsVisualizer(MathViz):
    """Visualizations for statistics and probability concepts."""

    def __init__(self, figsize=(12, 8)):
        super().__init__(figsize=figsize)
        self._normal = NormalDist(mu=0.0, sigma=1.0)

    def _beta_pdf(self, x_vals, alpha, beta):
        """Numerically stable beta PDF without requiring scipy."""
        eps = 1e-9
        x = np.clip(x_vals, eps, 1 - eps)
        log_norm = lgamma(alpha + beta) - lgamma(alpha) - lgamma(beta)
        log_pdf = log_norm + (alpha - 1) * np.log(x) + (beta - 1) * np.log(1 - x)
        return np.exp(log_pdf)

    def hypothesis_tester(self,
                          n_range=(10, 500),
                          effect_range=(0.0, 3.0),
                          alpha_range=(0.01, 0.20)):
        """
        Interactive Type-I/Type-II error and power visualizer.

        Assumes two-sided z-test with unit variance and standardized effect size.
        """
        self.create_figure()
        self.fig.subplots_adjust(bottom=0.34)

        slider_n = self.add_slider('sample size n', n_range[0], n_range[1], 60, [0.10, 0.20, 0.34, 0.03])
        slider_eff = self.add_slider('effect size d', effect_range[0], effect_range[1], 0.6, [0.58, 0.20, 0.34, 0.03])
        slider_alpha = self.add_slider('alpha', alpha_range[0], alpha_range[1], 0.05, [0.20, 0.12, 0.60, 0.03])

        for s in (slider_n, slider_eff, slider_alpha):
            s.label.set_fontsize(10)
            s.valtext.set_fontsize(10)

        info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                 va='top', ha='left', fontsize=10,
                                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

        def update(val=None):
            n = max(2, int(round(slider_n.val)))
            d = slider_eff.val
            alpha = slider_alpha.val

            delta = d * np.sqrt(n)
            z_crit = self._normal.inv_cdf(1 - alpha / 2)

            x_min = min(-6, delta - 6)
            x_max = max(6, delta + 6)
            x = np.linspace(x_min, x_max, 1200)

            # H0: Z~N(0,1), H1: Z~N(delta,1)
            pdf_h0 = np.array([self._normal.pdf(v) for v in x])
            pdf_h1 = np.array([NormalDist(mu=delta, sigma=1).pdf(v) for v in x])

            self.ax.clear()
            self.ax.plot(x, pdf_h0, color='tab:blue', linewidth=2, label='H0: N(0,1)')
            self.ax.plot(x, pdf_h1, color='tab:orange', linewidth=2, label=f'H1: N(δ,1), δ={delta:.2f}')

            # Type-I (alpha tails under H0)
            left_tail = x <= -z_crit
            right_tail = x >= z_crit
            self.ax.fill_between(x[left_tail], 0, pdf_h0[left_tail], color='red', alpha=0.25, label='Type I area')
            self.ax.fill_between(x[right_tail], 0, pdf_h0[right_tail], color='red', alpha=0.25)

            # Type-II (beta center under H1)
            beta_mask = (x >= -z_crit) & (x <= z_crit)
            self.ax.fill_between(x[beta_mask], 0, pdf_h1[beta_mask], color='purple', alpha=0.25, label='Type II area')

            beta = NormalDist(mu=delta, sigma=1).cdf(z_crit) - NormalDist(mu=delta, sigma=1).cdf(-z_crit)
            power = 1.0 - beta
            p_value_at_delta = 2 * (1 - self._normal.cdf(abs(delta)))

            self.ax.axvline(-z_crit, color='black', linestyle='--', alpha=0.6)
            self.ax.axvline(z_crit, color='black', linestyle='--', alpha=0.6)
            self.ax.set_title('Interactive Hypothesis Tester')
            self.ax.set_xlabel('z')
            self.ax.set_ylabel('Density')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend(loc='upper right')

            info_text = (
                f"n={n}, d={d:.2f}, α={alpha:.3f}\n"
                f"β={beta:.3f}, Power={power:.3f}\n"
                f"Approx p-value at z=δ: {p_value_at_delta:.4f}"
            )
            self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

            self.fig.canvas.draw_idle()

        for s in [slider_n, slider_eff, slider_alpha]:
            s.on_changed(update)

        update()
        return self.fig

    def bayesian_updater(self,
                         prior_alpha=2.0,
                         prior_beta=2.0,
                         max_flips=200):
        """
        Real-time Beta-Binomial Bayesian updater.

        Prior: Beta(alpha, beta)
        Likelihood data: heads out of flips
        Posterior: Beta(alpha+heads, beta+flips-heads)
        """
        self.create_figure()
        self.fig.subplots_adjust(bottom=0.34)

        slider_a0 = self.add_slider('prior α', 1.0, 20.0, prior_alpha, [0.08, 0.20, 0.36, 0.03])
        slider_b0 = self.add_slider('prior β', 1.0, 20.0, prior_beta, [0.58, 0.20, 0.36, 0.03])
        slider_flips = self.add_slider('flips n', 1, max_flips, 30, [0.08, 0.12, 0.36, 0.03])
        slider_heads = self.add_slider('heads k', 0, max_flips, 18, [0.58, 0.12, 0.36, 0.03])

        for s in (slider_a0, slider_b0, slider_flips, slider_heads):
            s.label.set_fontsize(10)
            s.valtext.set_fontsize(10)

        def update(val=None):
            a0 = slider_a0.val
            b0 = slider_b0.val
            n = int(round(slider_flips.val))
            k = int(round(slider_heads.val))
            if k > n:
                k = n

            a1 = a0 + k
            b1 = b0 + (n - k)

            x = np.linspace(0, 1, 1000)
            prior_pdf = self._beta_pdf(x, a0, b0)
            post_pdf = self._beta_pdf(x, a1, b1)

            self.ax.clear()
            self.ax.plot(x, prior_pdf, color='tab:blue', linewidth=2, label=f'Prior Beta({a0:.1f},{b0:.1f})')
            self.ax.plot(x, post_pdf, color='tab:green', linewidth=2, label=f'Posterior Beta({a1:.1f},{b1:.1f})')

            prior_mean = a0 / (a0 + b0)
            post_mean = a1 / (a1 + b1)

            self.ax.axvline(prior_mean, color='tab:blue', linestyle='--', alpha=0.7)
            self.ax.axvline(post_mean, color='tab:green', linestyle='--', alpha=0.7)

            self.ax.set_title('Real-Time Bayesian Updater (Beta-Binomial)')
            self.ax.set_xlabel('Probability of success p')
            self.ax.set_ylabel('Density')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend(loc='upper right')

            info = (
                f"Data: k={k} heads out of n={n}\n"
                f"Prior mean={prior_mean:.3f}\n"
                f"Posterior mean={post_mean:.3f}"
            )
            self.ax.text(0.02, 0.98, info, transform=self.ax.transAxes,
                         va='top', ha='left', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

            self.fig.canvas.draw_idle()

        for s in [slider_a0, slider_b0, slider_flips, slider_heads]:
            s.on_changed(update)

        update()
        return self.fig