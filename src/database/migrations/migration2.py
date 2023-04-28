import sqlite3

# Create a new database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Execute the SQL command to add the new column
cursor.execute("ALTER TABLE email ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'not_ready' CHECK (status IN ('not_ready', 'ready', 'in_use'));")
cursor.execute("ALTER TABLE email DROP COLUMN is_ready;")

# Commit the changes
conn.commit()

# Close the database connection
conn.close()