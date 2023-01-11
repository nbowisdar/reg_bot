from datetime import datetime
from typing import NamedTuple


class EmailModel(NamedTuple):
    email_id: str
    email_address: str


class EmailMessageModel(NamedTuple):
    inbox_id: str
    from_email: str
    subject: str
    body: str


class PhoneMessageModel(NamedTuple):
    from_number: str
    to_number: str
    msg: str
    received: datetime = None
