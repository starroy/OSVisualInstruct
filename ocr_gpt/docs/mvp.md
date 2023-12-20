# MVP Project Blueprint: Interactive Screen Automation Tool

## Objective
Develop an application, choosing between PyQt5 and Streamlit, that translates user prompts and screenshots into mouse movements and keyboard interactions with PyAutoGui within a 2-month timeframe.

## Key Features
- Interactive UI for inputting natural language prompts.
- Capability to capture and analyze screencapture images.
- LLM translation of natural language prompt into an action plan to complete the user's desired task or request.
- Translation of combined visual and textual input (original user prompt + LLM developed action plan) into near-real-time PyAutoGUI script actions.

## Technology Selection
- Select one primary technology for image and text interpretation: Custom OpenCV + GPT3.5-turbo/LLAMA 2, fine-tuned LLaVa + LLAMA 2, or GPT-4Vision + GPT3.5-turbo based on viability and effectiveness.

## Development Workflow
1. Environment setup with dotenv, virtualenv, and requirements.txt, and an extensible project structure and a well-thought out CI/CD pipeline, see [Python best practices template from sourcery-ai](https://github.com/sourcery-ai/python-best-practices-cookiecutter).
2. Design and implement screen capture functionality.
3. **Brainstorm and implement a method for interpreting the captured image.**
4. Integrate the chosen core technology for image and prompt processing.
5. Create PyAutoGUI commands in response to the processed inputs.
6. Develop a UI for user input and output (PyQt5 or Streamlit).
7. Test and debug the application.
8. Document the project and its usage (README.md, CONTRIBUTING.md, etc.).

## Output Format
- PyAutoGUI one-line scripts for actions like mouse clicks or keyboard hotkeys, for this MVP they will be temporarily executed with Python `eval()` at runtime.

## Proposed Execution Flow
1. User inputs a natural language prompt.
2. The application captures a screenshot of the user's screen.
3. The application interprets the screenshot and the prompt with the chosen core technologies.
4. The application send an API request to the chosen Natural Language LLM technology with the original prompt + the detailed description of the screenshot with a response of a list of actions to take.
5. The application send another API request to the chosen LLM technology to translate the previous LLM response actions to take into a list of PyAutoGUI commands to execute.
6. The application executes the PyAutoGUI commands returned by the LLM technology.



## Security Protocols
- Establish stringent input validation and code execution measures. **(TBD)**

## Deliverables
- A functional application with either a PyQt5 or Streamlit frontend.
- In-depth documentation for deployment and usage.
- Accessible and annotated source code repository.

*Further technical details and decisions will be elaborated in the project documentation.*