from src.database.tables import EmailMessage

if __name__ == '__main__':
    EmailMessage.delete().execute()