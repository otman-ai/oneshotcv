# Changelog

## 0.2.0

### Fixed
- Bundled fonts are now shipped inside the package (`oneshotcv/fonts/`) and
  declared as package data, so `add_box` / `add_text` work after
  `pip install` instead of raising `OSError: cannot open resource`.
- Font sizes are cast to `int` before being handed to Pillow.
- `add_box` always returns a 3-channel image, even with `overlayAlpha` set.
- `add_text` handles empty strings and the `left-center` / `right-center`
  positions correctly.
- `license` metadata now matches the actual `LICENSE` file (Apache-2.0).
- `pytest` moved from runtime dependencies to the `test` extra.
- `numpy` / `opencv-python` / `pillow` lower bounds pinned; `requires-python`
  lowered to `>=3.9`.

### Added
- `add_circle`, `add_line`, `add_polygon`, `add_keypoints`.
- Hex colour strings (`"#6bd41c"`) and an explicit `color_format`
  (`"bgr"` default / `"rgb"`) argument on every helper.
- `Draw.list_colors()` / `Draw.list_fonts()` and `oneshotcv.__version__`.
- Extra palette colours: `orange`, `purple`, `cyan`, `gray`.
- End-to-end test suite (synthetic images, no golden files) and a GitHub
  Actions workflow running it on Python 3.9-3.13 plus a packaging check.
