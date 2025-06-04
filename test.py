from oneshotcv import Draw
from PIL import Image
image = Image.open("assets/image.jpg")

bbox  = (100, 100, 400, 400)
new_image = Draw.box(bbox, 
                    image,
                    label="Persone",
                    overlayAlpha=50
                    )

new_image.save("assets/image_with_bbox.png")