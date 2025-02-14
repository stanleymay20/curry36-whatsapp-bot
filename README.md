# Curry36 WhatsApp Chatbot

## 📌 Overview
The **Curry36 WhatsApp Chatbot** is an AI-powered ordering assistant designed to help customers seamlessly place food orders via WhatsApp. The bot uses **Twilio WhatsApp API** and **Dialogflow AI** to understand customer queries and process orders efficiently.

🚀 **Features:**
- 🤖 AI-powered conversation using **Dialogflow**
- 📍 Branch selection for customers
- 🍽️ Menu browsing and order confirmation
- 💬 Multi-language support (English & German)
- ✅ Order confirmation & real-time responses

## ⚙️ Installation & Setup
### **1️⃣ Clone the Repository**
```sh
 git clone https://github.com/stanleymay20/curry36-whatsapp-bot.git
 cd curry36-whatsapp-bot
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```sh
 python -m venv venv
 source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
 pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
DIALOGFLOW_ACCESS_TOKEN=your_dialogflow_token
DIALOGFLOW_PROJECT_ID=your_dialogflow_project_id
```

### **5️⃣ Run the Flask Webhook Server**
```sh
 python twilio_webhook.py
```
The bot will be available at: `http://127.0.0.1:5000`

## 💡 How to Use
1. **Join the Twilio Sandbox for WhatsApp**
   - Send `join loose-lay` to `+14155238886` via WhatsApp.
2. **Interact with the Bot**
   - Start with a greeting (`Hello` or `Hi`).
   - Select a branch location.
   - Browse the menu and place an order.
   - Confirm your order and receive a response.

## 🛠️ Troubleshooting & Common Issues
### ❌ **Twilio API Errors**
- Ensure your Twilio credentials are correctly set in `.env`.
- Check if the Twilio **Sandbox for WhatsApp** is activated.

### ❌ **Dialogflow Authentication Issues**
- Confirm that the **Google Cloud Service Account** has the correct IAM roles.
- Verify the access token using:
  ```sh
  gcloud auth application-default print-access-token
  ```

## 👨‍💻 Contributors
- **[Stanley Osei-Wusu](https://github.com/stanleymay20)** – Developer

## 📜 License
This project is **open-source** and available under the **MIT License**.

---
🚀 **Happy Ordering!**


