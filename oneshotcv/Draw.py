"""High level drawing helpers.

Every function takes a ``numpy`` image (as returned by ``cv2.imread``), never
mutates it, and returns a new ``numpy`` array of the same shape and dtype.
Colours may be given as a palette name (``"green"``), a hex string
(``"#6bd41c"``) or an ``(r, g, b)`` tuple. Because OpenCV images are BGR, the
channel order of the input/output is controlled by ``color_format`` which
defaults to ``"bgr"``.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Sequence, Tuple, Union

from .utils import get_text_dimensions, resolve_color, resolve_font, to_draw_color
from .palette import (
    DEFAULT_COLORS,
    DEFAULT_FONTS,
    DEFAULT_POSITIONS,
    DEFAULT_POSITIONS_FACTORS,
    DEFAULT_SIZES,
    DEFAULT_SIZE_FACTORS,
)

ColorLike = Union[str, Sequence[int]]
Point = Tuple[int, int]


def _as_array(image) -> np.ndarray:
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy array (e.g. from cv2.imread)")
    return image.copy()


def _blend(base: np.ndarray, region: slice, color: tuple, opacity: float) -> None:
    """Alpha-blend a solid *color* into *base* at the boolean/slice *region*."""
    patch = base[region].astype(np.float32)
    color_arr = np.array(color, dtype=np.float32)
    base[region] = (patch * (1 - opacity) + color_arr * opacity).astype(base.dtype)


# ---------------------------------------------------------------------------
# Mask
# ---------------------------------------------------------------------------
def add_mask(
    image: np.ndarray,
    mask: np.ndarray,
    color: ColorLike = "blue",
    opacity: Union[int, float] = 0.5,
    color_format: str = "bgr",
) -> np.ndarray:
    """Overlay a segmentation *mask* on *image*.

    Parameters
    ----------
    image: HxWxC ``numpy`` array.
    mask: HxW array, non-zero for the pixels to colour.
    color: palette name, hex string or ``(r, g, b)`` tuple.
    opacity: overlay strength in the ``0-1`` range.
    color_format: ``"bgr"`` (OpenCV, default) or ``"rgb"``.

    Returns
    -------
    ``numpy`` array with the mask blended in.
    """
    output = _as_array(image)
    if mask is None or not isinstance(mask, np.ndarray):
        raise TypeError("mask must be a numpy array")
    if mask.shape[:2] != output.shape[:2]:
        raise ValueError(
            f"mask shape {mask.shape[:2]} does not match image {output.shape[:2]}"
        )
    if not 0 <= opacity <= 1:
        raise ValueError(f"opacity {opacity} is not between 0 and 1")

    draw_color = to_draw_color(color, color_format)
    mask_indices = mask.astype(bool)
    _blend(output, mask_indices, draw_color, float(opacity))
    return output


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
def add_text(
    image: np.ndarray,
    text: str = "Text",
    position: Union[Point, str] = DEFAULT_POSITIONS[0],
    color: ColorLike = "white",
    font: str = "arial",
    size: Union[str, int] = DEFAULT_SIZES[2],
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw *text* on *image*.

    ``position`` is either an ``(x, y)`` pixel tuple or one of
    :data:`oneshotcv.palette.DEFAULT_POSITIONS`. ``size`` is a pixel integer or
    one of :data:`oneshotcv.palette.DEFAULT_SIZES`.
    """
    output = _as_array(image)
    pil_image = Image.fromarray(output)
    width, height = pil_image.size
    draw = ImageDraw.Draw(pil_image)

    if isinstance(size, str):
        if size not in DEFAULT_SIZES:
            raise ValueError(
                f'size "{size}" is invalid, use an int or one of {DEFAULT_SIZES}'
            )
        font_size = max(1, int(width * DEFAULT_SIZE_FACTORS[size] / 486))
    else:
        font_size = max(1, int(size))

    pil_font = ImageFont.truetype(resolve_font(font), font_size)
    text_color = to_draw_color(color, color_format)
    text_width, text_height = get_text_dimensions(text, pil_font)

    if isinstance(position, str):
        if position not in DEFAULT_POSITIONS:
            raise ValueError(
                f'position "{position}" is invalid, use (x, y) or one of '
                f"{DEFAULT_POSITIONS}"
            )
        free_w, free_h = width - text_width, height - text_height
        fx = DEFAULT_POSITIONS_FACTORS
        horizontal = {
            "left": int(free_w * fx["left"]),
            "center": free_w // 2,
            "right": int(free_w * fx["right"]),
        }
        vertical = {
            "top": int(free_h * fx["top"]),
            "center": free_h // 2,
            "bottom": int(free_h * fx["bottom"]),
        }
        v = h = "center"
        for token in position.split("-"):
            if token in ("top", "bottom"):
                v = token
            elif token in ("left", "right"):
                h = token
        draw_position = (horizontal[h], vertical[v])
    else:
        draw_position = (int(position[0]), int(position[1]))

    draw.text(draw_position, text, fill=text_color, font=pil_font)
    return np.array(pil_image)


