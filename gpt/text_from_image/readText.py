import pytesseract
from PIL import Image

# Path to the Tesseract OCR executable (may vary depending on the installation method)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Open the image file using PIL
image = Image.open('Evos.jpg')

# Use pytesseract to extract text from the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)