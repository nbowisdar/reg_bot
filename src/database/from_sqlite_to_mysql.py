import sqlite3
import mysql.connector

# Connect to SQLite database
sqlite_conn = sqlite3.connect('app.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL database
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='admin',
    database='db'
)
mysql_cursor = mysql_conn.cursor()

# Get list of tables in SQLite database
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in sqlite_cursor.fetchall()]

# Transfer data from SQLite to MySQL for each table
for table in tables:
    # Get data from SQLite table
    sqlite_cursor.execute(f"SELECT * FROM {table};")
    data = sqlite_cursor.fetchall()

    # Create MySQL table with same schema as SQLite table
    sqlite_cursor.execute(f"PRAGMA table_info({table});")
    schema = sqlite_cursor.fetchall()
    mysql_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({','.join([f'{col[1]} {col[2]}' for col in schema])});")

    # Insert data into MySQL table
    ok = 0
    e = 0
    for row in data:
        try:
            mysql_cursor.execute(f"INSERT INTO {table} VALUES ({','.join(['%s']*len(row))})", row)
            ok += 1
        except Exception as err:
            print(f"Error - {err}")
            e += 1
    print("Okay -", ok)
    print("Errors -", e)

# Commit changes and close connections
mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()
