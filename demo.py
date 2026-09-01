"""Small end-to-end demo. Run from the repo root: ``python demo.py``."""

import cv2

from oneshotcv import Draw

image = cv2.imread("assets/image.jpg")

boxed = Draw.add_box(
    (100, 100, 400, 400),
    image,
    label="Person",
    overlayAlpha=50,
)
boxed = Draw.add_text(boxed, "OneShotCV", position="bottom-center", color="yellow", size="lg")
boxed = Draw.add_keypoints(boxed, [(150, 150), (250, 200), (350, 300)], color="pink")
cv2.imwrite("assets/demo_box.png", boxed)

dog = cv2.imread("assets/dog.jpg")
mask = cv2.imread("assets/mask.png", cv2.IMREAD_GRAYSCALE)
masked = Draw.add_mask(image=dog, color="pink", mask=mask)
cv2.imwrite("assets/mask_output.jpg", masked)

print("wrote assets/demo_box.png and assets/mask_output.jpg")
