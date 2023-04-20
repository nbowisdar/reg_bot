import mailbox
from datetime import datetime
from pprint import pprint
from typing import NamedTuple

import loguru
from bs4 import BeautifulSoup

from src.models import EmailMessageModel

# Define the path to the Maildir mailbox
mailbox_path = '/root/Maildir'

# Open the Maildir mailbox
# maildir = mailbox.Maildir(mailbox_path)





def get_all_message_amount(inbox: str) -> int:
    c = 0
    maildir = mailbox.Maildir(mailbox_path)
    for message in maildir:
        if inbox == message['To']:
            c += 1
    return c


def get_last_msg(inbox: str) -> EmailMessageModel:
    maildir = mailbox.Maildir(mailbox_path)
    messages = sorted(maildir, key=lambda message: datetime.datetime.fromtimestamp(float(message.get_date())))
    pprint([i['Subject'] for i in messages])
    messages.reverse()
    # pprint(messages)
    for message in messages:
        recipient = message['To']
        loguru.logger.info(f"recip - {recipient}")
        loguru.logger.info(f"waiting - {inbox}")
        if inbox != recipient:
            continue
        date_info = message['Date']
        sender = message['From']
        subject = message['Subject']
        # if "SECURITY information for" in subject:
        #     continue
        if message.is_multipart():
            # If the message has multiple parts, iterate over them
            content = []
            for part in message.get_payload():
                charset = part.get_content_charset() or 'utf-8'
                content.append(part.get_payload(decode=True).decode(charset))
            content = '\n'.join(content)
        else:
            # If the message has a single part, just get its content
            charset = message.get_content_charset() or 'utf-8'
            content = message.get_payload(decode=True).decode(charset)



        # soup = BeautifulSoup(content, 'html.parser')
        # divs = soup.find_all('div', {'dir': 'ltr'})
        # # soup.get
        #
        # text_list = [div.text for div in divs]
        # print(text_list)
        #
        #
        # content = "\n".join(text_list)

        return EmailMessageModel(
            email=recipient,
            from_email=sender,
            subject=subject,
            body=content
        )
