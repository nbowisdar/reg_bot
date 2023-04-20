import asyncio
import multiprocessing as ml
import time
from flask import Flask, render_template, render_template_string
from flask_sslify import SSLify

from src.config import message_live_sec

app = Flask(__name__)
sslify = SSLify(app)

outer_html = "Error"


@app.route('/message')
def index():
    return render_template_string(outer_html)


def run_flask(html):
    global outer_html
    outer_html = html
    # app.run(debug=True, )
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))





if __name__ == '__main__':
    app.run


def generate_flask_proc(html) -> ml.Process:
    return ml.Process(target=run_flask, args=(html,))


async def run_temp_flask(html):
    # start = time.perf_counter()
    proc = generate_flask_proc(html)
    proc.start()
    await asyncio.sleep(message_live_sec)
    proc.terminate()
    print("message expired")



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


