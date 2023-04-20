import multiprocessing as ml
import time
from flask import Flask, render_template, render_template_string
app = Flask(__name__)

outer_html = "Error"


@app.route('/message')
def index():
    return render_template_string(outer_html)


def run_flask(html):
    global outer_html
    outer_html = html
    app.run(host='0.0.0.0', port=5000)


def generate_flask_proc(html) -> ml.Process:
    return ml.Process(target=run_flask, args=(html,))


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


