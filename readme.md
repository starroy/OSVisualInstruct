# OSVisualInstruct


Recreating a Windows OS version of w/out access to the target OS (aside from HDMI, and USB devices such as keyboard/mouse):
https://www.youtube.com/watch?v=QXJ7rImz-Wk

[AI To Control Computer](https://www.youtube.com/watch?v=QXJ7rImz-Wk)

### Foreseeable challenges using the current resources and technologies for the POC mainly come from [limitations](https://platform.openai.com/docs/guides/vision#:~:text=While%20GPT%2D4,submission%20of%20CAPTCHAs.), in the OpenAI Vision model:
Big text: Enlarge text within the image to improve readability, but avoid cropping important details.
Visual elements: The model may struggle to understand graphs or text where colors or styles like solid, dashed, or dotted lines vary.
Spatial reasoning: The model struggles with tasks requiring precise spatial localization, such as identifying chess positions.
Rotation: The model may misinterpret rotated / upside-down text or images.

### Potential Solutions to Foreseeable challenges
> Chunk the screenshot into large sections or grids and have the Vision Model identify the portion of the image the user is talking about recursively until the model is comfortable it has found the general area the user is refering to, use that small chunked section to calculate the coordinates that the model/api should return.

#### Example

> The below example may need to have larger labels to work better
```py
from openai import OpenAI

# Omitted steps:
# Take screenshot
# Chunk screenshot into x amount of sections
# Create a grid overlayed against each chunked screenshot with x,y labels based off the total resolution of the original screenshot, use as large of a font size for the labels as possible
# Save a copy of and provide a link to the model with each of the chunked screenshots
# After the model returns a x,y tuple, feed the x,y tuple with the original prompt back into gpt3.5-turbo with an expected one-line response of the pyautogui code to be run to complete the users action:
# Example Prompt: "Write out a one-liner with pyautogui that performs the action based on the original prompt, and the determined x,y coordinates: 'Original Prompt: What are the x,y coordinates for the "X"/close button for my Windows Explorer application?', 'Vision Assistant Answer: (1420, 680)'"

client = OpenAI()
USER_PROMPT = "What are the x,y coordinates for the "X"/close button for my Windows Explorer application?"
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "system",
            "content": "You are a helpful assistant who analyzes screenshots from a computer that may have various applications or windows open, you expertly analyze the images provided and detail which one had what the user was looking for, you will respond with your thought process, which image contained what the user was referring to, and finally a tuple of the X,Y coordinates using the overlayed grid and x and y labels. Helpful Tip: First determine the application/location/task they might be referring to and use that to determine which image contains what they are referring to, then determine the exact spot of the image they want and respond with the X,Y coordinates."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": "https://github.com/0xDeadcell/OSVisualInstruct/blob/main/img1topleft.PNG?raw=true",
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/0xDeadcell/OSVisualInstruct/blob/main/img2topright.PNG?raw=true",
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/0xDeadcell/OSVisualInstruct/blob/main/img3bottomleft.PNG?raw=true",
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/0xDeadcell/OSVisualInstruct/blob/main/img4bottomright.PNG?raw=true",
                },
                
                {
                    "type": "text",
                    "text": USER_PROMPT,
                }
            ],
        }
    ],
    max_tokens=750,
)
print(response.choices[0])
```


### Resources:

https://github.com/haotian-liu/LLaVA (Potential Open Source Alternative to Vision, but will likely need to be fine-tuned for this use case)

https://openai.com/blog/new-models-and-developer-products-announced-at-devday
https://platform.openai.com/docs/guides/vision
https://cookbook.openai.com/examples/gpt_with_vision_for_video_understanding
```py
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                    "type": "image_url",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])
```


