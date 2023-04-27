from datetime import timedelta, datetime
from pprint import pprint

from flask import Flask, render_template, g, render_template_string, request, redirect, session
import os

from loguru import logger

from setup import TEMP_PASSWORD
from src.database.tables import Email, EmailMessage, EmailSaver
from src.email.methods import gen_email_name
print(os.getcwd())
from src.email.messages import get_all_emails, get_all_messages, get_msg_by_date, get_all_emails_with_info, InboxInfo

app = Flask(__name__)
app.secret_key = "dwadawd123123dawdwd23123dahhtyhr423"


inboxer = EmailSaver()


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


@app.route("/message/<id>")
def show_msg(id):
    # msg = get_msg_by_date(date)
    msg = EmailMessage.get_by_id(id)
    html = msg.body
    return render_template_string(html)


@app.route("/inbox/<inbox>")
def show_messages(inbox):
    messages = EmailMessage.select()\
        .order_by(EmailMessage.id.desc())\
        .where(EmailMessage.email == inbox)
    return render_template('messages.html', messages=messages, with_drop=True)


@app.route("/messages")
def all_messages():
    query = request.args.get('query')
    if query:
        print(query)
        messages = EmailMessage.select().order_by(EmailMessage.received.desc())
        messages = filter(lambda addr: query in addr.body, messages)
        with_drop = False
    else:
        messages = EmailMessage.select()\
            .where(
            (EmailMessage.received > datetime.now() - timedelta(minutes=30)) & (EmailMessage.received < datetime.now())
        )\
            .order_by(EmailMessage.received.desc())
        with_drop = False

    return render_template('messages.html', messages=messages, with_drop=with_drop)


@app.route("/")
def r1():
    return redirect('/messages')


@app.route("/main")
def r2():
    return redirect('/emails')


@app.route('/emails')
def main():
    emails = []
    messages = []
    print(f"amount from main - {len(EmailMessage.select())}")
    for msg in EmailMessage.select().order_by(EmailMessage.received.desc()):
        if msg.email in emails:
            continue
        emails.append(msg.email)
        messages.append(msg)
    query = request.args.get('query')
    if query:
        messages = filter(lambda addr: query in addr.email, messages)

    messages = inboxer.filter_deleted(messages)
    return render_template('emails.html', messages=messages)


@app.route('/inbox/delete_email')
def delete_email():
    inbox = request.args.get('email')
    if inbox:
        inboxer.delete_email(inbox)
        logger.info(f"deleted - {inbox}")
    return redirect('/emails')


@app.route('/generate_email')
def generate_email():
    return render_template('generate_emails.html', generated_email=gen_email_name())



# app.add_url_rule('/main', 'main', view_func=main)
# app.add_url_rule('/messages', 'messages', view_func=main)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)