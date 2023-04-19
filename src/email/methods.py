import mailslurp_client
from bs4 import BeautifulSoup
from loguru import logger
from mailslurp_client import ApiException
from threading import Thread
from time import perf_counter, time, sleep
from src.config import domain
from src.database.queries import save_new_email, save_email_message
from src.email.messages import get_all_message_amount, get_last_msg
from src.models import EmailModel, EmailMessageModel
import random
from names import get_full_name


def gen_email_name() -> str:
    name = get_full_name().replace(" ", ".").lower()
    name_add_num = name + str(random.randrange(10, 999))
    #return name_add_num + '@stevejobs.pp.ua'
    return name_add_num + '@' + domain
#
#
# configuration = mailslurp_client.Configuration()
# configuration.api_key['x-api-key'] = MAILSLURP_KEY


# create new inbox
def create_inbox(note=None) -> str:
        inbox = gen_email_name()
        save_new_email(EmailModel(
            email_address=inbox,
            note=note
        ))
        return inbox


def create_few_inboxes(amount=1, note=None) -> list[str]:
    res = []
    for _ in range(amount):
        inbox = gen_email_name()
        save_new_email(EmailModel(
            email_address=inbox,
            note=note
        ))
        res.append(inbox)
    return res


def _receive_msg(inbox) -> EmailMessageModel | bool:
    start = perf_counter()
    amount = get_all_message_amount(inbox)

    while perf_counter() < start + 360:
        sleep(10)
        new_amount = get_all_message_amount(inbox)
        if new_amount == amount:
            continue

        return get_last_msg(inbox)

    return False

        # return EmailMessageModel(
        #     from_email=msg._from,
        #     email=msg.to,
        #     inbox_id=inbox_id,
        #     subject=msg.subject,
        #     body=soup.text
        # )


def _receive_and_save(inbox):
    logger.info(f"start listening {inbox}")
    msg = _receive_msg(inbox)
    save_email_message(msg)


def receive_msg_in_new_thread(inbox):
    thr = Thread(target=_receive_and_save, args=(inbox,))
    thr.start()

#
# def delete_all_inboxes():
#     with mailslurp_client.ApiClient(configuration) as api_client:
#         api_instance = mailslurp_client.InboxControllerApi(api_client)
#         api_instance.delete_all_inboxes()


# if __name__ == '__main__':
#     with mailslurp_client.ApiClient(configuration) as api_client:
#         # create an inbox using the inbox controller
#         api_instance = mailslurp_client.InboxControllerApi(api_client)
#         api_instance.delete_inbox(inbox_id="8d146c3a-9ad5-4789-bc88-cc3be3fbd3d6")
#         api_instance.de