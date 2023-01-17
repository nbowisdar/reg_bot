import time
from pprint import pprint
from threading import Thread
from loguru import logger
from smsactivate.api import SMSActivateAPI
from setup import SMS_TOKEN
from src.database.queries import save_message
from src.models import PhoneMessageModel, NumberModel

sa = SMSActivateAPI(SMS_TOKEN)


def _get_cheapest_country(data: dict) -> int:
    struct_data = [value for value in data.values()]
    for info in sorted(struct_data, key=lambda x: x['price']):
        if info["count"] > 0:
            return info['country']


def buy_new_number(service="go") -> NumberModel:
    country = sa.getTopCountriesByService("go")
    best_country = _get_cheapest_country(country)
    number = sa.getNumberV2(service=service, country=best_country, verification="false")
    return NumberModel(
        activation_id=number['activationId'],
        number=number['phoneNumber'],
        service=service,
        is_active=True
    )


def cancel_number(activation_id: str) -> bool:
    response = sa.setStatus(id=activation_id, status=8)
    if response == "ACCESS_CANCEL":
        return True
    return False


def _get_amount_sms(phone_number: str) -> int:
    for active in sa.getActiveActivations()['activeActivations']:
        if active['phoneNumber'] == phone_number:
            return len(active['smsText'])


def _receive_sms(phone_number: str):
    old_messages_amount = _get_amount_sms(phone_number)
    while True:
        time.sleep(5)
        actives = sa.getActiveActivations()
        active_list = actives['activeActivations']

        for active in active_list:
            if phone_number == active['phoneNumber']:
                messages = active['smsText']
                if len(messages) > old_messages_amount:
                    save_message(PhoneMessageModel(
                        to_number=phone_number,
                        message=messages[-1]
                    ))
                    break


def request_new_sms(activation_id: str):
    response = sa.setStatus(id=activation_id, status=3)
    print(response)
    if response == "ACCESS_CANCEL":
        return True
    return False


def create_waiting_thread(phone_number: str) -> Thread:
    return Thread(target=_receive_sms, args=(phone_number,))


if __name__ == '__main__':
    _get_amount_sms("1232154780")
