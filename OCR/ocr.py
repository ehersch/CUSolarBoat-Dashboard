from PIL import Image
from pytesseract import pytesseract

image_path = r"images/kmc2.png"
  
# Opening the image & storing it in an image object
img = Image.open(image_path)

text = pytesseract.image_to_string(img)
  
# Displaying the extracted text
print(text[:-1])