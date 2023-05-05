# from peewee import SqliteDatabase, PostgresqlDatabase, Model, CharField, IntegerField
# from
#
# # Define the source SQLite database
# sqlite_db = SqliteDatabase('app.db')
#
# # Define the target PostgreSQL database
# pg_db = PostgresqlDatabase('db', user='admin', password='admin',
#                            host='localhost', port=5432)
#
# # Define a base model for the SQLite database
# class SQLiteBaseModel(Model):
#     class Meta:
#         database = sqlite_db
#
# # Define a model for the SQLite database
# class SQLiteModel(SQLiteBaseModel):
#     name = CharField()
#     age = IntegerField()
#
# class PostgresBaseModel(Model):
#     class Meta:
#         database = pg_db
#
# # Define a model for the PostgreSQL database
# class PostgresModel(PostgresBaseModel):
#     name = CharField()
#     age = IntegerField()
#
# # Connect to the SQLite database and fetch all records
# sqlite_db.connect()
# sqlite_records = SQLiteModel.select()
#
# # Connect to the PostgreSQL database and create the table
# pg_db.connect()
# pg_db.create_tables([PostgresModel])
#
# # Migrate the data from SQLite to PostgreSQL
# for record in sqlite_records:
#     pg_record = PostgresModel(name=record.name, age=record.age)
#     pg_record.save()
#
# # Close the database connections
# sqlite_db.close()
# pg_db.close()
