import sqlite3

# Connect to the database
conn = sqlite3.connect('vaccination_app.db')
cursor = conn.cursor()

# Create a new temporary table with the desired modifications
cursor.execute('''CREATE TABLE IF NOT EXISTS User_temp (
                    id INTEGER,
                    name TEXT,
                    email_id TEXT PRIMARY KEY,
                    password TEXT,
                    otp INTEGER,
                    center_id INTEGER,
                    slot INTEGER,
                    FOREIGN KEY (center_id) REFERENCES VaccinationCenter(center_id)
                )''')

# Copy data from the original User table to the temporary table
cursor.execute('''INSERT INTO User_temp SELECT * FROM User''')

# Drop the original User table
cursor.execute('''DROP TABLE User''')

# Rename the temporary table to User
cursor.execute('''ALTER TABLE User_temp RENAME TO User''')

# Commit the changes and close the connection
conn.commit()
conn.close()
