import sqlite3

from peewee import PostgresqlDatabase

conn = sqlite3.connect('app.db')
conn = PostgresqlDatabase('db', user='admin', password='admin',
                            host='localhost', port=3306)

# Get a cursor object
cursor = conn.cursor()

# Add a new column to the table
cursor.execute("ALTER TABLE EmailMessage ALTER COLUMN body TYPE TEXT;")

# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()