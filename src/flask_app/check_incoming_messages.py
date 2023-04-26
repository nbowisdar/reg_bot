import time
from loguru import logger
from src.database.tables import EmailMessage
from src.email.messages import get_all_message_amount, get_sorted_messages, struct_message, get_messages

all_messages_amount = 0

cache_data_msg = [msg.received_str for msg in EmailMessage.select()]


def checking_and_save_messages(sleep=10):
    global all_messages_amount
    logger.info("pars emails started")
    while True:
        new_messages = []
        amount = get_all_message_amount()
        print(f'msg amount - {amount}')
        if amount == all_messages_amount:
            time.sleep(10)
            logger.debug("Nothing new")
            continue
        all_messages_amount = amount
        messages = get_sorted_messages()
        for msg in messages:
            if msg['Date'] in cache_data_msg:
                continue
            cache_data_msg.append(msg['Date'])
            msg = struct_message(msg)
            new_messages.append(EmailMessage(from_email=msg.from_email.replace("<", "").replace(">", ""),
                                             subject=msg.subject,
                                             body=msg.body,
                                             email=msg.email.replace("<", "").replace(">", "")))

        print(f'saved - {len(new_messages)} msg')
        EmailMessage.bulk_create(new_messages)







