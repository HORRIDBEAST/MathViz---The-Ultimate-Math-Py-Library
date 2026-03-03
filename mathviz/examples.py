"""
Example gallery for MathViz demonstrations
"""

import matplotlib.pyplot as plt
import numpy as np
from .core import MathViz
from .concepts import AlgebraVisualizer, CalculusVisualizer

class ExampleGallery:
    """Gallery of mathematical visualization examples"""
    
    def __init__(self):
        self.examples = {}
        
    def algebra_examples(self):
        """Run algebra visualization examples"""
        print("MathViz Algebra Examples")
        print("=" * 40)
        
        examples = [
            ("Quadratic Function Explorer", self._quadratic_example),
            ("Polynomial Function Explorer", self._polynomial_example),
            ("Linear Transformation", self._linear_transformation_example),
            ("Function Families", self._function_families_example)
        ]
        
        for title, example_func in examples:
            print(f"\n{title}:")
            try:
                example_func()
                input("Press Enter to continue to next example...")
                plt.close('all')  # Close current figures
            except KeyboardInterrupt:
                print("\nExamples interrupted by user.")
                break
            except Exception as e:
                print(f"Error in example: {e}")
    
    def calculus_examples(self):
        """Run calculus visualization examples"""
        print("MathViz Calculus Examples")
        print("=" * 40)
        
        examples = [
            ("Derivative Visualization", self._derivative_example),
            ("Integral Visualization", self._integral_example),
            ("Limits Visualization", self._limits_example),
            ("Series Expansion", self._series_example)
        ]
        
        for title, example_func in examples:
            print(f"\n{title}:")
            try:
                example_func()
                input("Press Enter to continue to next example...")
                plt.close('all')
            except KeyboardInterrupt:
                print("\nExamples interrupted by user.")
                break
            except Exception as e:
                print(f"Error in example: {e}")
    
    def advanced_examples(self):
        """Run advanced visualization examples"""
        print("MathViz Advanced Examples")
        print("=" * 40)
        
        examples = [
            ("Multi-Function Comparison", self._multi_function_example),
            ("Parametric Curves", self._parametric_example),
            ("Function Animation", self._animation_example),
            ("3D Surface Plot", self._surface_example)
        ]
        
        for title, example_func in examples:
            print(f"\n{title}:")
            try:
                example_func()
                input("Press Enter to continue to next example...")
                plt.close('all')
            except KeyboardInterrupt:
                print("\nExamples interrupted by user.")
                break
            except Exception as e:
                print(f"Error in example: {e}")
    
    def _quadratic_example(self):
        """Quadratic function explorer example"""
        print("Explore how changing coefficients affects quadratic functions")
        print("- Adjust sliders to see vertex and roots change")
        print("- Note how 'a' affects opening direction and width")
        
        viz = AlgebraVisualizer()
        fig = viz.quadratic_explorer(
            a_range=(-3, 3),
            b_range=(-5, 5),
            c_range=(-5, 5),
            x_range=(-8, 8),
            y_range=(-10, 15)
        )
        plt.show()
    
    def _polynomial_example(self):
        """Polynomial function explorer example"""
        print("Explore higher degree polynomials")
        print("- See how different coefficients affect the curve shape")
        print("- Observe the relationship between degree and turning points")
        
        viz = AlgebraVisualizer()
        fig = viz.polynomial_explorer(
            degree=4,
            x_range=(-3, 3),
            y_range=(-5, 5)
        )
        plt.show()
    
    def _linear_transformation_example(self):
        """Linear transformation visualization"""
        print("Visualizing linear transformations y = mx + b")
        
        viz = MathViz()
        viz.create_figure()
        
        # Create sliders
        m_slider = viz.add_slider('slope (m)', -3, 3, 1, [0.2, 0.15, 0.3, 0.03])
        b_slider = viz.add_slider('intercept (b)', -5, 5, 0, [0.2, 0.10, 0.3, 0.03])
        
        x = np.linspace(-10, 10, 1000)
        line, = viz.ax.plot(x, x, 'b-', linewidth=2, label='y = mx + b')
        
        viz.ax.set_xlim(-10, 10)
        viz.ax.set_ylim(-10, 10)
        viz.ax.grid(True, alpha=0.3)
        viz.ax.legend()
        viz.ax.set_title('Linear Transformation Explorer')
        
        def update(val):
            m = m_slider.val
            b = b_slider.val
            y = m * x + b
            line.set_ydata(y)
            viz.ax.set_title(f'y = {m:.2f}x + {b:.2f}')
            viz.fig.canvas.draw()
        
        m_slider.on_changed(update)
        b_slider.on_changed(update)
        update(0)
        
        plt.show()
    
    def _function_families_example(self):
        """Function families comparison"""
        print("Compare different function families")
        
        functions = [
            "x**2",      # Quadratic
            "x**3",      # Cubic
            "sin(x)",    # Trigonometric
            "exp(x)",    # Exponential
            "log(x)",    # Logarithmic
        ]
        
        viz = MathViz()
        fig = viz.multi_function_plotter(
            functions=functions,
            x_range=(-5, 5)
        )
        plt.show()
    
    def _derivative_example(self):
        """Derivative visualization example"""
        print("Explore derivatives and tangent lines")
        print("- See how the derivative represents the slope")
        print("- Move the slider to see tangent lines at different points")
        
        viz = CalculusVisualizer()
        fig = viz.derivative_visualizer(
            func_str="x**3 - 3*x**2 + 2*x",
            x_range=(-2, 4),
            show_function_input=True
        )
        plt.show()
    
    def _integral_example(self):
        """Integral visualization example"""
        print("Visualize definite integrals as area under curves")
        print("- Adjust integration bounds with sliders")
        print("- See how the area changes with different bounds")
        
        viz = CalculusVisualizer()
        fig = viz.integral_visualizer(
            func_str="x**2 - 4",
            x_range=(-3, 3),
            integration_range=(-2, 2)
        )
        plt.show()
    
    def _limits_example(self):
        """Limits visualization example"""
        print("Exploring limits and continuity")
        
        viz = MathViz()
        viz.create_figure()
        
        # Function with a discontinuity
        x = np.linspace(-5, 5, 1000)
        
        # Remove point at x=0 to show discontinuity
        x_discontinuous = x[x != 0]
        y_discontinuous = np.sin(x_discontinuous) / x_discontinuous
        
        viz.ax.plot(x_discontinuous, y_discontinuous, 'b-', linewidth=2, label='sin(x)/x')
        viz.ax.plot(0, 1, 'ro', markersize=8, label='lim(x→0) sin(x)/x = 1')
        
        viz.ax.set_xlim(-5, 5)
        viz.ax.set_ylim(-0.5, 1.5)
        viz.ax.grid(True, alpha=0.3)
        viz.ax.legend()
        viz.ax.set_title('Limit of sin(x)/x as x approaches 0')
        
        plt.show()
    
    def _series_example(self):
        """Series expansion visualization"""
        print("Taylor series approximations")
        
        viz = MathViz()
        viz.create_figure()
        
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        
        # sin(x) and its Taylor series approximations
        sin_exact = np.sin(x)
        
        # Taylor series terms
        sin_1 = x
        sin_3 = x - x**3/6
        sin_5 = x - x**3/6 + x**5/120
        sin_7 = x - x**3/6 + x**5/120 - x**7/5040
        
        viz.ax.plot(x, sin_exact, 'k-', linewidth=3, label='sin(x) exact')
        viz.ax.plot(x, sin_1, 'r--', linewidth=2, label='1st order: x')
        viz.ax.plot(x, sin_3, 'g--', linewidth=2, label='3rd order')
        viz.ax.plot(x, sin_5, 'b--', linewidth=2, label='5th order')
        viz.ax.plot(x, sin_7, 'm--', linewidth=2, label='7th order')
        
        viz.ax.set_xlim(-2*np.pi, 2*np.pi)
        viz.ax.set_ylim(-3, 3)
        viz.ax.grid(True, alpha=0.3)
        viz.ax.legend()
        viz.ax.set_title('Taylor Series Approximation of sin(x)')
        
        plt.show()
    
    def _multi_function_example(self):
        """Multi-function comparison example"""
        print("Compare multiple functions simultaneously")
        
        functions = ["x**2", "2**x", "x**3", "sin(2*x)"]
        
        viz = MathViz()
        fig = viz.multi_function_plotter(
            functions=functions,
            x_range=(-3, 3)
        )
        plt.show()
    
    def _parametric_example(self):
        """Parametric curves example"""
        print("Explore parametric equations")
        print("- Try different parametric equations")
        print("- Observe how parameter changes affect the curve")
        
        viz = MathViz()
        
        # Show multiple parametric examples
        examples = [
            ("Circle", "cos(t)", "sin(t)", (0, 2*np.pi)),
            ("Ellipse", "2*cos(t)", "sin(t)", (0, 2*np.pi)),
            ("Lissajous", "sin(3*t)", "sin(2*t)", (0, 2*np.pi)),
            ("Spiral", "t*cos(t)", "t*sin(t)", (0, 4*np.pi))
        ]
        
        for name, x_func, y_func, t_range in examples:
            print(f"\nShowing {name}: x(t)={x_func}, y(t)={y_func}")
            fig = viz.parametric_plotter(x_func, y_func, t_range)
            plt.show()
            input("Press Enter for next parametric example...")
            plt.close('all')
    
    def _animation_example(self):
        """Function animation example"""
        print("Animated function transformations")
        
        viz = MathViz()
        viz.create_figure()
        
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        
        # Create multiple sine waves with different phases
        for phase in np.linspace(0, 2*np.pi, 8):
            y = np.sin(x + phase)
            alpha = 0.3 + 0.7 * (phase / (2*np.pi))
            viz.ax.plot(x, y, alpha=alpha, color='blue')
        
        viz.ax.set_xlim(-2*np.pi, 2*np.pi)
        viz.ax.set_ylim(-1.5, 1.5)
        viz.ax.grid(True, alpha=0.3)
        viz.ax.set_title('Sine Wave Phase Animation (Static View)')
        
        plt.show()
    
    def _surface_example(self):
        """3D surface plot example"""
        print("3D surface visualization")
        
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create meshgrid
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        
        # 3D function
        Z = np.sin(np.sqrt(X**2 + Y**2))
        
        # Surface plot
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D Surface: z = sin(√(x² + y²))')
        
        fig.colorbar(surf)
        plt.show()
    
    def educational_demos(self):
        """Educational demonstration examples"""
        print("Educational Mathematics Demonstrations")
        print("=" * 50)
        
        demos = [
            ("Quadratic Formula Visualization", self._quadratic_formula_demo),
            ("Chain Rule Demonstration", self._chain_rule_demo),
            ("Fundamental Theorem of Calculus", self._ftc_demo),
            ("Trigonometric Identities", self._trig_identities_demo)
        ]
        
        for title, demo_func in demos:
            print(f"\n{title}:")
            try:
                demo_func()
                input("Press Enter to continue to next demo...")
                plt.close('all')
            except KeyboardInterrupt:
                print("\nDemos interrupted by user.")
                break
            except Exception as e:
                print(f"Error in demo: {e}")
    
    def _quadratic_formula_demo(self):
        """Demonstrate the quadratic formula graphically"""
        print("See how discriminant affects roots")
        
        viz = AlgebraVisualizer()
        fig = viz.quadratic_explorer(
            a_range=(0.1, 2),  # Keep a positive
            b_range=(-4, 4),
            c_range=(-3, 3),
            x_range=(-5, 5),
            y_range=(-5, 5)
        )
        plt.show()
    
    def _chain_rule_demo(self):
        """Demonstrate the chain rule"""
        print("Chain rule: d/dx[f(g(x))] = f'(g(x)) * g'(x)")
        
        viz = CalculusVisualizer()
        fig = viz.derivative_visualizer(
            func_str="sin(x**2)",  # Composite function
            x_range=(-3, 3)
        )
        plt.show()
    
    def _ftc_demo(self):
        """Fundamental Theorem of Calculus demonstration"""
        print("FTC: The derivative of an integral gives back the original function")
        
        viz = CalculusVisualizer()
        fig = viz.integral_visualizer(
            func_str="x**2",
            x_range=(-3, 3),
            integration_range=(0, 2)
        )
        plt.show()
    
    def _trig_identities_demo(self):
        """Trigonometric identities visualization"""
        print("Visualizing trigonometric identities")
        
        functions = [
            "sin(x)",
            "cos(x)", 
            "sin(x)**2 + cos(x)**2",  # Should equal 1
            "sin(2*x)",
            "2*sin(x)*cos(x)"         # Should equal sin(2x)
        ]
        
        viz = MathViz()
        fig = viz.multi_function_plotter(
            functions=functions,
            x_range=(0, 2*np.pi)
        )
        plt.show()
    
    def run_all_examples(self):
        """Run all example categories"""
        categories = [
            ("Algebra Examples", self.algebra_examples),
            ("Calculus Examples", self.calculus_examples),
            ("Advanced Examples", self.advanced_examples),
            ("Educational Demos", self.educational_demos)
        ]
        
        print("MathViz Complete Example Gallery")
        print("=" * 50)
        
        for category_name, category_func in categories:
            print(f"\nStarting {category_name}...")
            try:
                category_func()
                print(f"Completed {category_name}")
            except KeyboardInterrupt:
                print(f"\n{category_name} interrupted by user.")
                break
            except Exception as e:
                print(f"Error in {category_name}: {e}")
        
        print("\nExample gallery complete!")
    
    def get_example_list(self):
        """Get a list of all available examples"""
        examples = {
            'algebra': [
                'quadratic_explorer',
                'polynomial_explorer', 
                'linear_transformation',
                'function_families'
            ],
            'calculus': [
                'derivative_visualization',
                'integral_visualization',
                'limits_exploration',
                'series_expansion'
            ],
            'advanced': [
                'multi_function_comparison',
                'parametric_curves',
                'function_animation',
                'surface_plots'
            ],
            'educational': [
                'quadratic_formula',
                'chain_rule',
                'fundamental_theorem_calculus',
                'trigonometric_identities'
            ]
        }
        return examples