from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)


def get_sheet():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.environ['GOOGLE_CREDENTIALS_JSON'], scope)
    client = gspread.authorize(creds)
    sheet = client.open(os.environ['SHEET_NAME']).sheet1
    return sheet


@app.route('/sms', methods=['POST'])
def sms_reply():
    incoming = request.form.get('Body', '')
    from_number = request.form.get('From', '')

    openai.api_key = os.environ['OPENAI_API_KEY']
    prompt = (
        "You are a lead qualification assistant for a contractor business. "
        "Extract the name, service type, urgency, and address from this message:\n\n"
        f"{incoming}\n"
    )
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
    )
    info = response['choices'][0]['message']['content']

    sheet = get_sheet()
    sheet.append_row([from_number, incoming, info])

    reply = MessagingResponse()
    reply.message("Thanks for reaching out! We'll get back to you shortly.")
    return str(reply)


if __name__ == '__main__':
    app.run(debug=True)
