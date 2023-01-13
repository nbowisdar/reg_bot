import mailslurp_client
from bs4 import BeautifulSoup
from mailslurp_client import ApiException
from threading import Thread

from setup import MAILSLURP_KEY
from src.database.queries import save_new_email, save_email_message
from src.models import EmailModel, EmailMessageModel

#key = "61ecd7525d62030537f01d073de497c7a5fa958ebd19d597ec04083fef9e473f"

configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = MAILSLURP_KEY


# create new inbox
def create_inbox(note=None) -> str:
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        inbox = api_instance.create_inbox()
        save_new_email(EmailModel(
            email_id=inbox.id,
            email_address=inbox.email_address,
            note=note
        ))
        return inbox.email_address


def create_few_inboxes(amount=1, note=None) -> list[str]:
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        res = []
        for _ in range(amount):
            inbox = api_instance.create_inbox()
            save_new_email(EmailModel(
                email_id=inbox.id,
                email_address=inbox.email_address,
                note=note
            ))
            res.append(inbox.email_address)
        return res


def get_email(inbox_id: str):
    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        return inbox_controller.get_inbox(inbox_id=inbox_id)


def delete_email_on_site(inbox_id: str):
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        api_instance.delete_inbox(inbox_id=inbox_id)


def _receive_msg(inbox_id) -> EmailMessageModel:
    #try:
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create two inboxes for testing
        waiter = mailslurp_client.WaitForControllerApi(api_client)
        msg = waiter.wait_for_latest_email(inbox_id=inbox_id, timeout=360000, unread_only=True)
        soup = BeautifulSoup(msg.body, "html.parser")
        body = soup.div.text
        return EmailMessageModel(
            from_email=msg._from,
            email=msg.to,
            inbox_id=inbox_id,
            subject=msg.subject,
            body=body
        )


def _receive_and_save(inbox_id):
    try:
        msg = _receive_msg(inbox_id)
        save_email_message(msg)
    except ApiException:
        print("time is over")


def receive_msg_in_new_thread(inbox_id):
    thr = Thread(target=_receive_and_save, args=(inbox_id,))
    thr.start()


if __name__ == '__main__':
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        api_instance.delete_inbox(inbox_id="8d146c3a-9ad5-4789-bc88-cc3be3fbd3d6")