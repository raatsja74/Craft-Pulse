# Contractor Lead Qualification & Booking Assistant

This sample Flask application demonstrates the core workflow of the Craft Pulse AI assistant. It receives inbound SMS messages via Twilio, uses OpenAI to extract lead details, and stores them in a Google Sheet.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a Google service account and export the path to the credentials JSON file:
   ```bash
   export GOOGLE_CREDENTIALS_JSON=path/to/credentials.json
   export SHEET_NAME="Your Leads Sheet"
   ```
3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```
4. Configure Twilio to send incoming SMS webhooks to `/sms` on your running Flask server.

Run the development server:
```bash
python app.py
```

This is a minimal example meant as a starting point. You can extend it with voice call handling, appointment booking via Google Calendar, and additional follow-up logic.
