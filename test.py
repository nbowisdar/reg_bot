from run import start_simple
from src.database.tables import Email
from src.telegram.handlers.admin_handlers import inboxer

inboxer.add_in_ready("n123ew_test@.com")

if __name__ == '__main__':
    print(
    "test1@mailsipe.com" in [e.email_address for e in Email.select().where(Email.status == "in_use")]

    )
    # start_simple()
