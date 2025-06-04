import pytest
from oneshotcv import Draw
from PIL import Image


def test_draw_text():
    """Testing text drawing"""
    image = Image.open("assets/image.jpg")
    image_tested = Image.open("assets/white_text_image.png")

    new_image = Draw.add_text(
                        image=image, 
                        text="Hi this is text", 
                        position="top-left", 
                        color="white",
                        size="normal")
    new_image.save("assets/tested_white_text_image.png")

    assert Image.open("assets/tested_white_text_image.png") == image_tested


def test_draw_box():
    """Testing box drawing"""
    image = Image.open("assets/image.jpg")
    image_tested = Image.open("assets/image_with_bbox.png")


    bbox  = (100, 100, 400, 400)
    new_image = Draw.add_box(bbox, 
                        image,
                        label="Persone",
                        overlayAlpha=50,
                        fontPath="fonts/ARIAL.TTF"
                        )
    new_image.save("assets/tested_image_with_bbox.png")

    assert Image.open("assets/tested_image_with_bbox.png") == image_tested


if __name__ == '__main__':
    pytest.main()