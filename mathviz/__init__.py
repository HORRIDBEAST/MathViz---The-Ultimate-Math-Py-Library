"""
MathViz - Interactive Mathematical Visualization Library

A Python library for creating interactive mathematical visualizations
with real-time parameter manipulation and educational features.
"""

__version__ = "0.1.0"
__author__ = "MathViz Contributors"
__email__ = "mathviz@example.com"

# Core imports
from .core import MathViz

# Specialized visualizers
from .concepts import AlgebraVisualizer, CalculusVisualizer

# Widget components
from .widgets import Slider, Button, InputBox

# Utility functions
from .utils import export_to_data_url

# Examples and gallery
from .examples import ExampleGallery

# Optional Jupyter integration
try:
    from .jupyter_integration import JupyterMathViz, JUPYTER_AVAILABLE
except ImportError:
    JupyterMathViz = None
    JUPYTER_AVAILABLE = False

# Jupyter-native widgets (ipywidgets-based, safe for notebook text input)
try:
    from .jupyter_simple import JupyterSimpleMathViz
except ImportError:
    JupyterSimpleMathViz = None

__all__ = [
    # Core classes
    'MathViz',
    'AlgebraVisualizer', 
    'CalculusVisualizer',
    
    # Widget components
    'Slider',
    'Button', 
    'InputBox',
    
    # Utilities
    'export_to_data_url',
    
    # Examples
    'ExampleGallery',
    
    # Jupyter (may be None if ipywidgets not installed)
    'JupyterMathViz',
    'JupyterSimpleMathViz',
    
    # Metadata
    '__version__',
    '__author__',
    '__email__',
]

# Configuration
import matplotlib
matplotlib.rcParams['figure.max_open_warning'] = 50  # Allow more figures

# Display library information
def get_info():
    """Get library information"""
    info = {
        'version': __version__,
        'author': __author__,
        'description': __doc__.strip(),
        'jupyter_available': JUPYTER_AVAILABLE,
    }
    return info

def print_info():
    """Print library information"""
    info = get_info()
    print(f"MathViz v{info['version']}")
    print(f"Author: {info['author']}")
    print(f"Jupyter Support: {'Available' if info['jupyter_available'] else 'Not Available (install ipywidgets)'}")
    print(f"\n{info['description']}")
    
# Convenience function for quick start
def quick_start():
    """Display quick start guide"""
    print("""
MathViz Quick Start Guide:

1. Quadratic Explorer:
   from mathviz import AlgebraVisualizer
   viz = AlgebraVisualizer()
   viz.quadratic_explorer()
   
2. Function and Derivative:
   from mathviz import CalculusVisualizer  
   viz = CalculusVisualizer()
   viz.derivative_visualizer("x**3 - 3*x**2 + 2*x")
   
3. Multi-function Plotter:
   from mathviz import MathViz
   viz = MathViz()
   viz.multi_function_plotter(["x**2", "sin(x)", "cos(x)"])
   
4. Example Gallery:
   from mathviz import ExampleGallery
   gallery = ExampleGallery()
   gallery.algebra_examples()
   
5. Jupyter Integration — slider-only (if ipywidgets installed):
   from mathviz import JupyterMathViz
   if JupyterMathViz:
       viz = JupyterMathViz()
       viz.interactive_quadratic()

6. Jupyter Integration — with text input (recommended for notebooks):
   from mathviz import JupyterSimpleMathViz
   if JupyterSimpleMathViz:
       viz = JupyterSimpleMathViz()
       viz.interactive_function_plotter()   # type sin(x), x**3, etc.
       viz.interactive_derivative()
       viz.interactive_integral()

For more examples, check the notebooks/ directory!
""")