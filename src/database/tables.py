from peewee import Model, CharField, IntegerField, SqliteDatabase, ForeignKeyField,\
    TextField, DateTimeField
from datetime import datetime
from setup import ROOT_DIR


db = SqliteDatabase(ROOT_DIR / "app.db")


class BaseModel(Model):
    class Meta:
        database = db


class Number(BaseModel):
    number = CharField(unique=True)
    note = CharField(null=True)
    created = DateTimeField(default=datetime.now())


class Email(BaseModel):
    email_id = CharField(unique=True)
    email_address = CharField(unique=True)
    note = CharField(null=True)


class EmailMessage(BaseModel):
    from_email = CharField()
    subject = CharField(0)
    body = CharField()
    received = DateTimeField(default=datetime.now())
    email = ForeignKeyField(Email, backref="messages", on_delete='CASCADE')


class PhoneMessage(BaseModel):
    from_number = CharField()
    to_number = ForeignKeyField(Number, backref="messages", on_delete='CASCADE')
    message = TextField()
    received = DateTimeField(default=datetime.now())


def create_tables():
    tables = [Number, Email, PhoneMessage, EmailMessage]
    db.create_tables(tables)


if __name__ == '__main__':
    create_tables()