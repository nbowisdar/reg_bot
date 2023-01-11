from src.database.tables import db, Number, Email, PhoneMessage, EmailMessage
from src.models import EmailModel, PhoneMessageModel, EmailMessageModel


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


if __name__ == '__main__':
    #save_number(number="+16089274961")
    save_new_gmail(EmailModel(
        email_id="123",
        email_address="312321"
    ))
