import datetime
import mailbox

maildir = mailbox.Maildir('/root/Maildir')
sorted_messages = sorted(maildir, key=lambda message: datetime.datetime.fromtimestamp(float(message.get_date())))

for message in sorted_messages:
    print(message['Subject'])
    date_info = message['Date']
    print(date_info)
