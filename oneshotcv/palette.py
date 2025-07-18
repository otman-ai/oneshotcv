from pathlib import Path

DEFAULT_COLORS = {
    "green": (107, 212, 28),
    "white": (255, 255, 255),
    "blue": (28, 126, 212),
    "red": (212, 28, 28),
    "black": (20, 20, 20),
    "yellow": (197, 214, 43),
    "pink": (214, 43, 205),
    }

DEFAULT_FONTS = {
    "arial": Path(".") / "fonts" / "arial.ttf",
    "mont": Path(".") / "fonts" / "mont.otf",
    "nexa": Path(".") / "fonts" / "nexa.ttf",
    "coolvetica": Path(".") / "fonts" / "coolvetica.otf"
}

DEFAULT_POSITIONS_FACTORS = {
    "top":0.05,
    "bottom":0.95,
    "left":0.05,
    "right":0.95
}

DEFAULT_POSITIONS = ["center", 
                     "bottom-center", 
                     "top-center",
                     "left-center",
                     "right-center",
                     "top-left", 
                     "top-right", 
                     "bottom-left", 
                     "bottom-right"]

DEFAULT_SIZES = [ "xl","lg","normal", "sm", "xs"]

DEFAULT_SIZE_FACTORS ={
    "xl":40,
    "lg":25,
    "normal":18,
    "sm":13,
    "xs":11
}
