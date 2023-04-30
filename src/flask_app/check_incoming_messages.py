import time
from datetime import datetime

from loguru import logger

from setup import check_ready_uber
from src.database.tables import EmailMessage, EmailSaver, Email
from src.email.messages import get_all_message_amount, get_sorted_messages, struct_message, get_messages
import shutil

# maildir_path =


all_messages_amount = 0

cache_data_msg = [msg.received_str for msg in EmailMessage.select()]
inboxer = EmailSaver()

ready_phrases = [
    ", welcome to the Uber Eats platform. You can start making money today by going online and accepting your first delivery request."
    # "ready to start delivering",
    # "you can start delivering anytime"
]


def str_time_to_timestamp(date: str) -> datetime:
    time_str = date.replace(" (UTC)", "")
    date_object = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
    return date_object


def check_ready_email(msg: EmailMessage) -> bool:
    if msg.email in inboxer.get_ready_emails():
        return False
    elif msg.email in [e.email_address for e in Email.select().where(Email.status == "in_use")]:
        return False
    for chunk in ready_phrases:
        if chunk in msg.body:

            inboxer.add_in_ready(msg.email)
            return True


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

            if check_ready_uber:
                logger.debug("checking uber now")
                ready = check_ready_email(message)
                if ready:
                    logger.info(f'{message.email} approved!')

        print(f'saved - {len(new_messages)} msg')
        EmailMessage.bulk_create(new_messages)
        shutil.rmtree('/root/Maildir')







