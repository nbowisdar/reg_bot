import multiprocessing
import time
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate_flask_proc() -> multiprocessing.Process:
    return multiprocessing.Process(target=run_flask)


def run_flask():
    app.run(host='0.0.0.0', port=5000)


def tests():
    page_proc = generate_flask_proc()
    page_proc.start()
    time.sleep(5)
    print('termitate')
    page_proc.terminate()
    time.sleep(10)
    print('start again')
    page_proc = generate_flask_proc()
    page_proc.start()

# if __name__ == '__main__':


