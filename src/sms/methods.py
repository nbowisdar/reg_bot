from loguru import logger
from twilio.rest import Client
import json

from twilio.rest.api.v2010.account.incoming_phone_number import IncomingPhoneNumberContext

from setup import TWILIO_SID, TWILIO_TOKEN
from src.database.queries import save_number

client = Client(TWILIO_SID, TWILIO_TOKEN)


class ClientNumber:
    def __init__(self, webhook: str):
        self.client = client
        self.webhook = webhook

    def set_webhook(self, number: str):
        # dedov_update(number)
        pass

    def get_all_numbers(self) -> list[str]:
        numbers = self.client.incoming_phone_numbers.list()
        return [number.phone_number for number in numbers]

    def create_new_number(self, amount: int) -> list[str]:
        numbers = self.client.available_phone_numbers('US').local.list(limit=amount)
        res = []
        for number in numbers:
            if number.capabilities['SMS']:
                new_number = client.incoming_phone_numbers.create(phone_number=number.phone_number)
                # save number in db
                save_number(new_number.phone_number)
                res.append(new_number.phone_number)
        return res

    def delete_number_from_site(self, number: str) -> bool:
        numbers = self.client.incoming_phone_numbers.list()
        for cur_number in numbers:
            if cur_number == number:
                cur_number.delete()
                logger.info(f"{number} - deleted")
                return True
        return False


my_client = ClientNumber("test.link")
if __name__ == '__main__':
    cur = ClientNumber('test.link')
    cur.delete_number_from_site("+13204410934")
    x = cur.get_all_numbers()
    print(x)


