import matplotlib.pyplot as plt
import matplotlib.figure
import base64
from io import BytesIO

def export_to_data_url(fig: plt.Figure, format: str = 'png'):
    """
    Export figure as a data URL for browser-based environments
    Args:
        fig: Matplotlib figure object
        format: Image format ('png' or 'jpg')
    Returns:
        str: Data URL containing the image
    Raises:
        TypeError: If fig is not a matplotlib Figure object
    """
    if not isinstance(fig, matplotlib.figure.Figure):
        raise TypeError(
            f"Expected a matplotlib Figure, got {type(fig).__name__}. "
            "Pass the return value of a MathViz visualizer method, e.g. viz.quadratic_explorer()."
        )
    buf = BytesIO()
    fig.savefig(buf, format=format, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/{format};base64,{img_str}'