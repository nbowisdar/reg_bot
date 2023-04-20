import datetime
import mailbox

maildir = mailbox.Maildir('/root/Maildir')
sorted_messages = sorted(maildir, key=lambda message: datetime.datetime.strptime(message.get_date('%a, %d %b %Y %H:%M:%S %z'), '%a, %d %b %Y %H:%M:%S %z'))

for message in sorted_messages:
    print(message['Subject'])
    date_info = message['Date']
    print(date_info)
