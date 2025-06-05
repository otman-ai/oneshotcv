import pytest
from oneshotcv import Draw
import cv2
import numpy as np

def test_draw_mask():
    """Testing mask drawing"""
    new_image = Draw.add_mask(image=cv2.imread("assets/dog.jpg"),
                            color="pink",
                            mask=cv2.imread("assets/mask.png", cv2.IMREAD_GRAYSCALE).astype(np.uint8))
    cv2.imwrite("assets/test_mask_output.jpg",new_image)
    assert cv2.imread("assets/test_mask_output.jpg").all() == cv2.imread("assets/mask_output.jpg").all()

def test_draw_text():
    """Testing text drawing"""
    image = cv2.imread("assets/image.jpg")
    new_image = Draw.add_text(
                        image=image, 
                        text="Hi this is text", 
                        position="top-left", 
                        color="white",
                        size="normal")
    cv2.imwrite("assets/tested_white_text_image.png", new_image)
    assert cv2.imread("assets/tested_white_text_image.png").all() == cv2.imread("assets/white_text_image.png").all()


def test_draw_box():
    """Testing box drawing"""
    image = cv2.imread("assets/image.jpg")

    bbox  = (100, 100, 400, 400)
    new_image = Draw.add_box(bbox, 
                        image,
                        label="Persone",
                        overlayAlpha=50,
                        fontPath="fonts/ARIAL.TTF"
                        )
    cv2.imwrite("assets/tested_image_with_bbox.png", new_image)
    assert cv2.imread("assets/tested_image_with_bbox.png").all() ==  cv2.imread("assets/image_with_bbox.png").all()


if __name__ == '__main__':
    pytest.main()