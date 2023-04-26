import json

from peewee import Model, CharField, IntegerField, SqliteDatabase, ForeignKeyField,\
    TextField, DateTimeField, BooleanField
from datetime import datetime
from setup import ROOT_DIR


db = SqliteDatabase(ROOT_DIR / "app.db")


class BaseModel(Model):
    class Meta:
        database = db


class Number(BaseModel):
    number = CharField(unique=True)
    activation_id = CharField()
    # note = CharField(null=True)
    service = CharField()
    is_active = BooleanField(default=True)
    created = DateTimeField(default=datetime.now())


class Email(BaseModel):
    email_address = CharField(unique=True)
    is_ready = BooleanField(default=False)
    note = CharField(null=True)


class EmailMessage(BaseModel):
    from_email = CharField()
    subject = CharField()
    body = CharField()
    received = DateTimeField(default=datetime.now())
    received_str = CharField()
    # email = ForeignKeyField(Email, backref="messages", on_delete='CASCADE')
    email = CharField()


class PhoneMessage(BaseModel):
    to_number = ForeignKeyField(Number, backref="messages", on_delete='CASCADE')
    message = TextField()
    received = DateTimeField(default=datetime.now())


def create_tables():
    tables = [Number, Email, PhoneMessage, EmailMessage]
    db.create_tables(tables)



class EmailSaver:
    def __init__(self):
        with open("emails.json", mode='r', encoding="utf-8") as file:
            self.data = json.load(file)
            # self.active = data['active']
            # self.deleted = data['deleted']

    def get_emails(self) -> list[str]:
        return self.data['active']

    def filter_deleted(self, msgs: list[EmailMessage]):
        return [msg for msg in msgs if msg.email not in self.data['deleted']]

    def delete_email(self, inbox: str):
        self.data['deleted'].append(inbox)
        with open("emails.json", mode='w', encoding="utf-8") as file:
            json.dump(self.data, file)

    def add_inbox(self, inbox):
        self.data['active'].append(inbox)
        with open("emails.json", mode='r', encoding="utf-8") as file:
            json.dump(self.data, file)



if __name__ == '__main__':
    create_tables()