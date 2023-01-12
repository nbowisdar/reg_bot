from src.database.tables import db, Number, Email, PhoneMessage, EmailMessage
from src.models import EmailModel, PhoneMessageModel, EmailMessageModel
from datetime import datetime

def save_new_email(email: EmailModel) -> bool:
    Email.create(
        email_id=email.email_id,
        email_address=email.email_address,
    )
    return True


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


def check_new_message(from_time: datetime) -> EmailMessageModel | None:
    msg = EmailMessage.select().where(from_time < EmailMessage.received)

    if msg:
        return EmailMessageModel(
            from_email=msg[0].from_email,
            email=msg[0].emal.email_address,
            inbox_id=msg[0].inbox_id,
            subject=msg[0].subject,
            body=msg[0].body
        )


if __name__ == '__main__':
    c = datetime.now()
    check_new_message(c)
    print('1')
