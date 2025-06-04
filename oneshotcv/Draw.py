import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Union

from .utils import get_text_dimensions
from .palette import DEFAULT_COLORS

# Draw box arround an object or any
def box(bbox: tuple, 
         image: Image, 
         color = DEFAULT_COLORS["green"], 
         labelColor = DEFAULT_COLORS["white"],
         lineSize = 4, 
         label = None, 
         fontPath = "assets/ARIAL.TTF",
         overlayAlpha = 0) -> Image:
    
    """Simplifiy drawing bounding box in the input image

    Parameters
    ----------
    bbox: list type contain bounding box in this format (x0, y0, x1, y1),
    image: Pillow Image datatype
    color: background color, either in (r, b, g) or choice from DEFAULT_COLORS [white, green, black, yellow, blue]
    labelColor: Label color, either in (r, b, g) format or choice from DEFAULT_COLORS [white, green, black, yellow, blue]
    lineSize: The stroke size of the rectangle
    label: The text value to draw around the object
    fontPath: the path to the font
    overlayAlpha: the opacity of the overlay color inside the rectangle between 0-255

    Returns
    -------
    combined: Pillow Image datatype
    """

    # get the color
    bg_color = color
    # check if the color is key 
    if type(color) == str:
        # get the color value using the key color
        bg_color = DEFAULT_COLORS[color]
    
    # Chech if overlayAlpha is valid
    if not 0<=overlayAlpha<=255:
        raise Exception("overlayAlpha argument is not valid, make sure it is in 0-255 range")

    x0, y0, x1, y1 = bbox
    draw = ImageDraw.Draw(image)
    width, height = image.size


    # normal size
    padding = width * 5 /486 # 486
    fontSize = width * 25 /486
    y_spacing = height * 26 / 500 # h=500

    draw.rectangle(bbox, outline=bg_color, width=lineSize)

    text_position = (x0, y0 - y_spacing)

    font = ImageFont.truetype(fontPath, fontSize)
    if label:
        text_width, text_height = get_text_dimensions(label, font)

        text_bg_position = (x0, 
                            y0 - y_spacing, 
                            x0 + text_width + padding, 
                            y0 -y_spacing + text_height )

        draw.rectangle(text_bg_position, fill=bg_color, width=lineSize)

        draw.text(text_position, label, fill=labelColor, font=font)

    # Create a transparent overlay image (RGBA)
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))  # fully transparent

    # Draw a semi-transparent rectangle on the overlay
    overlay_draw = ImageDraw.Draw(overlay)
    if overlayAlpha:
        overlay_draw.rectangle(bbox, fill=bg_color+(overlayAlpha,))

        # Composite the overlay onto the base image
        image = Image.alpha_composite(image.convert('RGBA'), overlay)

    # return the  image
    return image.convert('RGB')