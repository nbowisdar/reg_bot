from datetime import datetime
from .tables import Email as OldEmail
from peewee import *

from setup import ROOT_DIR

# db_lite = SqliteDatabase(ROOT_DIR / "app.db")

db_mysql = MySQLDatabase('db', user='admin', password='admin',
                            host='localhost', port=3306)


# class BaseLite(Model):
#     class Meta:
#         database = db_lite

#
# class Number(BaseLite):
#     number = CharField(unique=True)
#     activation_id = CharField()
#     # note = CharField(null=True)
#     service = CharField()
#     is_active = BooleanField(default=True)
#     created = DateTimeField(default=datetime.now())
#
#
# class Email(BaseLite):
#     email_address = CharField(unique=True)
#     type = CharField(choices=["Uber", "Lyft", "Doorsdash"], default="Uber")
#     status = CharField(choices=["not_ready", "ready", "in_use"], default="not_ready")
#     sex = CharField(default="male")
#     note = CharField(null=True)
#
#
# class EmailMessage(BaseLite):
#     from_email = CharField()
#     subject = CharField()
#     body = TextField()
#     # body = CharField()
#     received = DateTimeField(default=datetime.now())
#     received_str = CharField()
#     # email = ForeignKeyField(Email, backref="messages", on_delete='CASCADE')
#     email = CharField()
#
#
# class PhoneMessage(BaseLite):
#     to_number = ForeignKeyField(Number, backref="messages", on_delete='CASCADE')
#     message = TextField()
#     received = DateTimeField(default=datetime.now)
#
#
# class Task(BaseLite):
#     title = CharField(max_length=255)
#     desc = TextField(null=True)
#     created = DateTimeField(default=datetime.now)
#     executed = BooleanField(default=False)
#
#
# class Template(BaseLite):
#     name = TextField(unique=True)
#     text = TextField()
#     system = BooleanField(default=False)
#
#
# class Trigger(BaseLite):
#     phrase = CharField()
#     template = ForeignKeyField(Template, backref="triggers", on_delete="CASCADE")



class BaseMy(Model):
    class Meta:
        database = db_mysql


class Number_(BaseMy):
    number = CharField(unique=True)
    activation_id = CharField()
    # note = CharField(null=True)
    service = CharField()
    is_active = BooleanField(default=True)
    created = DateTimeField(default=datetime.now())


class Email(BaseMy):
    email_address = CharField(unique=True)
    type = CharField(choices=["Uber", "Lyft", "Doorsdash"], default="Uber")
    status = CharField(choices=["not_ready", "ready", "in_use"], default="not_ready")
    sex = CharField(default="male")
    note = CharField(null=True)


class EmailMessage_(BaseMy):
    from_email = CharField()
    subject = CharField()
    body = TextField()
    # body = CharField()
    received = DateTimeField(default=datetime.now())
    received_str = CharField()
    # email = ForeignKeyField(Email, backref="messages", on_delete='CASCADE')
    email = CharField()


# class PhoneMessage_(BaseMy):
#     to_number = ForeignKeyField(Number, backref="messages", on_delete='CASCADE')
#     message = TextField()
#     received = DateTimeField(default=datetime.now)
#
#
# class Task_(BaseMy):
#     title = CharField(max_length=255)
#     desc = TextField(null=True)
#     created = DateTimeField(default=datetime.now)
#     executed = BooleanField(default=False)
#
#
# class Template_(BaseMy):
#     name = TextField(unique=True)
#     text = TextField()
#     system = BooleanField(default=False)
#
#
# class Trigger_(BaseMy):
#     phrase = CharField()
#     template = ForeignKeyField(Template, backref="triggers", on_delete="CASCADE")


def move_emails():
    for email in OldEmail.select():
        email_ = Email(
            email_address=email.email_address,
            type=email.type,
            status=email.status,
            sex=email.sex,
            note=email.note
        )
        email_.save()


if __name__ == '__main__':
    move_emails()
