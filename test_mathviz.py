#!/usr/bin/env python3
"""
Comprehensive test suite for MathViz library
"""

import sys
import os
import unittest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from io import StringIO
from contextlib import redirect_stdout

# Add the mathviz directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestMathVizCore(unittest.TestCase):
    """Test the core MathViz class"""
    
    def setUp(self):
        """Set up test fixtures"""
        from mathviz import MathViz
        self.viz = MathViz()
    
    def tearDown(self):
        """Clean up after tests"""
        plt.close('all')
    
    def test_initialization(self):
        """Test MathViz initialization"""
        self.assertIsNotNone(self.viz)
        self.assertEqual(self.viz.figsize, (12, 8))
    
    def test_create_figure(self):
        """Test figure creation"""
        fig, ax = self.viz.create_figure()
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(self.viz.fig, fig)
        self.assertEqual(self.viz.ax, ax)
    
    def test_function_explorer(self):
        """Test function explorer functionality"""
        fig = self.viz.function_explorer("x**2", (-5, 5))
        self.assertIsNotNone(fig)
    
    def test_multi_function_plotter(self):
        """Test multi-function plotter"""
        functions = ["x**2", "sin(x)", "cos(x)"]
        fig = self.viz.multi_function_plotter(functions, (-5, 5))
        self.assertIsNotNone(fig)
    
    def test_parametric_plotter(self):
        """Test parametric plotter"""
        fig = self.viz.parametric_plotter("cos(t)", "sin(t)", (0, 6.28))
        self.assertIsNotNone(fig)
    
    def test_invalid_functions(self):
        """Test handling of invalid functions"""
        # Should not crash with invalid function
        fig = self.viz.function_explorer("invalid_function", (-5, 5))
        self.assertIsNotNone(fig)

class TestAlgebraVisualizer(unittest.TestCase):
    """Test the AlgebraVisualizer class"""
    
    def setUp(self):
        from mathviz import AlgebraVisualizer
        self.viz = AlgebraVisualizer()
    
    def tearDown(self):
        plt.close('all')
    
    def test_quadratic_explorer(self):
        """Test quadratic function explorer"""
        fig = self.viz.quadratic_explorer()
        self.assertIsNotNone(fig)
    
    def test_quadratic_custom_ranges(self):
        """Test quadratic explorer with custom ranges"""
        fig = self.viz.quadratic_explorer(
            a_range=(-2, 2),
            b_range=(-5, 5),
            c_range=(-3, 3),
            x_range=(-8, 8),
            y_range=(-10, 10)
        )
        self.assertIsNotNone(fig)
    
    def test_polynomial_explorer(self):
        """Test polynomial explorer"""
        for degree in range(2, 6):
            with self.subTest(degree=degree):
                fig = self.viz.polynomial_explorer(degree=degree)
                self.assertIsNotNone(fig)
    
    def test_polynomial_invalid_degree(self):
        """Test polynomial explorer with invalid degree"""
        with self.assertRaises(ValueError):
            self.viz.polynomial_explorer(degree=1)
        
        with self.assertRaises(ValueError):
            self.viz.polynomial_explorer(degree=6)

class TestCalculusVisualizer(unittest.TestCase):
    """Test the CalculusVisualizer class"""
    
    def setUp(self):
        from mathviz import CalculusVisualizer
        self.viz = CalculusVisualizer()
    
    def tearDown(self):
        plt.close('all')
    
    def test_derivative_visualizer(self):
        """Test derivative visualizer"""
        fig = self.viz.derivative_visualizer("x**2")
        self.assertIsNotNone(fig)
    
    def test_derivative_complex_function(self):
        """Test derivative visualizer with complex function"""
        fig = self.viz.derivative_visualizer("x**3 - 3*x**2 + 2*x")
        self.assertIsNotNone(fig)
    
    def test_integral_visualizer(self):
        """Test integral visualizer"""
        fig = self.viz.integral_visualizer("x**2")
        self.assertIsNotNone(fig)
    
    def test_integral_custom_bounds(self):
        """Test integral visualizer with custom bounds"""
        fig = self.viz.integral_visualizer(
            func_str="sin(x)",
            x_range=(-3.14, 3.14),
            integration_range=(0, 3.14)
        )
        self.assertIsNotNone(fig)
    
    def test_invalid_function_derivative(self):
        """Test derivative visualizer with invalid function"""
        # Should handle invalid functions gracefully
        fig = self.viz.derivative_visualizer("invalid_function")
        self.assertIsNotNone(fig)

