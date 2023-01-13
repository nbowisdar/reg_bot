from src.database.tables import db, Number, Email, PhoneMessage, EmailMessage
from src.models import EmailModel, PhoneMessageModel, EmailMessageModel, NumberModel
from datetime import datetime


def get_all_emails() -> list[EmailModel]:
    return [EmailModel(
        email_id=email.id,
        email_address=email.email_address,
        note=email.note
    ) for email in Email.select()]


def save_new_email(email: EmailModel) -> bool:
    Email.create(
        email_id=email.email_id,
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


def delete_email_from_db(email_id: str):
    query = Email.delete().where(Email.email_id == email_id)
    query.execute()


def save_email_message(msg: EmailMessageModel):
    email = Email.get(email_id=msg.inbox_id)
    EmailMessage.create(
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body,
        email=email
    )


def get_all_numbers() -> list[NumberModel]:
    return [NumberModel(
        number=number.number,
        note=number.note)
        for number in Number.select()
    ]


def save_number(number: str) -> bool:
    if number[0] != "+":
        raise ValueError("Wrong number! Support only +1...")
    elif len(number) != 12:
        raise ValueError("lents of number must be -> +110")
    Number.create(number=number)
    return True


def delete_number_from_db(number: str):
    query = Number.delete().where(Number.number == number)
    query.execute()


def save_message(message: PhoneMessageModel) -> bool:
    number = Number.get(number=message.to_number)
    PhoneMessage.create(
        to_number=number,
        from_number=message.from_number,
        message=message.message,
    )
    return True


def get_all_email_messages(inbox_id) -> list[EmailMessageModel]:
    email = Email.get(email_id=inbox_id)
    return [EmailMessageModel(
        inbox_id=email.email_id,
        email=email.email_address,
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body)
        for msg in email.messages]


def check_new_email_message(inbox_id: str, count: int) -> EmailMessageModel | None:
    msg = Email.get(email_id=inbox_id).messages
    # msg = EmailMessage.select()  # .where()
    if len(msg) > count:
        return EmailMessageModel(
            from_email=msg[-1].from_email,
            email=msg[-1].email.email_address,
            inbox_id=msg[-1].email.email_id,
            subject=msg[-1].subject,
            body=msg[-1].body
        )


def get_all_number_messages(number: str) -> list[PhoneMessageModel]:
    number = Number.get(number=number)
    return [PhoneMessageModel(
        from_number=msg.from_number,
        to_number=msg.to_number,
        message=msg.message
    )
        for msg in number.messages]


def check_new_number_message(number: str, count: int) -> PhoneMessageModel | None:
    msg = Number.get(number=number).messages
    # msg = EmailMessage.select()  # .where()
    if len(msg) > count:
        return PhoneMessageModel(
            from_number=msg[-1].from_number,
            to_number=msg[-1].to_number,
            message=msg[-1].message
        )


if __name__ == '__main__':
    delete_number_from_db('1')
