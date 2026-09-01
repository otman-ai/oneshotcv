from pathlib import Path

PACKAGE_DIR = Path(__file__).parent
FONTS_DIR = PACKAGE_DIR / "fonts"

# Colours are stored as RGB triplets.
DEFAULT_COLORS = {
    "green": (107, 212, 28),
    "white": (255, 255, 255),
    "blue": (28, 126, 212),
    "red": (212, 28, 28),
    "black": (20, 20, 20),
    "yellow": (197, 214, 43),
    "pink": (214, 43, 205),
    "orange": (245, 158, 11),
    "purple": (139, 92, 246),
    "cyan": (34, 211, 238),
    "gray": (107, 114, 128),
}

DEFAULT_FONTS = {
    "arial": str(FONTS_DIR / "arial.ttf"),
    "mont": str(FONTS_DIR / "mont.otf"),
    "nexa": str(FONTS_DIR / "nexa.ttf"),
    "coolvetica": str(FONTS_DIR / "coolvetica.otf"),
}

DEFAULT_POSITIONS_FACTORS = {
    "top": 0.05,
    "bottom": 0.95,
    "left": 0.05,
    "right": 0.95,
}

DEFAULT_POSITIONS = [
    "center",
    "bottom-center",
    "top-center",
    "left-center",
    "right-center",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
]

DEFAULT_SIZES = ["xl", "lg", "normal", "sm", "xs"]

DEFAULT_SIZE_FACTORS = {
    "xl": 40,
    "lg": 25,
    "normal": 18,
    "sm": 13,
    "xs": 11,
}
