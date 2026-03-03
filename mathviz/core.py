import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from typing import Callable, List, Tuple, Optional, Union
import warnings

class MathViz:
    """Base class for mathematical visualizations"""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize MathViz with figure size
        Args:
            figsize: Figure size as (width, height)
        """
        self.figsize = figsize
        self.fig = None
        self.ax = None
        self.sliders = {}
        self.widgets = {}
        
    def create_figure(self, subplot_layout: Tuple[int, int, int] = (1, 1, 1)):
        """
        Create matplotlib figure and axes
        Args:
            subplot_layout: (nrows, ncols, index) for subplot
        """
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.fig.subplots_adjust(bottom=0.25)  # Make room for sliders
        return self.fig, self.ax
    
    def add_slider(self, name: str, valmin: float, valmax: float, 
                   valinit: float, position: List[float]) -> Slider:
        """
        Add a slider widget
        Args:
            name: Slider name/label
            valmin: Minimum value
            valmax: Maximum value
            valinit: Initial value
            position: [left, bottom, width, height] in figure coordinates
        Returns:
            Slider widget
        """
        ax_slider = plt.axes(position)
        slider = Slider(ax_slider, name, valmin, valmax, valinit=valinit)
        self.sliders[name] = slider
        return slider
    
    def add_button(self, label: str, position: List[float], 
                   callback: Optional[Callable] = None) -> Button:
        """
        Add a button widget
        Args:
            label: Button text
            position: [left, bottom, width, height]
            callback: Function to call when clicked
        Returns:
            Button widget
        """
        ax_button = plt.axes(position)
        button = Button(ax_button, label)
        if callback:
            button.on_clicked(callback)
        self.widgets[label] = button
        return button
    
    def add_textbox(self, label: str, initial: str, position: List[float],
                    callback: Optional[Callable] = None) -> TextBox:
        """
        Add a text input box
        Args:
            label: Text box label
            initial: Initial text
            position: [left, bottom, width, height]
            callback: Function to call on submit
        Returns:
            TextBox widget
        """
        ax_textbox = plt.axes(position)
        textbox = TextBox(ax_textbox, label, initial=initial)
        if callback:
            textbox.on_submit(callback)
        self.widgets[label] = textbox
        return textbox
    
    def function_explorer(self, initial_func: str = "x**2", 
                         x_range: Tuple[float, float] = (-5, 5),
                         auto_detect_features: bool = True):
        """
        General purpose function explorer with feature detection
        Args:
            initial_func: Initial function string
            x_range: X-axis range
            auto_detect_features: Whether to automatically detect critical points
        """
        self.create_figure()
        
        # Make room for controls
        self.fig.subplots_adjust(bottom=0.4)
        
        # Add function input
        textbox = self.add_textbox('f(x) = ', initial_func, [0.2, 0.25, 0.5, 0.04])
        
        # Add range controls
        x_min_slider = self.add_slider('x_min', -20, 0, x_range[0], [0.15, 0.15, 0.2, 0.03])
        x_max_slider = self.add_slider('x_max', 0, 20, x_range[1], [0.45, 0.15, 0.2, 0.03])
        
        current_func_str = initial_func
        plot_elements = {}
        
        def plot_function(func_string, x_min, x_max):
            """Plot function with feature detection"""
            try:
                # Clear previous plots
                self.ax.clear()
                
                # Parse function
                x = sp.Symbol('x')
                func = sp.sympify(func_string)
                
                # Create numpy function
                func_np = sp.lambdify(x, func, 'numpy')
                
                # Create x values
                x_vals = np.linspace(x_min, x_max, 1000)
                y_vals = func_np(x_vals)
                
                # Main plot
                self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func}')
                
                if auto_detect_features:
                    # Find critical points (derivative = 0)
                    try:
                        derivative = sp.diff(func, x)
                        critical_points = sp.solve(derivative, x)
                        
                        # Filter real critical points in range
                        real_criticals = []
                        for cp in critical_points:
                            if cp.is_real and x_min <= float(cp) <= x_max:
                                real_criticals.append(float(cp))
                        
                        # Plot critical points
                        if real_criticals:
                            critical_y = [func_np(cp) for cp in real_criticals]
                            self.ax.plot(real_criticals, critical_y, 'ro', 
                                       markersize=8, label='Critical Points')
                        
                        # Find roots (function = 0)
                        roots = sp.solve(func, x)
                        real_roots = []
                        for root in roots:
                            if root.is_real and x_min <= float(root) <= x_max:
                                real_roots.append(float(root))
                        
                        # Plot roots
                        if real_roots:
                            self.ax.plot(real_roots, [0] * len(real_roots), 'go', 
                                       markersize=8, label='Roots')
                    
                    except Exception as e:
                        # Skip feature detection if it fails
                        pass
                
                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                self.ax.set_xlabel('x')
                self.ax.set_ylabel('f(x)')
                self.ax.set_title(f'Function Explorer: f(x) = {func}')
                
                return True
                
            except Exception as e:
                self.ax.clear()
                self.ax.text(0.5, 0.5, f"Error: {str(e)}", 
                           transform=self.ax.transAxes, ha='center', va='center',
                           fontsize=12, bbox=dict(boxstyle="round", facecolor="lightcoral"))
                self.ax.set_title("Function Explorer - Error")
                return False
        
        def update_function(text):
            """Update function when text changes"""
            nonlocal current_func_str
            current_func_str = text
            plot_function(text, x_min_slider.val, x_max_slider.val)
            self.fig.canvas.draw()
        
        def update_range(val):
            """Update when range changes"""
            plot_function(current_func_str, x_min_slider.val, x_max_slider.val)
            self.fig.canvas.draw()
        
        # Connect events
        textbox.on_submit(update_function)
        x_min_slider.on_changed(update_range)
        x_max_slider.on_changed(update_range)
        
        # Initial plot
        plot_function(current_func_str, x_range[0], x_range[1])
        
        # Add hover tooltips for detected features
        try:
            import mplcursors
            # Add hover to all plotted elements
            for artist in self.ax.lines + self.ax.collections:
                if len(artist.get_xdata()) > 0:  # Only if has data
                    cursor = mplcursors.cursor(artist, hover=True)
                    @cursor.connect("add")
                    def on_add(sel):
                        x_val, y_val = sel.target
                        sel.annotation.set_text(f'x = {x_val:.3f}\ny = {y_val:.3f}')
        except ImportError:
            pass
        
        
        return self.fig
    
    def multi_function_plotter(self, functions: List[str], 
                              x_range: Tuple[float, float] = (-10, 10),
                              colors: Optional[List[str]] = None):
        """
        Plot multiple functions simultaneously
        Args:
            functions: List of function strings
            x_range: X-axis range
            colors: List of colors for each function
        """
        if not functions:
            raise ValueError("At least one function must be provided")
        
        if colors is None:
            colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
        
        self.create_figure()
        self.fig.subplots_adjust(bottom=0.5)
        
        # Create text inputs for each function
        textboxes = []
        for i, func in enumerate(functions):
            y_pos = 0.35 - i * 0.05
            textbox = self.add_textbox(f'f{i+1}(x) = ', func, [0.15, y_pos, 0.4, 0.03])
            textboxes.append(textbox)
        
        # Range controls
        x_min_slider = self.add_slider('x_min', -20, 0, x_range[0], [0.6, 0.35, 0.25, 0.03])
        x_max_slider = self.add_slider('x_max', 0, 20, x_range[1], [0.6, 0.30, 0.25, 0.03])
        
        current_functions = functions.copy()
        
        def plot_all_functions():
            """Plot all current functions"""
            self.ax.clear()
            
            x_vals = np.linspace(x_min_slider.val, x_max_slider.val, 1000)
            
            for i, func_str in enumerate(current_functions):
                if func_str.strip():
                    try:
                        x = sp.Symbol('x')
                        func = sp.sympify(func_str)
                        func_np = sp.lambdify(x, func, 'numpy')
                        
                        y_vals = func_np(x_vals)
                        color = colors[i % len(colors)]
                        line, = self.ax.plot(x_vals, y_vals, color=color, linewidth=2, 
                                   label=f'f{i+1}(x) = {func}')
                        
                        # ADD HOVER HERE
                        try:
                            import mplcursors
                            cursor = mplcursors.cursor(line, hover=True)
                            func_copy = func  # Capture for closure
                            @cursor.connect("add")
                            def on_add(sel, f=func_copy):
                                x_val, y_val = sel.target
                                sel.annotation.set_text(f'f(x) = {f}\nx = {x_val:.3f}\ny = {y_val:.3f}')
                        except ImportError:
                            pass
                    
                    except Exception as e:
                        continue
            
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title('Multi-Function Plotter')
            self.fig.canvas.draw()
        
        def create_update_function(index):
            """Create update function for specific textbox"""
            def update_function(text):
                current_functions[index] = text
                plot_all_functions()
            return update_function
        
        def update_range(val):
            """Update when range changes"""
            plot_all_functions()
        
        # Connect events
        for i, textbox in enumerate(textboxes):
            textbox.on_submit(create_update_function(i))
        
        x_min_slider.on_changed(update_range)
        x_max_slider.on_changed(update_range)
        
        # Initial plot
        plot_all_functions()
        
        return self.fig
    
    def parametric_plotter(self, x_func: str = "cos(t)", y_func: str = "sin(t)",
                          t_range: Tuple[float, float] = (0, 6.28)):
        """
        Plot parametric equations
        Args:
            x_func: X-component function string
            y_func: Y-component function string  
            t_range: Parameter range
        """
        self.create_figure()
        self.fig.subplots_adjust(bottom=0.4)
        
        # Add function inputs
        x_textbox = self.add_textbox('x(t) = ', x_func, [0.15, 0.25, 0.3, 0.04])
        y_textbox = self.add_textbox('y(t) = ', y_func, [0.55, 0.25, 0.3, 0.04])
        
        # Parameter range controls
        t_min_slider = self.add_slider('t_min', -10, 10, t_range[0], [0.15, 0.15, 0.25, 0.03])
        t_max_slider = self.add_slider('t_max', -10, 20, t_range[1], [0.55, 0.15, 0.25, 0.03])
        
        current_x_func = x_func
        current_y_func = y_func
        
        def plot_parametric():
            """Plot the parametric curve"""
            try:
                self.ax.clear()
                
                # Parse functions
                t = sp.Symbol('t')
                x_expr = sp.sympify(current_x_func)
                y_expr = sp.sympify(current_y_func)
                
                # Convert to numpy functions
                x_func_np = sp.lambdify(t, x_expr, 'numpy')
                y_func_np = sp.lambdify(t, y_expr, 'numpy')
                
                # Create parameter values
                t_vals = np.linspace(t_min_slider.val, t_max_slider.val, 1000)
                x_vals = x_func_np(t_vals)
                y_vals = y_func_np(t_vals)
                
                # Plot parametric curve
                self.ax.plot(x_vals, y_vals, 'b-', linewidth=2)
                
                # Mark start and end points
                self.ax.plot(x_vals[0], y_vals[0], 'go', markersize=8, label='Start')
                self.ax.plot(x_vals[-1], y_vals[-1], 'ro', markersize=8, label='End')
                
                # Add direction arrows
                if len(x_vals) > 100:
                    arrow_indices = np.linspace(0, len(x_vals)-1, 10, dtype=int)
                    for i in arrow_indices[:-1]:
                        dx = x_vals[i+50] - x_vals[i]
                        dy = y_vals[i+50] - y_vals[i]
                        self.ax.annotate('', xy=(x_vals[i+25], y_vals[i+25]), 
                                       xytext=(x_vals[i], y_vals[i]),
                                       arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7))
                
                self.ax.grid(True, alpha=0.3)
                self.ax.legend()
                self.ax.set_xlabel('x(t)')
                self.ax.set_ylabel('y(t)')
                self.ax.set_title(f'Parametric Plot: x(t)={x_expr}, y(t)={y_expr}')
                self.ax.axis('equal')
                
            except Exception as e:
                self.ax.clear()
                self.ax.text(0.5, 0.5, f"Error: {str(e)}", 
                           transform=self.ax.transAxes, ha='center', va='center',
                           bbox=dict(boxstyle="round", facecolor="lightcoral"))
                self.ax.set_title("Parametric Plotter - Error")
            
            self.fig.canvas.draw()
        
        def update_x_func(text):
            nonlocal current_x_func
            current_x_func = text
            plot_parametric()
        
        def update_y_func(text):
            nonlocal current_y_func
            current_y_func = text
            plot_parametric()
        
        def update_range(val):
            plot_parametric()
        
        # Connect events
        x_textbox.on_submit(update_x_func)
        y_textbox.on_submit(update_y_func)
        t_min_slider.on_changed(update_range)
        t_max_slider.on_changed(update_range)
        
        # Initial plot
        plot_parametric()
        
        return self.fig
    
    def save_figure(self, filename: str, dpi: int = 300, 
                   bbox_inches: str = 'tight'):
        """
        Save the current figure
        Args:
            filename: Output filename
            dpi: Resolution in dots per inch
            bbox_inches: Bounding box setting
        """
        if self.fig is None:
            raise ValueError("No figure to save. Create a visualization first.")
        
        self.fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
        print(f"Figure saved as {filename}")
    
    def show(self):
        """Display the current figure"""
        if self.fig is not None:
            plt.show()
        else:
            print("No figure to show. Create a visualization first.")
    
    def close(self):
        """Close the current figure"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None