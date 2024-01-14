## Grid Screenshot Prompt


### System Prompt
Attached is a screenshot of my desktop with various applications open.
The x, y pixel values start at 0,0 at the top left and the y values are labeled on the left-side and the x values are on-top of the screenshot provided, the x values are in increments of 50 and the y values are in increments of 20.

Start by describing the user's screenshot in detail, and finally answer their question in the form of a coordinate tuple (x,y) (e.g. (1020, 400))

### User Prompt
What are the x,y coordinates for the "X"/close button for my Windows Explorer application?




## ~~Initial Project Prompt~~

~~Given the screenshot I took of my desktop, write a program described below.~~

~~The program will be ran on a raspberry PI and only have access to the HDMI video output of the target computer, and a usb connect that is the mouse and keyboard (used to perform the actions, provided with the HDMI video output).
The program  will have a refresh rate of 750 milliseconds after every action (click on x, send keystroke/hotkeys, move to x,y coordinate and click, type keys, etc). The program will take in a text message and use a llm to understand the task the user wants to have it perform: it will take a screenshot of the current video, and send that to Gpt-4Vision along with the users prompt, the response should be various actions mentioned previously, with a recommended timeout after each action, and then perform the various actions, until the task is complete.~~

~~Given the resolution of the screenshot (1920x1080) create a program to figure out the x,y coordinates of things to click on given the previous information. The program will start by taking a screenshot of the HDMI video input, then it will determine the resolution (1920x1080 in our screenshot), then it will have a script/another function draw a grid over the screenshot, it will have a number at the top over each line, and a number on the left side next to each line, like a x, y graph would. The amount of horizontal and vertical lines will correspond to the resolution/8 (divided by 8), so 1920/8 for horizontal and 1080/8 for vertical (rounded to a whole number). Once the new image is labeled in a graph like fashion with the numbers it will be sent  to OpenAI's GPT-4VISION model with the users original prompt, and the response will be an x,y coordinate of where to click on the screen, or what to type.~~
