"""OneShotCV - the tailwindcss of computer-vision drawing."""

from . import Draw
from .Draw import (
    add_box,
    add_circle,
    add_keypoints,
    add_line,
    add_mask,
    add_polygon,
    add_text,
    list_colors,
    list_fonts,
)
from .palette import DEFAULT_COLORS, DEFAULT_FONTS, DEFAULT_POSITIONS, DEFAULT_SIZES

__version__ = "0.2.0"

__all__ = [
    "Draw",
    "add_box",
    "add_circle",
    "add_keypoints",
    "add_line",
    "add_mask",
    "add_polygon",
    "add_text",
    "list_colors",
    "list_fonts",
    "DEFAULT_COLORS",
    "DEFAULT_FONTS",
    "DEFAULT_POSITIONS",
    "DEFAULT_SIZES",
    "__version__",
]
