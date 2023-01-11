from datetime import datetime
from typing import NamedTuple


class GmailModel(NamedTuple):
    mail: str
    password: str
    cookies: str
    number: str


class PhoneMessageModel(NamedTuple):
    from_number: str
    to_number: str
    msg: str
    received: datetime = None
