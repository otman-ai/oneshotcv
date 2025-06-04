import pytest
from oneshotcv import Draw
from PIL import Image

def test_draw_box():
    image = Image.open("assets/image.jpg")
    image_tested = Image.open("assets/image_with_bbox.png")


    bbox  = (100, 100, 400, 400)
    new_image = Draw.box(bbox, 
                        image,
                        label="Persone",
                        overlayAlpha=50
                        )
    new_image.save("assets/tested_image_with_bbox.png")

    assert Image.open("assets/tested_image_with_bbox.png") == image_tested


if __name__ == '__main__':
    pytest.main()