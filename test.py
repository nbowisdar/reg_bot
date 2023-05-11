from src.database.tables import EmailMessage, Email

if __name__ == '__main__':
    c = 0
    for email in Email.select():
        if email.sex == "❓":
            email.sex = "male"
            email.save()
            c += 1
    print("all -", c)