from flask import Flask, render_template, g

import os

print(os.getcwd())

# exit(1)

from src.email.messages import get_all_emails, get_all_messages

app = Flask(__name__)


@app.route("/message/<timestamp>")
def anon(timestamp):
    # g.inbox = inbox
    # messages = get_all_messages(inbox)
    # print(messages[0].)
    # return render_template('messages.html', messages=messages)
    return f"Date - {timestamp}"


@app.route("/inbox/<inbox>")
def anon(inbox):
    g.inbox = inbox
    messages = get_all_messages(inbox)
    # print(messages[0].)
    return render_template('messages.html', messages=messages)


@app.route('/')
def index():
    addresses = ["anne.johnson766@mailsipe.com", "test@mailsipe.com"]
    # addresses = get_all_emails()
    return render_template('index.html', addresses=addresses)


if __name__ == "__main__":
    app.run(host='0.0.0.0')