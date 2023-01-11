from src.database.tables import db, Number, Gmail, PhoneMessage
from src.models import GmailModel, PhoneMessageModel


def save_new_gmail(gmail: GmailModel) -> bool:
    number = Number.get_or_none(number=gmail.number)
    if not number:
        raise ValueError(f"Number {gmail.number} - doesn't exist")
    Gmail.create(
        number=number,
        mail=gmail.mail,
        password=gmail.password,
        cookies=gmail.cookies
    )
    return True


def delete_gmail(mail: str) -> bool:
    gmail = Gmail.get(mail=mail)
    gmail.delete().execute()
    return True


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


if __name__ == '__main__':
    save_number(number="+16089274961")
    # x = "+11234567890"
    #
    # message = PhoneMessageModel(
    #     from_number="123213",
    #     to_number=x,
    #     msg="Hello"
    # )
    #
    # save_message(message=message)

    # save_number(number=x)
    # g = GmailModel(
    #     mail="123",
    #     password="123",
    #     number=x,
    #     cookies="123"
    # )
    # gmail = save_new_gmail(g)
