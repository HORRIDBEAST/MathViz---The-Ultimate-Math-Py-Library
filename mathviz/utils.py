import matplotlib.pyplot as plt
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
    """
    buf = BytesIO()
    fig.savefig(buf, format=format, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/{format};base64,{img_str}'