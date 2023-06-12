# import sqlite3

# # Connect to the database
# conn = sqlite3.connect('vaccination_app.db')
# cursor = conn.cursor()

# # Alter User Table to add Date column
# cursor.execute('''ALTER TABLE User 
#                 ADD COLUMN date DATE''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

import sqlite3

# Connect to the database
conn = sqlite3.connect('vaccination_app.db')
cursor = conn.cursor()

# Create a temporary table with the desired column definitions and default values
cursor.execute('''CREATE TABLE temp_User (
                    id INTEGER,
                    name TEXT,
                    email_id TEXT PRIMARY KEY,
                    password TEXT,
                    otp INTEGER DEFAULT 0,
                    center_id INTEGER,
                    slot INTEGER DEFAULT 0,
                    date DATE,
                    FOREIGN KEY (center_id) REFERENCES VaccinationCenter(center_id)
                )''')

# Copy data from the original table to the temporary table
cursor.execute('''INSERT INTO temp_User SELECT * FROM User''')

# Drop the original table
cursor.execute('''DROP TABLE User''')

# Rename the temporary table to the original table name
cursor.execute('''ALTER TABLE temp_User RENAME TO User''')

# Commit the changes and close the connection
conn.commit()
conn.close()

