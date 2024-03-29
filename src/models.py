from datetime import datetime
from typing import NamedTuple


class EmailModel(NamedTuple):
    email_address: str
    note: str = None


class EmailMessageModel(NamedTuple):
    email: str
    from_email: str
    subject: str
    body: str
    received: str = None
    timestamp: datetime = None


class NumberModel(NamedTuple):
    number: str
    activation_id: str
    is_active: bool
    service: str


class PhoneMessageModel(NamedTuple):
    to_number: str
    message: str
    received: datetime = None
