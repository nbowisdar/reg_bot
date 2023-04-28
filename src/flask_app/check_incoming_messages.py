import time
from datetime import datetime

from loguru import logger
from src.database.tables import EmailMessage, EmailSaver
from src.email.messages import get_all_message_amount, get_sorted_messages, struct_message, get_messages
import shutil

# maildir_path =


all_messages_amount = 0

cache_data_msg = [msg.received_str for msg in EmailMessage.select()]
inboxer = EmailSaver()

ready_phrases = [
    "ready to start delivering",
    "you can start delivering anytime"
]


def str_time_to_timestamp(date: str) -> datetime:
    time_str = date.replace(" (UTC)", "")
    date_object = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
    return date_object


def check_ready_email(msg: EmailMessage):
    if msg.email in inboxer.get_ready_emails():
        return
    # elif msg.email in inboxer.
    for chunk in ready_phrases:
        if chunk in msg.body:
            inboxer.add_in_ready(msg.email)
            return


def checking_and_save_messages(sleep=10):
    global all_messages_amount
    logger.info("pars emails started")
    while True:
        new_messages = []
        amount = get_all_message_amount()
        print(f'msg amount - {amount}')
        if amount == all_messages_amount:
            time.sleep(15)
            logger.debug("Nothing new")
            continue
        all_messages_amount = amount
        messages = get_sorted_messages()
        if not messages:
            time.sleep(15)
            logger.debug("Nothing new")
            continue
        for msg in messages:
            if msg['Date'] in cache_data_msg:
                continue
            cache_data_msg.append(msg['Date'])
            msg = struct_message(msg)
            received = str_time_to_timestamp(msg.received)
            message = EmailMessage(from_email=msg.from_email.replace("<", "").replace(">", ""),
                                             subject=msg.subject,
                                             body=msg.body,
                                             received=received,
                                             received_str=received.strftime('%Y-%m-%d %H:%M'),
                                             email=msg.email.replace("<", "").replace(">", ""))
            new_messages.append(message)
            check_ready_email(message)

        print(f'saved - {len(new_messages)} msg')
        EmailMessage.bulk_create(new_messages)
        shutil.rmtree('/root/Maildir')







