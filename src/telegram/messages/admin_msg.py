from src.models import EmailMessageModel, EmailModel, NumberModel, PhoneMessageModel


def build_email_msg(msg: EmailMessageModel) -> str:
    return f"New message received: \n" \
           f"From :{msg.from_email}:\n" \
           f"Subject: {msg.subject}\n" \
           f"Text: \n{msg.body}"


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


# use when create new numbers
# def build_new_number_msg(number: str) -> str:
#     # if len(numbers) == 1:
#     #     return f'Number created - `{numbers[0]}`'
#     msg = f"Created new number -> {number}:"
#     for number in numbers:
#         msg += f'\n`{number}`\n'
#     return msg


# use when get a new message on number
def build_new_msg_number(msg: PhoneMessageModel) -> str:
    return f"New message received: \n" \
           f"To: {msg.to_number}\n" \
           f"Text: \n{msg.message}"
