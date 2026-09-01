"""End-to-end tests for the drawing helpers.

These do not rely on any checked-in golden image: they build synthetic
images, run each helper and assert on shape, dtype, immutability of the input
and on the pixels that must have changed.
"""

import numpy as np
import pytest

import oneshotcv
from oneshotcv import Draw
from oneshotcv.utils import hex_to_rgb, resolve_color, resolve_font


def _assert_valid_output(out, ref):
    assert isinstance(out, np.ndarray)
    assert out.shape == ref.shape
    assert out.dtype == np.uint8


# ---------------------------------------------------------------------------
# add_mask
# ---------------------------------------------------------------------------
def test_add_mask_colors_only_masked_pixels(image, mask):
    out = Draw.add_mask(image, mask, color="red", opacity=1.0)
    _assert_valid_output(out, image)

    m = mask.astype(bool)
    # masked area changed, everything else untouched
    assert np.any(out[m] != image[m])
    assert np.array_equal(out[~m], image[~m])
    # opacity=1 + bgr => palette red (212, 28, 28) written in BGR order
    assert np.array_equal(np.unique(out[m].reshape(-1, 3), axis=0), np.array([[28, 28, 212]]))


def test_add_mask_opacity_blends(image, mask):
    out = Draw.add_mask(image, mask, color=(0, 0, 0), opacity=0.5)
    m = mask.astype(bool)
    assert np.allclose(out[m], 63, atol=1)


def test_add_mask_does_not_mutate_input(image, mask):
    before = image.copy()
    Draw.add_mask(image, mask, color="blue")
    assert np.array_equal(image, before)


def test_add_mask_rejects_bad_opacity(image, mask):
    with pytest.raises(ValueError):
        Draw.add_mask(image, mask, opacity=5)


def test_add_mask_rejects_shape_mismatch(image):
    with pytest.raises(ValueError):
        Draw.add_mask(image, np.zeros((10, 10), dtype=np.uint8))


def test_add_mask_rejects_non_array(image, mask):
    with pytest.raises(TypeError):
        Draw.add_mask([[1, 2]], mask)


# ---------------------------------------------------------------------------
# add_text
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("position", oneshotcv.DEFAULT_POSITIONS)
def test_add_text_named_positions(image, position):
    out = Draw.add_text(image, "hi", position=position, color="white")
    _assert_valid_output(out, image)
    assert np.any(out != image)


@pytest.mark.parametrize("size", oneshotcv.DEFAULT_SIZES + [10, 42])
def test_add_text_sizes(image, size):
    out = Draw.add_text(image, "hi", size=size)
    assert np.any(out != image)


def test_add_text_tuple_position(image):
    out = Draw.add_text(image, "x", position=(5, 5))
    assert np.any(out != image)


def test_add_text_invalid_position(image):
    with pytest.raises(ValueError):
        Draw.add_text(image, "x", position="middle")


def test_add_text_invalid_size(image):
    with pytest.raises(ValueError):
        Draw.add_text(image, "x", size="huge")


def test_add_text_invalid_font(image):
    with pytest.raises(FileNotFoundError):
        Draw.add_text(image, "x", font="comic-sans")


def test_add_text_empty_string_is_noop(image):
    out = Draw.add_text(image, "", position="center")
    assert np.array_equal(out, image)


# ---------------------------------------------------------------------------
# add_box
# ---------------------------------------------------------------------------
def test_add_box_draws_outline(image):
    out = Draw.add_box((40, 40, 200, 180), image, color="green")
    _assert_valid_output(out, image)
    # border pixels changed, centre of the box untouched
    assert np.any(out[40, 40:200] != image[40, 40:200])
    assert np.array_equal(out[110, 120], image[110, 120])


def test_add_box_with_label(image):
    out = Draw.add_box((40, 60, 200, 180), image, label="cat", color="blue")
    assert np.any(out != image)


def test_add_box_overlay_alpha_fills(image):
    out = Draw.add_box((40, 40, 200, 180), image, color="red", overlayAlpha=120)
    assert not np.array_equal(out[110, 120], image[110, 120])
    assert out.shape == image.shape  # stays 3-channel


def test_add_box_label_near_top_edge(image):
    out = Draw.add_box((10, 2, 120, 90), image, label="edge")
    _assert_valid_output(out, image)


def test_add_box_invalid_bbox(image):
    with pytest.raises(ValueError):
        Draw.add_box((1, 2, 3), image)


