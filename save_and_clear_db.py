from from_sqlite_to_mysql import Email, EmailMessage


emails = []
for e in Email.select():
    emails.append(e.email_address)
    
with open('emails.txt', 'w', encoding='utf-8') as f:
    f.write(
        '\n'.join(emails)
    )
    
# for m in EmailMessage.select():
EmailMessage.delete().execute()
Email.delete().execute()

print("Done")