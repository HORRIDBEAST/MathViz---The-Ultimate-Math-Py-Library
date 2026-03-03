#!/usr/bin/env python3
"""
Enhanced interactive demo for MathViz library with user input capabilities
"""

import matplotlib.pyplot as plt
import numpy as np
from mathviz import AlgebraVisualizer, CalculusVisualizer, MathViz
from mathviz.examples import ExampleGallery

def get_user_input(prompt, default=None, input_type=str):
    """Get user input with default value"""
    if default is not None:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        if not user_input:
            return default
    else:
        user_input = input(f"{prompt}: ").strip()
    
    try:
        if input_type == float:
            return float(user_input)
        elif input_type == int:
            return int(user_input)
        else:
            return user_input
    except ValueError:
        print(f"Invalid input, using default: {default}")
        return default if default is not None else ""

def demo_custom_quadratic():
    """Demo quadratic explorer with user-defined ranges"""
    print("\n🔢 Custom Quadratic Function Explorer")
    print("Customize the parameter ranges for your quadratic function:")
    
    # Get user preferences
    a_min = get_user_input("Minimum value for 'a'", -5, float)
    a_max = get_user_input("Maximum value for 'a'", 5, float)
    b_min = get_user_input("Minimum value for 'b'", -10, float)
    b_max = get_user_input("Maximum value for 'b'", 10, float)
    c_min = get_user_input("Minimum value for 'c'", -10, float)
    c_max = get_user_input("Maximum value for 'c'", 10, float)
    
    x_min = get_user_input("X-axis minimum", -10, float)
    x_max = get_user_input("X-axis maximum", 10, float)
    y_min = get_user_input("Y-axis minimum", -25, float)
    y_max = get_user_input("Y-axis maximum", 25, float)
    
    print(f"\nCreating quadratic explorer with:")
    print(f"  a ∈ [{a_min}, {a_max}], b ∈ [{b_min}, {b_max}], c ∈ [{c_min}, {c_max}]")
    print(f"  Viewing window: x ∈ [{x_min}, {x_max}], y ∈ [{y_min}, {y_max}]")
    
    viz = AlgebraVisualizer()
    fig = viz.quadratic_explorer(
        a_range=(a_min, a_max),
        b_range=(b_min, b_max), 
        c_range=(c_min, c_max),
        x_range=(x_min, x_max),
        y_range=(y_min, y_max)
    )
    plt.show()

def demo_polynomial_explorer():
    """Demo polynomial explorer with user-chosen degree"""
    print("\n📊 Custom Polynomial Explorer")
    
    degree = get_user_input("Polynomial degree (2-5)", 3, int)
    if degree < 2 or degree > 5:
        print("Using default degree 3")
        degree = 3
    
    x_min = get_user_input("X-axis minimum", -5, float)
    x_max = get_user_input("X-axis maximum", 5, float)
    y_min = get_user_input("Y-axis minimum", -10, float)
    y_max = get_user_input("Y-axis maximum", 10, float)
    
    print(f"\nCreating degree-{degree} polynomial explorer")
    print("Use the sliders to adjust coefficients!")
    
    viz = AlgebraVisualizer()
    fig = viz.polynomial_explorer(
        degree=degree,
        x_range=(x_min, x_max),
        y_range=(y_min, y_max)
    )
    plt.show()

def demo_custom_derivative():
    """Demo derivative visualizer with user function"""
    print("\n📈 Custom Derivative Visualizer")
    
    func = get_user_input("Enter function to visualize", "x**3 - 3*x**2 + 2*x")
    x_min = get_user_input("X-axis minimum", -3, float)
    x_max = get_user_input("X-axis maximum", 5, float)
    
    print(f"\nVisualizing f(x) = {func}")
    print("You can change the function using the text input box!")
    print("Use the slider to explore tangent lines.")
    
    viz = CalculusVisualizer()
    fig = viz.derivative_visualizer(
        func_str=func,
        x_range=(x_min, x_max),
        show_function_input=True
    )
    plt.show()

