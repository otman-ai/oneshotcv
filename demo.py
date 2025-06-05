from oneshotcv import Draw
import cv2

image = cv2.imread("assets/dog.jpg")
mask = cv2.imread("assets/mask.png",  cv2.IMREAD_GRAYSCALE)

new_image = Draw.add_mask(image=image,
                          color="pink",
                           mask=mask)


cv2.imwrite('assets/mask_output.jpg', new_image)