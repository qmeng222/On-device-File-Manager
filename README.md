## On-device-File-Manager

### Introduction:

- Description: A self-organizing file manager that uses Nexa SDK and the Phi-3.5 model to automatically summarize, classify, rename, and organize files based on their content.
- Highlights:
- Tech stack: GPT, Python
- Workflow:
- Demo:

### Setup:

1. Create & activate the virtual environment:
   ```
   conda create --name file_manager python=3.10
   conda activate file_manager
   ```
2. Upgrade the pip package manager to the latest version within the venv:
   `python -m pip install --upgrade pip`
3. Install required packages:
   - Install Nexa SDK: `pip install nexaai`
4. Generate a snapshot of the installed packages and their versions to the requirements.txt file (or overwrite the txt file): `pip freeze > requirements.txt`

### Usage:

- Clone using the web URL: https://github.com/qmeng222/On-device-File-Manager.git
- Install all the packages and their respective versions specified in the requirements.txt file: `pip install -r requirements.txt`

### Resources:

1. [Nexa SDK](https://pypi.org/project/nexaai/)
2. [Nexa Model Hub | Phi-3.5-mini-instruct](https://nexaai.com/microsoft/Phi-3.5-mini-instruct/gguf-fp16/readme)
