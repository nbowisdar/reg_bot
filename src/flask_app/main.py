from flask import Flask, render_template, g, render_template_string, request, redirect, session
import os

from setup import TEMP_PASSWORD
from src.email.methods import gen_email_name
print(os.getcwd())
from src.email.messages import get_all_emails, get_all_messages, get_msg_by_date, get_all_emails_with_info, InboxInfo

app = Flask(__name__)
app.secret_key = "dwadawd123123dawdwd23123dahhtyhr423"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if "password" in session.keys():
        if session['password'] == TEMP_PASSWORD:
            return redirect('\main')

    if request.method == "POST":
        password = request.form['password']
        if password == TEMP_PASSWORD:
            session['password'] = TEMP_PASSWORD
            return redirect('/protected')
        else:
            return 'Incorrect password'
    return render_template('login.html')


@app.route('/protected')
def protected():
    # Check if user has entered correct password
    if 'password' not in session or session['password'] != TEMP_PASSWORD:
        return redirect('/password')

    return redirect('/main')


@app.before_request
def require_password():
    if 'password' not in session or session['password'] != TEMP_PASSWORD:
        if request.path != '/login' and request.path != "/protected":
            return redirect('/login')


@app.route("/inbox/message/<date>")
def show_msg_redirect(date):
    return redirect("/message/" + date)
    # msg = get_msg_by_date(date)
    # html = msg.body
    # return render_template_string(html)


@app.route("/message/<date>")
def show_msg(date):
    msg = get_msg_by_date(date)
    html = msg.body
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


@app.route("/")
def r1():
    return redirect('/emails')


@app.route("/main")
def r2():
    return redirect('/inbox/emails')


@app.route('/emails')
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
    return render_template('emails.html', addresses=addresses)


@app.route('/generate_email')
def generate_email():
    return render_template('generate_emails.html', generated_email=gen_email_name())



# app.add_url_rule('/main', 'main', view_func=main)
# app.add_url_rule('/messages', 'messages', view_func=main)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)