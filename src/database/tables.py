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


class Gmail(BaseModel):
    mail = CharField(unique=True)
    password = CharField()
    cookies = CharField()
    number = ForeignKeyField(Number, backref="mails")


class PhoneMessage(BaseModel):
    from_number = CharField()
    to_number = ForeignKeyField(Number, backref="messages")
    message = TextField()
    received = DateTimeField(default=datetime.now())


def create_tables():
    tables = [Number, Gmail, PhoneMessage]
    db.create_tables(tables)


if __name__ == '__main__':
    create_tables()