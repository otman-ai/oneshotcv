from oneshotcv import Draw
from PIL import Image
image = Image.open("assets/image.jpg")

"""Testing text drawing"""
image = Image.open("assets/image.jpg")
image_tested = Image.open("assets/image_with_text.png")

new_image = Draw.add_text(image, "Hi this is text", 
                          position="top-left", 
                          color="white",
                          size="normal")

new_image.save("assets/white_text_image.png")
