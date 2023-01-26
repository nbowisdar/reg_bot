from src.models import EmailMessageModel, EmailModel, NumberModel, PhoneMessageModel


def build_email_msg(msg: EmailMessageModel) -> str:
    message = msg.body.replace("\n\n", '').replace('\xa0', '')
    words = message.split(' ')
    x = [word for word in words if word != " " and word != '']
    message = " ".join(x).replace("\n", '')
    return f"New message received: \n" \
           f"From :{msg.from_email}:\n" \
           f"Subject: {msg.subject}\n" \
           f"Text: \n{message}"


def build_all_emails_msg(emails: list[EmailModel]) -> str:
    if not emails:
        return "You haven't created any emails"
    msg = ""
    for email in emails:
        msg += f"`{email.email_address}`\n"
        if email.note:
            msg += f'{email.note}\n'
        msg += '\n'
    return msg


def build_new_emails_msg(emails: list[str]) -> str:
    if len(emails) == 1:
        return f'Email created - `{emails[0]}`'
    msg = f"Created {len(emails)} new emails:"
    for email in emails:
        msg += f'\n`{email}`\n'
    return msg


def build_all_numbers_msg(numbers: list[NumberModel]) -> str:
    if not numbers:
        return "You haven't created any numbers"
    msg = "Your active numbers:\n"
    for number in numbers:
        msg += f"Google -> `+{number.number}`\n"
    return msg


def balance_message(balance: str) -> str:
    return f"Your balance - *{balance}*\n" \
           f"Top up balance:\n " \
           f"`TT2Qx3LkQk4r5XTa9hnYTxuqbN5BCghBEe` USDT-TRX\n" \
           f"BTC -> `3BoRxs8xywdYA5NUs5MttXUZ2kkRKkzxJM`\n\n" \
           f"⚡Attention! The minimum one transaction is 500 rubles\n" \
           f"⚡Transaction less than 500 rubles will not be credited to your account!\n\n" \
           f"After payment, the cryptocurrency will be converted into rubles and credited to your account\n" \
           f"This deposit address is assigned to you, you can use it for deposits at any time"


# use when get a new message on number
def build_new_msg_number(msg: PhoneMessageModel) -> str:
    message = msg.message.replace("\n\n", '').replace('\xa0', '')
    words = message.split(' ')
    x = [word for word in words if word != " " and word != '']
    message = " ".join(x)
    return f"New message received: \n" \
           f"To: {msg.to_number}\n" \
           f"Text: \n{message}"
