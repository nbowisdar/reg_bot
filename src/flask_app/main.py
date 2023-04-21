from flask import Flask, render_template, g, render_template_string, request
import os
from src.email.methods import gen_email_name

print(os.getcwd())

# exit(1)

from src.email.messages import get_all_emails, get_all_messages, get_msg_by_date, get_all_emails_with_info, InboxInfo

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


@app.route("/messages")
def all_messages():
    messages = get_all_messages()
    return render_template('messages.html', messages=messages)


@app.route('/main')
def main():
    # addresses = [
    #     InboxInfo(inbox="anne.johnson766@mailsipe.com",
    #               last_msg_date="yesterday",
    #               sender="dawdw"),
    #     InboxInfo(inbox="test@mailsipe.com",
    #               last_msg_date="today",
    #               sender="dawdw")
    # ]
    addresses = get_all_emails_with_info()

    query = request.args.get('query')
    if query:
        addresses = filter(lambda addr: query in addr.inbox, addresses)
    return render_template('index.html', addresses=addresses)


# @app.route('/search')
# def search():
#     query = request.args.get('query')
#     # perform search logic here
#     return render_template('search_results.html', results=results)



@app.route('/generate_email')
def generate_email():
    return render_template('generate_emails.html', generated_email=gen_email_name())


# @app.route('/search')
# def search():
#     query = request.args.get('query')
#     # perform search logic here
#     return render_template('index.html')




# app.add_url_rule('/main', 'main', view_func=main)
# app.add_url_rule('/messages', 'messages', view_func=main)



if __name__ == "__main__":
    app.run(host='0.0.0.0')