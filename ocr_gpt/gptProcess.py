from openai import OpenAI
import os
import re
import subprocess

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def new_task(prompt):
  addition_prompt = 'When Press the "win" key, you sometimes does not focus on the search, so focus on search and input. when opened program with fullscreen then take sleep time 2 second. and before start every instruction take sleep time 1 second.'

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      
      {"role": "system", "content": "Your code assistent, Please give me automation code using pyautogui in windows 10 os environment."},
      {"role": "user", "content": "pyautogui automation code step by step. mark each step with prefix 'step' : " + prompt + addition_prompt}
    ]
  )
  # "pyautogui automation code step by step. mark each step with prefix 'step' : "
  #get the result from gpt.
  gpt_result = completion.choices[0].message.content
  print(gpt_result)


  result = []
  steps = re.split(r"(?i)step \d:\s+", gpt_result)
  for step in steps:
    # print("---------steps---------")
    instruction = step.split("\n",1)[0]
    result.append(instruction)
    # print(instruction)
    # print("---end----")
  result.pop(0)
  return result

#   # Using the re module to extract content surrounded by triple quotes
#   auto_instruction = re.findall(r"```(.*?)```", gpt_result, re.DOTALL)
#   # print(auto_instruction)
#   # Display the extracted content

#   instruction = auto_instruction[0].split("\n",1)[0]

#   print(instruction)

#   #write auto instruction into automation.py file and run it.
#   with open('instruction.py', 'w+') as f:
#       f.write(instruction)

#   # subprocess.check_call()
#   # subprocess.run('py instruction.py', shell=True)

#   # Check if the file exists
#   if os.path.exists('instruction.py'):
#       # Delete the file
#       os.remove('instruction.py')
#       print("File deleted successfully.")
#   else:
#       print("File does not exist.")

# def getInstruction(paragraph):
#   auto_instruction = re.findall(r"```(.*?)```", paragraph, re.DOTALL)
#   return auto_instruction