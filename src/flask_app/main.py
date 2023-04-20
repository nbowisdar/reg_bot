from flask import Flask, render_template

import os

print(os.getcwd())

# exit(1)

from src.email.messages import get_all_emails

app = Flask(__name__)

@app.route('/emails')
def index():
    return render_template('index.html', addresses=get_all_emails())


if __name__ == "__main__":
    app.run(host='0.0.0.0')