import sqlite3

conn = sqlite3.connect('app.db')

# Get a cursor object
cursor = conn.cursor()

# Add a new column to the table
cursor.execute("ALTER TABLE Email ADD COLUMN type VARCHAR(20) DEFAULT 'Uber'")

# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()