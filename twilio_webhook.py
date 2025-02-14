import os
import json
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Twilio Credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox Number

# Dialogflow API Config
DIALOGFLOW_PROJECT_ID = "curry36bot-gcrb"
DIALOGFLOW_LANGUAGE = "en"
DIALOGFLOW_SESSION_ID = "whatsapp-session"
DIALOGFLOW_ACCESS_TOKEN = os.getenv("DIALOGFLOW_ACCESS_TOKEN")

# Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Store user preferences (in-memory storage for simplicity)
user_data = {}

# Define Curry36 Branches
BRANCHES = {
    "1": "Curry36 - Berlin Hauptbahnhof",
    "2": "Curry36 - Zoologischer Garten",
    "3": "Curry36 - Alexanderplatz",
}

# Define Menu Items
MENU_ITEMS = {
    "1": "Currywurst - €2.90",
    "2": "Bratwurst - €3.40",
    "3": "Fries - €2.90",
    "4": "Drinks - €2.50"
}


def send_to_dialogflow(user_message, language_code):
    """ Sends user message to Dialogflow for processing """
    url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{DIALOGFLOW_SESSION_ID}:detectIntent"
    
    headers = {
        "Authorization": f"Bearer {DIALOGFLOW_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "queryInput": {
            "text": {"text": user_message, "languageCode": language_code}
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("queryResult", {}).get("fulfillmentText", "⚠️ Error: Could not process request. Please try again later.")


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """ Handles incoming WhatsApp messages """
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender_id = request.values.get("From")

    # Initialize Twilio Response
    twilio_response = MessagingResponse()

    # Check if user is new and greet them
    if sender_id not in user_data:
        user_data[sender_id] = {"language": None, "branch": None, "order": None}
        twilio_response.message("👋 Hello! Welcome to Curry36. Please select your language:\n1️⃣ English\n2️⃣ Deutsch")
        return str(twilio_response)

    # Handle Language Selection
    if user_data[sender_id]["language"] is None:
        if incoming_msg == "1":
            user_data[sender_id]["language"] = "en"
            twilio_response.message("✅ Language set to English. Please select a branch:\n1️⃣ Curry36 - Berlin Hauptbahnhof\n2️⃣ Curry36 - Zoologischer Garten\n3️⃣ Curry36 - Alexanderplatz")
        elif incoming_msg == "2":
            user_data[sender_id]["language"] = "de"
            twilio_response.message("✅ Sprache auf Deutsch eingestellt. Bitte wählen Sie eine Filiale aus:\n1️⃣ Curry36 - Berlin Hauptbahnhof\n2️⃣ Curry36 - Zoologischer Garten\n3️⃣ Curry36 - Alexanderplatz")
        else:
            twilio_response.message("⚠️ Invalid choice. Please select your language:\n1️⃣ English\n2️⃣ Deutsch")
        return str(twilio_response)

    # Handle Branch Selection
    if user_data[sender_id]["branch"] is None:
        if incoming_msg in BRANCHES:
            user_data[sender_id]["branch"] = BRANCHES[incoming_msg]
            twilio_response.message(f"🏢 You selected: {BRANCHES[incoming_msg]}\n📜 Here is the menu:\n1️⃣ Currywurst - €2.90\n2️⃣ Bratwurst - €3.40\n3️⃣ Fries - €2.90\n4️⃣ Drinks - €2.50\n\nReply with a number to order.")
        else:
            twilio_response.message("⚠️ Please select a valid branch number:\n1️⃣ Curry36 - Berlin Hauptbahnhof\n2️⃣ Curry36 - Zoologischer Garten\n3️⃣ Curry36 - Alexanderplatz")
        return str(twilio_response)

    # Handle Order Placement
    if incoming_msg in MENU_ITEMS:
        user_data[sender_id]["order"] = MENU_ITEMS[incoming_msg]
        twilio_response.message(f"✅ You selected: {MENU_ITEMS[incoming_msg]}\nWould you like to confirm your order? Reply YES or NO.")
        return str(twilio_response)

    # Handle Order Confirmation
    if incoming_msg == "yes":
        if user_data[sender_id]["order"]:
            twilio_response.message(f"🎉 Order confirmed! Your {user_data[sender_id]['order']} will be prepared at {user_data[sender_id]['branch']}. Thank you!")
            user_data[sender_id]["order"] = None  # Reset order
        else:
            twilio_response.message("⚠️ No order found. Please select an item from the menu first.")
        return str(twilio_response)

    if incoming_msg == "no":
        user_data[sender_id]["order"] = None
        twilio_response.message("❌ Order canceled. You can start again by selecting a menu item.")
        return str(twilio_response)

    # Handle Dialogflow Responses
    response_text = send_to_dialogflow(incoming_msg, user_data[sender_id]["language"])
    twilio_response.message(response_text)

    return str(twilio_response)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
