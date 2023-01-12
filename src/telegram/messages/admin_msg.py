from src.models import EmailMessageModel


def build_email_msg(msg: EmailMessageModel) -> str:
    return f"New message from {msg.from_email}:" \
          f"Subject: {msg.subject}\n" \
          f"Text: \n{msg.body}"



