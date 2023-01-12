from src.models import EmailMessageModel, EmailModel


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
