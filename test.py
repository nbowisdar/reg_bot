from run import start_simple
from src.telegram.handlers.admin_handlers import inboxer

inboxer.add_in_ready("n123ew_test@.com")

if __name__ == '__main__':
    start_simple()
