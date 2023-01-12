from src.database.tables import db, Number, Email, PhoneMessage, EmailMessage
from src.models import EmailModel, PhoneMessageModel, EmailMessageModel
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


def delete_mail(mail_id: str) -> bool:
    gmail = Email.get(mail_id=mail_id)
    gmail.delete().execute()
    return True


def save_email_message(msg: EmailMessageModel):
    email = Email.get(email_id=msg.inbox_id)
    EmailMessage.create(
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body,
        email=email
    )


def save_number(number: str) -> bool:
    if number[0] != "+":
        raise ValueError("Wrong number! Support only +1...")
    elif len(number) != 12:
        raise ValueError("lents of number must be -> +110")
    Number.create(number=number)
    return True


def delete_number(number: str) -> bool:
    number = Number.get(number=number)
    number.delete().execute()
    return True


def save_message(message: PhoneMessageModel) -> bool:
    number = Number.get(number=message.to_number)
    PhoneMessage.create(
        to_number=number,
        from_number=message.from_number,
        message=message.msg,
    )
    return True


def get_all_messages(inbox_id) -> list[EmailMessageModel]:
    email = Email.get(email_id=inbox_id)
    return [EmailMessageModel(
        inbox_id=email.email_id,
        email=email.email_address,
        from_email=msg.from_email,
        subject=msg.subject,
        body=msg.body)
        for msg in email.messages]


def check_new_message(inbox_id: str, count: int) -> EmailMessageModel | None:
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


if __name__ == '__main__':
    e = "0b4647dc-cc51-4f17-89f0-a66aa72ba7ce"
    x = get_all_messages(e)
    print(x)

