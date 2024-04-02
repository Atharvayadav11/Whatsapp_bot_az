import asyncio
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

app = Flask(__name__)

async def send_initial_message():
    return "Hello! May I know your username?"

async def handle_username(username):
    print("Username:", username)
    return "Please let me know in which category you want to add the meal?\nOptions:\n1. Breakfast\n2. Lunch\n3. Evening Snacks\n4. Dinner"

async def handle_meal_category(meal_category):
    print("Meal Category:", meal_category)
    return "Please share the name of the dish."

async def handle_message(incoming_msg, is_username=False):
    incoming_msg = incoming_msg.strip().lower()
    if incoming_msg == 'hello aarogyazen':
        return await send_initial_message(), True
    elif is_username:
        return await handle_username(incoming_msg), False

    elif incoming_msg.isdigit() in ['1', '2', '3', '4']:
        return await handle_meal_category(incoming_msg), False
    else:
        return "I'm sorry, I didn't understand that. Please follow the instructions.", False

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
async def sms_reply():
    incoming_msg = request.values.get('Body', '')
    
    if 'username' not in request.values:
        response_msg, is_username = await handle_message(incoming_msg, is_username=True)
    else:
        response_msg, is_username = await handle_message(incoming_msg)

    resp = MessagingResponse()
    resp.message(response_msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
