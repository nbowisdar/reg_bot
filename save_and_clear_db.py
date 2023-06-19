import os
from from_sqlite_to_mysql import Email, EmailMessage
import shutil


emails = []
for e in Email.select():
    emails.append(e.email_address)

with open("emails.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(emails))

EmailMessage.delete().execute()


folder_path = "/root/Maildir"  # Specify the folder name

# Check if the folder exists
if os.path.exists(folder_path):
    # Remove the folder and its contents
    shutil.rmtree(folder_path)
    print(f"The folder '{folder_path}' has been deleted.")
else:
    print(f"The folder '{folder_path}' does not exist.")


print("Done")
