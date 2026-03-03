from matplotlib.widgets import Slider as MPLSlider, Button as MPLButton, TextBox
from typing import Callable, Any

class Slider:
    """Enhanced slider widget"""
    def __init__(self, ax, label: str, valmin: float, valmax: float,
                 valinit: float = None, callback: Callable = None):
        init_val = valinit if valinit is not None else valmin
        self.slider = MPLSlider(ax, label, valmin, valmax, valinit=init_val)
        if callback:
            self.slider.on_changed(callback)

    @property
    def val(self):
        return self.slider.val

class Button:
    """Enhanced button widget"""
    def __init__(self, ax, label: str, callback: Callable = None):
        self.button = MPLButton(ax, label)
        if callback:
            self.button.on_clicked(callback)

class InputBox:
    """Text input widget"""
    def __init__(self, ax, label: str, initial: str = "", callback: Callable = None):
        self.textbox = TextBox(ax, label, initial=initial)
        if callback:
            self.textbox.on_submit(callback)

    @property
    def text(self):
        return self.textbox.text