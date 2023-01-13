from datetime import datetime
from typing import NamedTuple


class EmailModel(NamedTuple):
    email_id: str
    email_address: str
    note: str = None


class EmailMessageModel(NamedTuple):
    inbox_id: str
    email: str
    from_email: str
    subject: str
    body: str
    received: datetime = None


class NumberModel(NamedTuple):
    number: str
    note: str = None


class PhoneMessageModel(NamedTuple):
    from_number: str
    to_number: str
    message: str
    received: datetime = None
