import pyautogui
import time
import cv2
import os
import time

# Function to click on a specific button based on its image
def click_button(image_path):
    button_position = pyautogui.locateOnScreen(image_path)
    button_center = pyautogui.center(button_position)
    pyautogui.click(button_center)

# Function to type a message into an input field
def type_message(message):
    pyautogui.typewrite(message)

os.system("notepad.exe")
time.sleep(10)

# Set the interval between each action (in seconds)
pyautogui.PAUSE = 1

# Open the Gmail website in your browser (place the correct path to your browser's executable)
pyautogui.press('win')
time.sleep(3)
pyautogui.typewrite('Chrome')
pyautogui.press('enter')
time.sleep(10)  # Wait for the browser to open
pyautogui.hotkey(['ctrl', 't'], logScreenshot = True)
time.sleep(3)
pyautogui.typewrite('https://mail.google.com')
pyautogui.press('enter')
time.sleep(10)  # Wait for the Gmail website to load

# Click on the "Compose" button
print('finding button')
button7location = pyautogui.locateOnScreen('compose.PNG', confidence=0.4)
print('postion:', button7location)
button7point = pyautogui.center(button7location)
button7x, button7y = button7point
print(button7x, button7y)
pyautogui.click(button7x, button7y)
# pyautogui.click('compose_button.png')

# click_button('compose_button.png')

# Type the recipient's email address
type_message('kevinhan9471@gmail.com')

time.sleep(1)
pyautogui.press('tab')

# Press "Tab" to move to the subject field
pyautogui.press('tab')

# Type the email subject
type_message('Subject of the email')
time.sleep(1)
# Press "Tab" to move to the email body
pyautogui.press('tab')
time.sleep(1)

# Type the email body
type_message('This is the body of the email')
time.sleep(1)
# Press "Tab" to move to the send button and "Enter" to send the email
pyautogui.press('tab')
time.sleep(1)
pyautogui.press('enter')

# Wait for the email to be sent
time.sleep(5)

# Close the browser
pyautogui.hotkey('ctrl', 'w')
