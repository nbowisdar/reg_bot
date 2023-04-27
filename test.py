#
# from src.database.tables import EmailMessage
# from datetime import datetime, timedelta
#
# messages = EmailMessage.select()
#
#
# def str_time_to_timestamp(date: str) -> datetime:
#     time_str = date.replace(" (UTC)", "")
#     date_object = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
#     return date_object
#
#
# # for msg in messages:
# #     new_date = str_time_to_timestamp(msg.received_str)
# #     msg.received = new_date
# #     msg.received_str = new_date.strftime('%Y-%m-%d %H:%M')
# #     msg.save()
#
# datetime.now() - timedelta(minutes=30)
# print('done')
#     # msg.received = new_date
import shutil

shutil.rmtree('/root/Maildir')