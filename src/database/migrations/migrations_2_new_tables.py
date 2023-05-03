import sqlite3

conn = sqlite3.connect('app.db')

# Get a cursor object
cursor = conn.cursor()

# Add a new column to the table
cursor.execute("""
CREATE TABLE template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE,
    text TEXT
);
""")

cursor.execute("""
CREATE TABLE trigger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phrase VARCHAR(255),
    template_id INTEGER,
    FOREIGN KEY (template_id) REFERENCES Template(id)
);
""")
# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
