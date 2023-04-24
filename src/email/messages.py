import mailbox
from datetime import datetime
from pprint import pprint
from typing import NamedTuple

import loguru
from bs4 import BeautifulSoup

from src.models import EmailMessageModel

# Define the path to the Maildir mailbox
mailbox_path = '/root/Maildir'


def get_sorted_messages():
    maildir = mailbox.Maildir(mailbox_path)
    return sorted(maildir, key=lambda message: datetime.fromtimestamp(float(message.get_date())),
                  reverse=True)


def get_all_message_amount(inbox: str) -> int:
    c = 0
    maildir = mailbox.Maildir(mailbox_path)
    for message in maildir:
        if inbox == message['To']:
            c += 1
    return c


def struct_message(message) -> EmailMessageModel:
    recipient = message['To']  # .replace("<", "", ">", "")
    date_info = message['Date']
    sender = message['From']
    subject = message['Subject']
    if message.is_multipart():
        # If the message has multiple parts, iterate over them
        content = []
        for part in message.get_payload():
            charset = part.get_content_charset() or 'utf-8'
            try:
                content.append(part.get_payload(decode=True).decode(charset))
            except AttributeError:
                pass
        content = '\n'.join(content)
    else:
        # If the message has a single part, just get its content
        charset = message.get_content_charset() or 'utf-8'
        content = message.get_payload(decode=True).decode(charset)
    return EmailMessageModel(
        email=recipient,
        from_email=sender,
        subject=subject,
        body=content,
        received=date_info,
        # timestamp=datetime.fromtimestamp(float(message.get_date()))
    )


def get_all_emails() -> set[str]:
    messages = get_sorted_messages()
    resp = set()
    for msg in messages:
        resp.add(msg["TO"])  #  .replace("<", "").replace(">", ""),)
    return resp


class InboxInfo(NamedTuple):
    inbox: str
    last_msg_date: str
    sender: str


def get_all_emails_with_info() -> list[InboxInfo]:
    messages = get_sorted_messages()
    resp = []
    emails = []
    for msg in messages:
        if msg["TO"] not in emails:
            emails.append(msg["TO"])
            resp.append(
                InboxInfo(
                    inbox=msg["TO"],  #  .replace("<", "").replace(">", ""),
                    last_msg_date=msg["Date"],
                    sender=msg['From']
                )
            )
    return resp


def get_msg_by_date(date: str) -> EmailMessageModel:
    for msg in get_all_messages():
        if msg.received == date:
            return msg


def get_all_messages(inbox: str = None) -> list[EmailMessageModel]:
    messages = get_sorted_messages()
    resp = []
    for msg in messages:
        if msg['To'] == inbox or not inbox:
            resp.append(struct_message(msg))
    return resp


def get_last_msg(inbox: str) -> EmailMessageModel:
    messages = get_sorted_messages()
    for message in messages:
        recipient = message['To']
        if inbox != recipient:
            continue
        return struct_message(message)

        # date_info = message['Date']
        # sender = message['From']
        # subject = message['Subject']
        # # if "SECURITY information for" in subject:
        # #     continue
        # if message.is_multipart():
        #     # If the message has multiple parts, iterate over them
        #     content = []
        #     for part in message.get_payload():
        #         charset = part.get_content_charset() or 'utf-8'
        #         content.append(part.get_payload(decode=True).decode(charset))
        #     content = '\n'.join(content)
        # else:
        #     # If the message has a single part, just get its content
        #     charset = message.get_content_charset() or 'utf-8'
        #     content = message.get_payload(decode=True).decode(charset)
        #
        #
        # return EmailMessageModel(
        #     email=recipient,
        #     from_email=sender,
        #     subject=subject,
        #     body=content
        # )
