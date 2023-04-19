import mailbox
from datetime import datetime
from pprint import pprint
from typing import NamedTuple

from src.models import EmailMessageModel

# Define the path to the Maildir mailbox
mailbox_path = '/home/incoming/Maildir'

# Open the Maildir mailbox
maildir = mailbox.Maildir(mailbox_path)


messages = list(maildir)
messages.reverse()


def get_all_message_amount(inbox: str) -> int:
    c = 0
    for message in messages:
        recipient = message['To']
        if inbox == recipient:
            c += 1
    return c


def get_last_msg(inbox: str) -> EmailMessageModel:
    for message in messages:
        recipient = message['To']
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

        return EmailMessageModel(
            email=recipient,
            from_email=sender,
            subject=subject,
            body=content
        )