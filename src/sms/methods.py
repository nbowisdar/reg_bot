import requests
from twilio.rest import Client
import json
client = Client('AC9ae53af1405032a48bb293c8aa8b6605', '462dbb5dc73e369c03b8c0d18bc92e1c')


# resp = client.request("")



# toll_free = client.available_phone_numbers('US').local.list(limit=10)
#
# for number in toll_free:
#     if number.capabilities['SMS']:
#         client.incoming_phone_numbers.create(phone_number=number.phone_number)


number = client.incoming_phone_numbers.list()[0]

print(number.update())

# buy a new number
# new_number = client.incoming_phone_numbers.create(phone_number=number.phone_number)

#client.incoming_phone_numbers.list()[0].delete()


# for i in numbers:
#     print(i.delete())
# mobile = client.available_phone_numbers("GB").mobile.list(limit=20)
# for record in mobile:
#     print(record.friendly_name)