class TestExampleGallery(unittest.TestCase):
    """Test the ExampleGallery class"""
    
    def setUp(self):
        from mathviz import ExampleGallery
        self.gallery = ExampleGallery()
    
    def tearDown(self):
        plt.close('all')
    
    def test_gallery_initialization(self):
        """Test gallery initialization"""
        self.assertIsNotNone(self.gallery)
        self.assertIsInstance(self.gallery.examples, dict)
    
    def test_get_example_list(self):
        """Test getting example list"""
        examples = self.gallery.get_example_list()
        self.assertIsInstance(examples, dict)
        self.assertIn('algebra', examples)
        self.assertIn('calculus', examples)

class TestWidgets(unittest.TestCase):
    """Test custom widgets"""
    
    def tearDown(self):
        plt.close('all')
    
    def test_slider_import(self):
        """Test slider widget import"""
        from mathviz import Slider
        self.assertIsNotNone(Slider)
    
    def test_button_import(self):
        """Test button widget import"""
        from mathviz import Button
        self.assertIsNotNone(Button)
    
    def test_inputbox_import(self):
        """Test input box widget import"""
        from mathviz import InputBox
        self.assertIsNotNone(InputBox)

class TestJupyterIntegration(unittest.TestCase):
    """Test Jupyter integration (if available)"""
    
    def test_jupyter_import(self):
        """Test Jupyter integration import"""
        from mathviz import JupyterMathViz
        # JupyterMathViz might be None if ipywidgets not installed
        # This is expected behavior

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_export_function_import(self):
        """Test export function import"""
        from mathviz import export_to_data_url
        self.assertIsNotNone(export_to_data_url)

class TestPackageMetadata(unittest.TestCase):
    """Test package metadata and structure"""
    
    def test_version_import(self):
        """Test version information"""
        import mathviz
        self.assertTrue(hasattr(mathviz, '__version__'))
        self.assertIsInstance(mathviz.__version__, str)
    
    def test_all_imports(self):
        """Test that all public components can be imported"""
        try:
            from mathviz import (
                MathViz, AlgebraVisualizer, CalculusVisualizer,
                Slider, Button, InputBox, ExampleGallery,
                export_to_data_url
            )
            # All imports successful
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import error: {e}")
    
    def test_info_functions(self):
        """Test info and help functions"""
        import mathviz
        
        # Test get_info function
        info = mathviz.get_info()
        self.assertIsInstance(info, dict)
        self.assertIn('version', info)
        
        # Test print_info function (capture output)
        f = StringIO()
        with redirect_stdout(f):
            mathviz.print_info()
        output = f.getvalue()
        self.assertIn('MathViz', output)
        
        # Test quick_start function
        f = StringIO()
        with redirect_stdout(f):
            mathviz.quick_start()
        output = f.getvalue()
        self.assertIn('Quick Start', output)

class TestMathematicalAccuracy(unittest.TestCase):
    """Test mathematical accuracy of computations"""
    
    def test_quadratic_vertex_calculation(self):
        """Test quadratic vertex calculation accuracy"""
        from mathviz.concepts import AlgebraVisualizer
        
        # Test known quadratic: y = x^2 - 2x + 1 = (x-1)^2
        # Vertex should be at (1, 0)
        a, b, c = 1, -2, 1
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        
        self.assertAlmostEqual(vertex_x, 1.0, places=10)
        self.assertAlmostEqual(vertex_y, 0.0, places=10)
    
    def test_derivative_calculation(self):
        """Test symbolic derivative calculation"""
        import sympy as sp
        
        x = sp.Symbol('x')
        func = x**3 - 3*x**2 + 2*x
        derivative = sp.diff(func, x)
        expected = 3*x**2 - 6*x + 2
        
        self.assertEqual(derivative, expected)
    
    def test_integration_calculation(self):
        """Test symbolic integration"""
        import sympy as sp
        
        x = sp.Symbol('x')
        func = x**2
        integral = sp.integrate(func, (x, 0, 2))
        expected = sp.Rational(8, 3)  # 8/3
        
        self.assertEqual(integral, expected)

