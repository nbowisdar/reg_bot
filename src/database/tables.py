from peewee import Model, CharField, IntegerField, SqliteDatabase, ForeignKeyField,\
    TextField, DateTimeField
from datetime import datetime
from setup import ROOT_DIR
print(ROOT_DIR / "app.db")
db = SqliteDatabase(ROOT_DIR / "app.db")


class BaseModel(Model):
    class Meta:
        database = db


class Number(BaseModel):
    number = CharField(unique=True)
    created = DateTimeField(default=datetime.now())


class Email(BaseModel):
    email_id = CharField(unique=True)
    email_address = CharField(unique=True)


class EmailMessage(BaseModel):
    from_email = CharField()
    subject = CharField(0)
    body = CharField()

    email = ForeignKeyField(Email, backref="messages")


class PhoneMessage(BaseModel):
    from_number = CharField()
    to_number = ForeignKeyField(Number, backref="messages")
    message = TextField()
    received = DateTimeField(default=datetime.now())


def create_tables():
    tables = [Number, Email, PhoneMessage, EmailMessage]
    db.create_tables(tables)


if __name__ == '__main__':
    create_tables()