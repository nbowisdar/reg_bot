from pprint import pprint

from flask import Flask, request
from loguru import logger
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import urllib

from src.database.queries import save_message
from src.models import PhoneMessageModel

# Account SID and Auth Token from www.twilio.com/console
client = Client('AC9ae53af1405032a48bb293c8aa8b6605', '462dbb5dc73e369c03b8c0d18bc92e1c')
app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    print(request.values)
    return str("hello")


# A route to respond to SMS messages and kick off a phone call.
@app.route('/sms', methods=['POST'])
def inbound_sms():
    """View for producing the TwiML document."""

    save_message(PhoneMessageModel(
        to_number=request.form['To'],
        from_number=request.form.get("From"),
        msg=request.form.get("Body")
    ))
    logger.info(f"Get new message on {request.form['To']}")
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
