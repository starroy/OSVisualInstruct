from openai import OpenAI
import os
import re
import subprocess

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def new_task(prompt):
  print("get::::::", prompt)
  addition_prompt = '!important :  input sleep time 2 seconde after every instruction.'
  code_prompt = 'im = pyautogui.screenshot() im.save("tes.jpg") img = "tes.jpg"  imge = Image.open(img) data=pytesseract.image_to_boxes(imge) print(data)'
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are my automation logic assistance using tesseract ocr and pyautogui. Please give me automation steps using tesseract ocr and pyautogui in windows 10 os environment."},
      {"role": "user", "content": "First, detect words and find coordination of word using tesseract OCR usig like " + code_prompt + "instruction and save it 'detect.png'. And use the coordinate of text which is detected by OCR. pyautogui automation logic and code need. output first paragraph is logic steps one by one and the second paragraph is pyautogui automation full code. print 'success' and each step number in automation code when achieve every steps. output only steps in first output paragraph. : " + prompt + addition_prompt}
    ]
  )
  # "pyautogui automation code step by step. mark each step with prefix 'step' : "
  #get the result from gpt.
  gpt_result = completion.choices[0].message.content
  print(gpt_result)


  result = []
  # Define the regular expression pattern to match the logic steps
  pattern = r"\d+\.\s(.*?)(?=\n)"

  # Use the findall() function to find all matches of the pattern in the text
  matches = re.findall(pattern, gpt_result)

  # Print the logic steps
  logic_steps = [match.strip() for match in matches]
  print(logic_steps)

    # Using the re module to extract content surrounded by triple quotes
  auto_instruction = re.findall(r"```(.*?)```", gpt_result, re.DOTALL)
  # print(auto_instruction)

  # Display the extracted content
  instruction=""
  try:
    instruction = auto_instruction[0].split("\n",1)[1]
  except Exception as e:
    print(e)

  #write auto instruction into automation.py file and run it.
  with open('instruction.py', 'w+') as f:
      f.write(instruction)

  return logic_steps
