from flask import Flask, render_template, g, render_template_string

import os

print(os.getcwd())

# exit(1)

from src.email.messages import get_all_emails, get_all_messages, get_msg_by_date

app = Flask(__name__)


@app.route("/inbox/message/<date>")
def show_msg(date):
    msg = get_msg_by_date(date)
    html = msg.body
    # messages = get_all_messages(inbox)
    # print(messages[0].)
    # return render_template('messages.html', messages=messages)
    return render_template_string(html)


@app.route("/inbox/<inbox>")
def show_messages(inbox):
    g.inbox = inbox
    messages = get_all_messages(inbox)
    # print(messages[0].)
    return render_template('messages.html', messages=messages)


@app.route('/')
def main():
    addresses = ["anne.johnson766@mailsipe.com", "test@mailsipe.com"]
    # addresses = get_all_emails()
    return render_template('index.html', addresses=addresses)


app.add_url_rule('/main', 'main', view_func=main)



if __name__ == "__main__":
    app.run(host='0.0.0.0')