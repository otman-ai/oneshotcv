"""Internal helpers shared by the drawing functions."""

import os
from typing import Sequence, Union

from .palette import DEFAULT_COLORS, DEFAULT_FONTS

ColorLike = Union[str, Sequence[int]]


def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    bbox = font.getmask(text_string).getbbox()
    if bbox is None:  # empty string / whitespace only
        return (0, ascent + descent)

    text_width = bbox[2]
    text_height = bbox[3] + descent

    return (text_width, text_height)


def hex_to_rgb(value: str) -> tuple:
    """Convert ``#rgb`` / ``#rrggbb`` to an ``(r, g, b)`` tuple."""
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        raise ValueError(f'"{value}" is not a valid hex colour')
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f'"{value}" is not a valid hex colour') from exc


def resolve_color(color: ColorLike) -> tuple:
    """Return an ``(r, g, b)`` tuple for a palette name, hex string or triplet."""
    if isinstance(color, str):
        if color.startswith("#"):
            return hex_to_rgb(color)
        if color in DEFAULT_COLORS:
            return DEFAULT_COLORS[color]
        raise KeyError(
            f'Unknown colour "{color}". Use a hex string, an (r, g, b) tuple or '
            f"one of {sorted(DEFAULT_COLORS)}"
        )
    color = tuple(int(c) for c in color)
    if len(color) != 3 or not all(0 <= c <= 255 for c in color):
        raise ValueError(f"Colour {color} must be 3 ints in the 0-255 range")
    return color


def resolve_font(font: str) -> str:
    """Return a usable font file path for a palette name or filesystem path."""
    if font in DEFAULT_FONTS:
        return DEFAULT_FONTS[font]
    if os.path.isfile(font):
        return font
    raise FileNotFoundError(
        f'Font "{font}" not found. Use one of {sorted(DEFAULT_FONTS)} or an '
        "existing font file path."
    )


def to_draw_color(color: ColorLike, color_format: str = "bgr") -> tuple:
    """Resolve *color* and order the channels for the target ``color_format``.

    Palette colours are defined in RGB. OpenCV images are BGR by default, so
    when drawing onto a BGR array the channels have to be reversed.
    """
    rgb = resolve_color(color)
    color_format = color_format.lower()
    if color_format == "rgb":
        return rgb
    if color_format == "bgr":
        return rgb[::-1]
    raise ValueError('color_format must be "bgr" or "rgb"')