def test_add_box_invalid_overlay(image):
    with pytest.raises(ValueError):
        Draw.add_box((1, 2, 3, 4), image, overlayAlpha=999)


# ---------------------------------------------------------------------------
# extra primitives
# ---------------------------------------------------------------------------
def test_add_circle(image):
    out = Draw.add_circle(image, (160, 120), 50, color="yellow")
    assert np.any(out[120, 110] != image[120, 110])
    assert np.array_equal(out[120, 160], image[120, 160])  # hollow centre


def test_add_circle_filled_with_opacity(image):
    out = Draw.add_circle(image, (160, 120), 40, color=(0, 0, 0), fill=True, opacity=0.5)
    assert np.allclose(out[120, 160], 63, atol=2)


def test_add_circle_bad_radius(image):
    with pytest.raises(ValueError):
        Draw.add_circle(image, (10, 10), 0)


def test_add_line(image):
    out = Draw.add_line(image, (0, 0), (319, 239), color="white", thickness=2)
    assert np.any(out != image)
    assert np.array_equal(out[0, 300], image[0, 300])


def test_add_polygon(image):
    out = Draw.add_polygon(image, [(20, 20), (200, 40), (120, 200)], color="cyan")
    assert np.any(out != image)


def test_add_polygon_needs_three_points(image):
    with pytest.raises(ValueError):
        Draw.add_polygon(image, [(0, 0), (1, 1)])


def test_add_keypoints(image):
    pts = [(30, 30), (100, 100), (200, 150)]
    out = Draw.add_keypoints(image, pts, color="red", radius=5)
    for x, y in pts:
        assert np.any(out[y, x] != image[y, x])


# ---------------------------------------------------------------------------
# colour / font resolution
# ---------------------------------------------------------------------------
def test_hex_to_rgb():
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("#000") == (0, 0, 0)
    assert hex_to_rgb("6bd41c") == (107, 212, 28)


def test_hex_to_rgb_invalid():
    with pytest.raises(ValueError):
        hex_to_rgb("#12")


def test_resolve_color_forms():
    assert resolve_color("green") == (107, 212, 28)
    assert resolve_color("#22d3ee") == (34, 211, 238)
    assert resolve_color((1, 2, 3)) == (1, 2, 3)


def test_resolve_color_unknown_name():
    with pytest.raises(KeyError):
        resolve_color("chartreuse")


def test_resolve_color_bad_tuple():
    with pytest.raises(ValueError):
        resolve_color((1, 2, 3, 4))
    with pytest.raises(ValueError):
        resolve_color((0, 0, 300))


def test_color_format_swaps_channels(image):
    hex_color = "#0a141e"  # asymmetric
    bgr = Draw.add_mask(image, np.full(image.shape[:2], 255, np.uint8), hex_color, 1.0, "bgr")
    rgb = Draw.add_mask(image, np.full(image.shape[:2], 255, np.uint8), hex_color, 1.0, "rgb")
    assert np.array_equal(bgr[0, 0][::-1], rgb[0, 0])


def test_bundled_fonts_resolve_to_real_files():
    fonts = Draw.list_fonts()
    assert set(fonts) == {"arial", "mont", "nexa", "coolvetica"}
    for path in fonts.values():
        assert resolve_font(path) == path
        from PIL import ImageFont

        ImageFont.truetype(path, 12)  # must not raise


def test_list_colors_is_a_copy():
    colors = Draw.list_colors()
    colors["green"] = (0, 0, 0)
    assert Draw.list_colors()["green"] == (107, 212, 28)


def test_version_exposed():
    assert isinstance(oneshotcv.__version__, str)


# ---------------------------------------------------------------------------
# optional: exercise against the repo sample assets when they are present
# ---------------------------------------------------------------------------
def test_pipeline_on_sample_assets(tmp_path):
    cv2 = pytest.importorskip("cv2")
    import os

    root = os.path.join(os.path.dirname(__file__), "..")
    img_path = os.path.join(root, "assets", "image.jpg")
    if not os.path.exists(img_path):
        pytest.skip("sample assets not available")

    img = cv2.imread(img_path)
    out = Draw.add_box((100, 100, 400, 400), img, label="Person", overlayAlpha=50)
    out = Draw.add_text(out, "hello", position="top-left")
    dst = tmp_path / "out.png"
    assert cv2.imwrite(str(dst), out)
    assert dst.exists() and dst.stat().st_size > 0
    assert cv2.imread(str(dst)).shape == img.shape