def demo_integral_visualizer():
    """Demo integral visualizer"""
    print("\n∫ Integral Visualizer")
    
    func = get_user_input("Enter function to integrate", "x**2")
    x_min = get_user_input("X-axis minimum", -2, float)
    x_max = get_user_input("X-axis maximum", 2, float)
    a = get_user_input("Integration lower bound", -1, float)
    b = get_user_input("Integration upper bound", 1, float)
    
    print(f"\nVisualizing ∫[{a}, {b}] {func} dx")
    print("You can adjust the integration bounds with sliders!")
    
    viz = CalculusVisualizer()
    fig = viz.integral_visualizer(
        func_str=func,
        x_range=(x_min, x_max),
        integration_range=(a, b)
    )
    plt.show()

def demo_multi_function_plotter():
    """Demo multi-function plotter"""
    print("\n📊 Multi-Function Plotter")
    print("Enter up to 4 functions to plot simultaneously:")
    
    functions = []
    for i in range(4):
        func = get_user_input(f"Function {i+1} (or press Enter to skip)", "")
        if func:
            functions.append(func)
        else:
            break
    
    if not functions:
        functions = ["x**2", "sin(x)", "cos(x)"]  # defaults
        print("Using default functions: x², sin(x), cos(x)")
    
    x_min = get_user_input("X-axis minimum", -10, float)
    x_max = get_user_input("X-axis maximum", 10, float)
    
    print(f"\nPlotting {len(functions)} functions")
    print("You can modify functions in real-time using the text boxes!")
    
    viz = MathViz()
    fig = viz.multi_function_plotter(
        functions=functions,
        x_range=(x_min, x_max)
    )
    plt.show()

def demo_parametric_plotter():
    """Demo parametric plotter"""
    print("\n🌀 Parametric Plotter")
    
    x_func = get_user_input("X-component function x(t)", "cos(t)")
    y_func = get_user_input("Y-component function y(t)", "sin(t)")
    t_min = get_user_input("Parameter minimum", 0, float)
    t_max = get_user_input("Parameter maximum", 2*np.pi, float)
    
    print(f"\nPlotting parametric curve:")
    print(f"  x(t) = {x_func}")
    print(f"  y(t) = {y_func}")
    print(f"  t ∈ [{t_min}, {t_max}]")
    print("You can modify the equations and parameter range!")
    
    viz = MathViz()
    fig = viz.parametric_plotter(
        x_func=x_func,
        y_func=y_func,
        t_range=(t_min, t_max)
    )
    plt.show()

def demo_function_explorer():
    """Demo general function explorer"""
    print("\n🔍 General Function Explorer")
    
    func = get_user_input("Enter function to explore", "x**2")
    x_min = get_user_input("X-axis minimum", -5, float)
    x_max = get_user_input("X-axis maximum", 5, float)
    
    print(f"\nExploring f(x) = {func}")
    print("Features:")
    print("- Change function in real-time")
    print("- Adjust viewing window")
    print("- Automatic critical point detection")
    
    viz = MathViz()
    fig = viz.function_explorer(
        initial_func=func,
        x_range=(x_min, x_max)
    )
    plt.show()

def demo_examples():
    """Run the example gallery"""
    print("\n🎨 Example Gallery")
    gallery = ExampleGallery()
    gallery.algebra_examples()
    gallery.calculus_examples()

def main():
    """Run interactive demos with user input"""
    print("🧮 MathViz Enhanced Interactive Demo")
    print("=" * 50)
    print("This demo showcases user input capabilities!")
    
    menu_options = {
        '1': ("Custom Quadratic Explorer", demo_custom_quadratic),
        '2': ("Polynomial Explorer", demo_polynomial_explorer),
        '3': ("Custom Derivative Visualizer", demo_custom_derivative),
        '4': ("Integral Visualizer", demo_integral_visualizer),
        '5': ("Multi-Function Plotter", demo_multi_function_plotter),
        '6': ("Parametric Plotter", demo_parametric_plotter),
        '7': ("Function Explorer", demo_function_explorer),
        '8': ("Example Gallery", demo_examples),
        '9': ("Exit", None)
    }
    
    while True:
        print("\n" + "="*50)
        print("Choose a demo:")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice in menu_options:
            description, func = menu_options[choice]
            if func is None:  # Exit
                print("👋 Thanks for using MathViz Enhanced Demo!")
                break
            else:
                print(f"\n🚀 Starting: {description}")
                try:
                    func()
                except KeyboardInterrupt:
                    print("\n⏹ Demo interrupted by user")
                except Exception as e:
                    print(f"\n❌ Error in demo: {e}")
                
                input("\nPress Enter to return to menu...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()