from src.database.tables import db, Number, Email, PhoneMessage, EmailMessage
from src.models import EmailModel, PhoneMessageModel, EmailMessageModel, NumberModel
from datetime import datetime

from web_app import generate_flask_proc


def get_all_emails() -> list[list[EmailModel]]:
    resp = []
    inner = []
    emails = Email.select()
    for email in emails:
        struct_email = EmailModel(
            email_address=email.email_address,
            note=email.note)
        inner.append(struct_email)
        if len(inner) > 50 or email == emails[-1]:
            resp.append(inner)
            inner = []
    return resp


def save_new_email(email: EmailModel) -> bool:
    Email.create(
        email_address=email.email_address,
        note=email.note
    )
    return True


def is_email_exists(email: str) -> bool:
    if Email.get_or_none(email_address=email):
        return True
    return False


def is_number_exists(number: str) -> bool:
    if Number.get_or_none(number=number):
        return True
    return False


def is_active(number: str) -> bool:
    n = Number.get(number=number)
    if n.is_active:
        return True
    return False


def delete_email_from_db(inbox: str):
    query = Email.delete().where(Email.email_address == inbox)
    query.execute()


def delete_all_email_from_db():
    Email.delete().execute()


def delete_all_numbers_from_db():
    Number.delete().execute()


def save_email_message(msg: EmailMessageModel):
    email = Email.get(email_address=msg.email)
    EmailMessage.create(
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body,
        email=email
    )


def get_all_numbers() -> list[NumberModel]:
    return [NumberModel(
        number=number.number,
        activation_id=number.activation_id,
        is_active=number.is_active,
        service=number.service)
        for number in Number.select().where(Number.is_active == True)
    ]


def get_number_by_name(phone_number: str) -> NumberModel | None:
    number = Number.get_or_none(number=phone_number)
    if not number:
        return None
    return NumberModel(
        number=number.number,
        activation_id=number.activation_id,
        is_active=number.is_active,
        service=number.service)


def save_number(number: NumberModel):
    Number.create(number=number.number,
                  activation_id=number.activation_id,
                  service=number.service)


def delete_number_from_db(number: str) -> bool:
    # TODO not delete sms, low possibility of error
    query = Number.delete().where(Number.number == number)
    query.execute()
    return True


# TODO add later
def deactivate_number(number: str) -> bool:
    number = Number.get_or_none(number=number)
    if not number:
        return False
    number.is_active = False
    number.save()
    return True


def save_message(message: PhoneMessageModel) -> bool:
    number = Number.get(number=message.to_number)
    PhoneMessage.create(
        to_number=number,
        message=message.message,
    )
    return True


def get_all_email_messages(address: str) -> list[EmailMessageModel]:
    email = Email.get(email_address=address)
    return [EmailMessageModel(
        email=email.email_address,
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body)
        for msg in email.messages]


# def get_messages(limit=20):
#     retur


def check_new_email_message(inbox: str, time_from: datetime) -> EmailMessageModel | None:
    msgs = EmailMessage.select().where(
        (EmailMessage.email == inbox) & (EmailMessage.received > time_from)
    )
    if msgs:
        return EmailMessageModel(
            from_email=msgs[-1].from_email,
            email=msgs[-1].email.email_address,
            subject=msgs[-1].subject,
            body=msgs[-1].body
        )


def get_all_number_messages(number: str) -> list[PhoneMessageModel]:
    number = Number.get(number=number)
    return [PhoneMessageModel(
        to_number=msg.to_number,
        message=msg.message
    )
        for msg in number.messages]


def check_new_number_message(number: str, count: int) -> PhoneMessageModel | None:
    number = Number.get_or_none(number=number)
    if not number:
        return None
    msg = number.messages
    # msg = EmailMessage.select()  # .where()
    if len(msg) > count:
        return PhoneMessageModel(
            to_number=msg[-1].to_number,
            message=msg[-1].message
        )


if __name__ == '__main__':
    delete_number_from_db('1')
