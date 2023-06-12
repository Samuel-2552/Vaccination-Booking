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

# Alter User Table to set default values for otp and slot columns
cursor.execute('''ALTER TABLE User 
                  ALTER COLUMN otp SET DEFAULT 0;
               ''')

cursor.execute('''ALTER TABLE User 
                  ALTER COLUMN slot SET DEFAULT 0;
               ''')

# Commit the changes and close the connection
conn.commit()
conn.close()
