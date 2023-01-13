import time

from flask import Flask, request
from loguru import logger
from twilio.rest import Client
from threading import Thread
from setup import TWILIO_SID, TWILIO_TOKEN
from src.database.queries import save_message
from src.models import PhoneMessageModel

# Account SID and Auth Token from www.twilio.com/console
client = Client(TWILIO_SID, TWILIO_TOKEN)
app = Flask(__name__)

# A route to respond to SMS messages and kick off a phone call.
@app.route('/sms', methods=['POST'])
def inbound_sms():
    """View for producing the TwiML document."""

    save_message(PhoneMessageModel(
        to_number=request.form['To'],
        from_number=request.form.get("From"),
        message=request.form.get("Body")
    ))
    logger.info(f"Get new message on {request.form['To']}")
    return "ok"

#def run_flask():
    #app.run(debug=True)


def get_flask_thread() -> Thread:
    return Thread(target=app.run)



if __name__ == '__main__':
    #run_app_in_other_thread()
    #time.sleep(5)
    print(1)