# ---------------------------------------------------------------------------
# Bounding box
# ---------------------------------------------------------------------------
def add_box(
    bbox: Sequence[int],
    image: np.ndarray,
    color: ColorLike = "green",
    labelColor: ColorLike = "white",
    strokeSize: int = 4,
    label: str = None,
    fontPath: str = "arial",
    overlayAlpha: int = 0,
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw a bounding *bbox* ``(x0, y0, x1, y1)`` with an optional *label*.

    ``overlayAlpha`` (``0-255``) fills the box with a translucent colour.
    """
    output = _as_array(image)
    if len(bbox) != 4:
        raise ValueError("bbox must be (x0, y0, x1, y1)")
    if not 0 <= overlayAlpha <= 255:
        raise ValueError("overlayAlpha must be in the 0-255 range")

    pil_image = Image.fromarray(output).convert("RGB")
    draw = ImageDraw.Draw(pil_image)
    width, _ = pil_image.size

    bg_color = to_draw_color(color, color_format)
    text_color = to_draw_color(labelColor, color_format)

    x0, y0, x1, y1 = (int(v) for v in bbox)
    padding = width * 5 / 486
    font_size = max(1, int(width * 25 / 486))
    y_spacing = max(font_size + 4, int(pil_image.size[1] * 26 / 500))

    draw.rectangle((x0, y0, x1, y1), outline=bg_color, width=int(strokeSize))

    if label:
        pil_font = ImageFont.truetype(resolve_font(fontPath), font_size)
        text_width, text_height = get_text_dimensions(label, pil_font)
        label_y = max(0, y0 - y_spacing)
        draw.rectangle(
            (x0, label_y, x0 + text_width + padding, label_y + text_height),
            fill=bg_color,
        )
        draw.text((x0, label_y), label, fill=text_color, font=pil_font)

    if overlayAlpha:
        overlay = Image.new("RGBA", pil_image.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).rectangle(
            (x0, y0, x1, y1), fill=tuple(bg_color) + (int(overlayAlpha),)
        )
        pil_image = Image.alpha_composite(pil_image.convert("RGBA"), overlay).convert(
            "RGB"
        )

    return np.array(pil_image)


# ---------------------------------------------------------------------------
# Extra primitives
# ---------------------------------------------------------------------------
def add_circle(
    image: np.ndarray,
    center: Point,
    radius: int,
    color: ColorLike = "green",
    thickness: int = 3,
    fill: bool = False,
    opacity: float = 1.0,
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw a circle (outline, or filled when ``fill=True``)."""
    if radius <= 0:
        raise ValueError("radius must be positive")
    if not 0 <= opacity <= 1:
        raise ValueError("opacity must be between 0 and 1")

    output = _as_array(image)
    draw_color = to_draw_color(color, color_format)
    cx, cy = int(center[0]), int(center[1])
    box = (cx - radius, cy - radius, cx + radius, cy + radius)

    layer = Image.fromarray(output).convert("RGB")
    ImageDraw.Draw(layer).ellipse(
        box,
        outline=None if fill else draw_color,
        fill=draw_color if fill else None,
        width=int(thickness),
    )
    drawn = np.array(layer)
    if opacity >= 1.0:
        return drawn
    changed = np.any(drawn != output, axis=-1)
    _blend(output, changed, draw_color, opacity)
    return output


def add_line(
    image: np.ndarray,
    start: Point,
    end: Point,
    color: ColorLike = "green",
    thickness: int = 3,
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw a straight line from *start* to *end*."""
    output = _as_array(image)
    draw_color = to_draw_color(color, color_format)
    layer = Image.fromarray(output).convert("RGB")
    ImageDraw.Draw(layer).line(
        [(int(start[0]), int(start[1])), (int(end[0]), int(end[1]))],
        fill=draw_color,
        width=int(thickness),
    )
    return np.array(layer)


def add_polygon(
    image: np.ndarray,
    points: Sequence[Point],
    color: ColorLike = "green",
    thickness: int = 3,
    fill: bool = False,
    opacity: float = 1.0,
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw a closed polygon through *points* (list of ``(x, y)``)."""
    if len(points) < 3:
        raise ValueError("a polygon needs at least 3 points")
    if not 0 <= opacity <= 1:
        raise ValueError("opacity must be between 0 and 1")

    output = _as_array(image)
    draw_color = to_draw_color(color, color_format)
    pts = [(int(x), int(y)) for x, y in points]

    layer = Image.fromarray(output).convert("RGB")
    ImageDraw.Draw(layer).polygon(
        pts,
        outline=draw_color,
        fill=draw_color if fill else None,
        width=int(thickness),
    )
    drawn = np.array(layer)
    if opacity >= 1.0:
        return drawn
    changed = np.any(drawn != output, axis=-1)
    _blend(output, changed, draw_color, opacity)
    return output


def add_keypoints(
    image: np.ndarray,
    points: Sequence[Point],
    color: ColorLike = "red",
    radius: int = 4,
    color_format: str = "bgr",
) -> np.ndarray:
    """Draw a filled dot for every ``(x, y)`` in *points*."""
    output = _as_array(image)
    draw_color = to_draw_color(color, color_format)
    layer = Image.fromarray(output).convert("RGB")
    drawer = ImageDraw.Draw(layer)
    for x, y in points:
        x, y = int(x), int(y)
        drawer.ellipse((x - radius, y - radius, x + radius, y + radius), fill=draw_color)
    return np.array(layer)


# ---------------------------------------------------------------------------
# Introspection helpers
# ---------------------------------------------------------------------------
def list_colors() -> dict:
    """Return the built-in palette as ``{name: (r, g, b)}``."""
    return dict(DEFAULT_COLORS)


def list_fonts() -> dict:
    """Return the bundled fonts as ``{name: path}``."""
    return dict(DEFAULT_FONTS)
