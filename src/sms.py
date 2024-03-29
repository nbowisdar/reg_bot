import time
from pprint import pprint
from threading import Thread
from loguru import logger
from smsactivate.api import SMSActivateAPI
from setup import SMS_TOKEN
from src.database.queries import save_message
from src.models import PhoneMessageModel, NumberModel

sa = SMSActivateAPI(SMS_TOKEN)


def _get_cheapest_country(data: dict, only_usa=False) -> dict:
    if only_usa:
        data = {key: value for key, value in data.items() if value['country'] == 12 or value['country'] == 187}
    struct_data = [value for value in data.values()]
    for info in sorted(struct_data, key=lambda x: x['price']):
        if info["count"] > 0:
            return info


def buy_new_number(service: str) -> NumberModel | str:
    only_usa = False
    if service in ['ub', 'tu']:
        only_usa = True
    country = sa.getTopCountriesByService(service)
    best_country = _get_cheapest_country(country, only_usa=only_usa)
    number = sa.getNumberV2(service=service, country=best_country['country'], verification="false")
    if 'error' in number.keys():
        return f"Not enough funds, price - {best_country['retail_price']} rub"
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
    try:
        for active in sa.getActiveActivations()['activeActivations']:
            if active['phoneNumber'] == phone_number:
                return len(active['smsText'])
    except Exception as err:
        logger.error(err)
        return 0


def _receive_sms(phone_number: str):
    old_messages_amount = _get_amount_sms(phone_number)
    try:
        while True:
            time.sleep(5)
            actives = sa.getActiveActivations()
            active_list = actives['activeActivations']

            for active in active_list:
                if phone_number == active['phoneNumber']:
                    messages = active['smsText']
                    if messages:
                        if old_messages_amount == 0:
                            save_message(PhoneMessageModel(
                                to_number=phone_number,
                                message=messages[0]
                            ))
                            return
                        elif old_messages_amount > 1:
                            if len(messages) > old_messages_amount:
                                save_message(PhoneMessageModel(
                                    to_number=phone_number,
                                    message=messages[-1]
                                ))
                                return
    except KeyError:
        pass


def request_new_sms(activation_id: str):
    response = sa.setStatus(id=activation_id, status=3)
    print(response)
    if response == "ACCESS_CANCEL":
        return True
    return False


def create_waiting_thread(phone_number: str) -> Thread:
    return Thread(target=_receive_sms, args=(phone_number,))


def get_balance() -> str:
    resp = sa.getBalance()
    return resp['balance'] + ' rub'


if __name__ == '__main__':
    x = get_balance()
    print(x)