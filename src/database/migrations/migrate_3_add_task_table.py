import sqlite3

connection = sqlite3.connect('app.db')
cursor = connection.cursor()

create_table_query = '''
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    desc TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed BOOLEAN DEFAULT 0
);
'''

cursor.execute(create_table_query)
connection.commit()

cursor.close()
connection.close()
