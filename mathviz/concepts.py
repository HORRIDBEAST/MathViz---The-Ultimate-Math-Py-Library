import numpy as np
import sympy as sp
from .core import MathViz
import matplotlib.pyplot as plt

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