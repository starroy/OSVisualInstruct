import pyautogui
from PIL import Image
import pytesseract
from pytesseract import Output
import time

# Step 1: Take a screenshot and save it as 'tes.jpg'
im = pyautogui.screenshot()
im.save('tes.jpg')
print("Step 1: Success")

# Step 2: Open the saved image using PIL
img = 'tes.jpg'
imge = Image.open(img)
print("Step 2: Success")

# Step 3: Use pytesseract to perform OCR on the image
d = pytesseract.image_to_data(imge, output_type=Output.DICT)
print("Step 3: Success")

# Step 4: Iterate through the detected text
n_boxes = len(d['text'])
for i in range(n_boxes):
    # Step 5: Filter out text with confidence higher than 60%
    if int(d['conf'][i]) > 60:
        # Step 6: Retrieve the coordinates of each detected word
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        print(f"Detected Word: {d['text'][i]}")
        print(f"Coordinates: ({x}, {y}, {w}, {h})")

    time.sleep(2)
    print(f"Step 4-6: Success for word {i+1}")

print("Success")
