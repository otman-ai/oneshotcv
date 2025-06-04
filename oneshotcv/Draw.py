import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Union
from .utils import get_text_dimensions
from .palette import (DEFAULT_COLORS, DEFAULT_FONTS, 
                      DEFAULT_POSITIONS, DEFAULT_POSITIONS_FACTORS,
                      DEFAULT_SIZES, DEFAULT_SIZE_FACTORS)

# Draw text
def add_text(
         image: Image,
         text: str ="Text",
         position: Union[tuple, str] = DEFAULT_POSITIONS[0],
         color: Union[str, tuple] = DEFAULT_COLORS["white"],
         fontPath: str = DEFAULT_FONTS["arial"],
         size: Union[str, int] = DEFAULT_SIZES[2]
         ):
    """Draw text in the image

    Parametres
    ----------
    image: PIL image.
    text: string text to draw in the image .
    position: tuple in the format of (x, y) , represent the position in pixels .
    color: string from DEFAULT_COLORS or RGB tuple .
    fontPath: string from DEFAULT_FONTS or custom font path .
    size: The size of the text , either integer value or string from DEFAULT_SIZES.

    Returns
    ------
    image: PIL image with text .
    """
    text_color = color
    # check if the color is key 
    if type(color) == str:
        # get the color value using the key color
        text_color = DEFAULT_COLORS[color]
    
    width, height = image.size
    draw = ImageDraw.Draw(image)
    fontSize = size
    if type(size) == str:
        if size in DEFAULT_SIZES:
            fontSize = width * DEFAULT_SIZE_FACTORS[size] /486
        else:
            raise Exception(
                            f"size argument is not valid, make sure it is either integer or in {DEFAULT_SIZES}"
                            )

    font = ImageFont.truetype(fontPath, fontSize)

    text_width, text_height = get_text_dimensions(text, font)

    new_position = position
    # calculate the position
    if type(position) == str:
        new_width, new_height = width - text_width, height - text_height
        if position == "center":
            new_position = (new_width //2, 
                            new_height //2)

        elif position == "top-center": # top center
            new_position = (new_width // 2, 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["top"]))

        elif position == "bottom-center": # bottom center
            new_position = (new_width // 2, 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["bottom"]))

        elif position == "left-center": # left center
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["left"]), 
                            new_height // 2)

        elif position == "right-center": # right center
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["right"]), 
                            new_height // 2)

        elif position == "top-left": 
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["left"]), 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["top"]))

        elif position == "top-right": 
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["right"]), 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["top"]))

        elif position ==  "bottom-left":
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["left"]), 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["bottom"]))

        elif position == "bottom-right": 
            new_position = (int(new_width * DEFAULT_POSITIONS_FACTORS["right"]), 
                            int(new_height * DEFAULT_POSITIONS_FACTORS["bottom"]))
        else:
            raise Exception(
                f"Position is invalid, make sure it is (x, y) or in {DEFAULT_POSITIONS}"
                )

    draw.text(new_position, text, fill=text_color, font=font)

    return image

# Draw box arround an object or any
def add_box(bbox: tuple, 
        image: Image, 
        color = DEFAULT_COLORS["green"], 
        labelColor = DEFAULT_COLORS["white"],
        strokeSize = 4, 
        label = None, 
        fontPath = DEFAULT_FONTS["arial"],
        overlayAlpha = 0) -> Image:
    
    """Simplifiy drawing bounding box in the input image

    Parameters
    ----------
    bbox: list type contain bounding box in this format (x0, y0, x1, y1).
    image: Pillow Image datatype.
    color: background color, either in (r, b, g) or choice from DEFAULT_COLORS [white, green, black, yellow, blue].
    labelColor: Label color, either in (r, b, g) format or choice from DEFAULT_COLORS [white, green, black, yellow, blue].
    strokeSize: The stroke size of the rectangle .
    label: The text value to draw around the object .
    fontPath: the path to the font .
    overlayAlpha: the opacity of the overlay color inside the rectangle between 0-255 .
    
    Returns
    -------
    image: Image with box added
    """

    # get the color
    bg_color = color
    # check if the color is key 
    if type(color) == str:
        # get the color value using the key color
        bg_color = DEFAULT_COLORS[color]

    text_color = labelColor
    # check if the color is key 
    if type(labelColor) == str:
        # get the color value using the key labelColor
        text_color = DEFAULT_COLORS[labelColor]
     
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

    draw.rectangle(bbox, outline=bg_color, width=strokeSize)

    text_position = (x0, y0 - y_spacing)

    font = ImageFont.truetype(fontPath, fontSize)
    if label:
        text_width, text_height = get_text_dimensions(label, font)

        text_bg_position = (x0, 
                            y0 - y_spacing, 
                            x0 + text_width + padding, 
                            y0 -y_spacing + text_height )

        draw.rounded_rectangle(text_bg_position, fill=bg_color, width=strokeSize, radius=0)

        draw.text(text_position, label, fill=text_color, font=font)

    # Create a transparent overlay image (RGBA)
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))  # fully transparent

    # Draw a semi-transparent rectangle on the overlay
    overlay_draw = ImageDraw.Draw(overlay)
    if overlayAlpha:
        overlay_draw.rectangle(bbox, fill=bg_color+(overlayAlpha,))

        # Composite the overlay onto the base image
        image = Image.alpha_composite(image.convert('RGBA'), overlay)

    # return the image
    return image.convert('RGB')