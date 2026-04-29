# BrightWay_Workspace_22_4_2026
Second homework from Brightway course - Building good architecture for AI Agent development, and building Semantic FAQ app using embeddings

$\color{red}{\text{This Setup procedure is exactly the same as previous homework}}$

## You will need to make a file named .env and copy this into it:
> GEMINI_API_KEY=your_api_key_placeholder
> 
> GEMINI_MODEL_NAME=gemini-2.5-flash
> 
> GEMINI_TEMPERATURE=0.7
> 
Then provide it with your gemini api key, and keep it secret in there!



## Setup — Virtual Environment & Dependencies
Open a terminal ( powershell ) inside project folder and run these commands in order:

Step 1 — create a virtual environment
> python -m venv venv
 if the above does not work, try:
> py -3.11 -m venv venv

Step 2 — activate the virtual environment
Windows (PowerShell):
> venv\Scripts\Activate.ps1

macOS / Linux:
> source venv/bin/activate
> 
Your terminal prompt should now show (venv) at the start. To deactivate the environment later, run: 'deactivate'

Step 3 — upgrade pip
> python -m pip install --upgrade pip

Step 4 — install dependencies
> pip install -r requirements.txt
