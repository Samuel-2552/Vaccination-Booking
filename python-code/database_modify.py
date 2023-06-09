import sqlite3

# Connect to the database
conn = sqlite3.connect('vaccination_app.db')
cursor = conn.cursor()

# Alter User Table to add center_id and slot columns if they don't exist
cursor.execute('''PRAGMA table_info(User)''')
columns = cursor.fetchall()
column_names = [column[1] for column in columns]
if 'center_id' not in column_names:
    cursor.execute('''ALTER TABLE User ADD COLUMN center_id INTEGER''')
if 'slot' not in column_names:
    cursor.execute('''ALTER TABLE User ADD COLUMN slot INTEGER''')

# Add foreign key constraint
cursor.execute('''PRAGMA foreign_keys = ON''')
cursor.execute('''ALTER TABLE User ADD FOREIGN KEY (center_id) REFERENCES VaccinationCenter(center_id)''')

# Commit the changes and close the connection
conn.commit()
conn.close()
