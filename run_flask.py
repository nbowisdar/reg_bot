#
#
# flask_proc = Process(target=run_flask)
# flask_proc.start()
from src.flask_app.main import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
