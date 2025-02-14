import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Dialogflow Access Token from .env
DIALOGFLOW_ACCESS_TOKEN = os.getenv("DIALOGFLOW_ACCESS_TOKEN")

# API Request Details
URL = "https://dialogflow.googleapis.com/v2/projects/curry36bot-gcrb/agent/sessions/whatsapp-session:detectIntent"
HEADERS = {
    "Authorization": f"Bearer {DIALOGFLOW_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

BODY = {
    "queryInput": {
        "text": {
            "text": "Hello",
            "languageCode": "en"
        }
    }
}

# Make Request
response = requests.post(URL, headers=HEADERS, json=BODY)

# Print Response
print(response.json())