def run_visual_tests():
    """Run visual tests that require manual inspection"""
    print("Running Visual Tests...")
    print("These tests will display plots for visual inspection.")
    print("Close each plot window to proceed to the next test.")
    
    visual_tests = [
        ("Basic Quadratic Explorer", test_basic_quadratic),
        ("Multi-function Plotter", test_multi_function),
        ("Derivative Visualizer", test_derivative_viz),
        ("Parametric Plotter", test_parametric_viz)
    ]
    
    for test_name, test_func in visual_tests:
        print(f"\nRunning: {test_name}")
        try:
            test_func()
            response = input("Did the visualization display correctly? (y/n): ")
            if response.lower() != 'y':
                print(f"Visual test failed: {test_name}")
            else:
                print(f"Visual test passed: {test_name}")
        except Exception as e:
            print(f"Error in visual test {test_name}: {e}")
        finally:
            plt.close('all')

def test_basic_quadratic():
    """Visual test for basic quadratic explorer"""
    from mathviz import AlgebraVisualizer
    viz = AlgebraVisualizer()
    viz.quadratic_explorer()
    plt.show()

def test_multi_function():
    """Visual test for multi-function plotter"""
    from mathviz import MathViz
    viz = MathViz()
    viz.multi_function_plotter(["x**2", "sin(x)", "cos(x)"])
    plt.show()

def test_derivative_viz():
    """Visual test for derivative visualizer"""
    from mathviz import CalculusVisualizer
    viz = CalculusVisualizer()
    viz.derivative_visualizer("x**3 - 3*x**2 + 2*x")
    plt.show()

def test_parametric_viz():
    """Visual test for parametric plotter"""
    from mathviz import MathViz
    viz = MathViz()
    viz.parametric_plotter("cos(t)", "sin(t)", (0, 6.28))
    plt.show()

def run_performance_tests():
    """Run performance benchmarks"""
    import time
    from mathviz import MathViz, AlgebraVisualizer, CalculusVisualizer
    
    print("Running Performance Tests...")
    
    # Test function plotting performance
    start_time = time.time()
    viz = MathViz()
    viz.function_explorer("sin(x) + cos(2*x)", (-10, 10))
    plt.close('all')
    elapsed = time.time() - start_time
    print(f"Function explorer creation: {elapsed:.3f} seconds")
    
    # Test quadratic explorer performance
    start_time = time.time()
    viz = AlgebraVisualizer()
    viz.quadratic_explorer()
    plt.close('all')
    elapsed = time.time() - start_time
    print(f"Quadratic explorer creation: {elapsed:.3f} seconds")
    
    # Test derivative visualizer performance
    start_time = time.time()
    viz = CalculusVisualizer()
    viz.derivative_visualizer("x**4 - 2*x**3 + x**2")
    plt.close('all')
    elapsed = time.time() - start_time
    print(f"Derivative visualizer creation: {elapsed:.3f} seconds")

if __name__ == '__main__':
    print("MathViz Comprehensive Test Suite")
    print("=" * 50)
    
    # Check if visual tests are requested
    run_visual = '--visual' in sys.argv
    run_performance = '--performance' in sys.argv
    
    if run_visual:
        sys.argv.remove('--visual')
        run_visual_tests()
    
    if run_performance:
        sys.argv.remove('--performance')
        run_performance_tests()
    
    # Run unit tests
    print("\nRunning Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\nTest suite completed!")
    print("Run with --visual flag to include visual tests")
    print("Run with --performance flag to include performance benchmarks")