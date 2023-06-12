import sqlite3

# Connect to the database
conn = sqlite3.connect('vaccination_app.db')
cursor = conn.cursor()

# Alter User Table to add Date column
cursor.execute('''ALTER TABLE User 
                ADD COLUMN date DATE''')

# Commit the changes and close the connection
conn.commit()
conn.close()
