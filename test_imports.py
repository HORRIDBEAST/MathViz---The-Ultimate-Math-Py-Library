from mathviz import AlgebraVisualizer
import matplotlib.pyplot as plt

viz = AlgebraVisualizer()
fig = viz.quadratic_explorer()

print("\nHover Test Instructions:")
print("1. Move sliders to create a parabola with:")
print("   - a = 1 (default)")
print("   - b = -2")
print("   - c = -3")
print("2. You should see:")
print("   - RED dot (vertex)")
print("   - GREEN dots (2 roots)")
print("3. HOVER your mouse over:")
print("   - RED dot → should show 'Vertex x=... y=...'")
print("   - GREEN dots → should show 'Root x=...'")
print("\nIf tooltips DON'T appear:")
print("- Check that mplcursors is installed: pip install mplcursors")
print("- Restart your Python/Jupyter session")

plt.show()