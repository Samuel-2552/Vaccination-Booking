import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('vaccination_app.db')
cursor = conn.cursor()

# Create User table
create_user_table_query = '''
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
'''
cursor.execute(create_user_table_query)

# Create VaccinationCenter table
create_vaccination_center_table_query = '''
CREATE TABLE IF NOT EXISTS VaccinationCenter (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    working_hours TEXT NOT NULL
);
'''
cursor.execute(create_vaccination_center_table_query)

# Create Slot table
create_slot_table_query = '''
CREATE TABLE IF NOT EXISTS Slot (
    id INTEGER PRIMARY KEY,
    center_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    available_slots INTEGER NOT NULL,
    user_names TEXT,
    FOREIGN KEY (center_id) REFERENCES VaccinationCenter(id)
);
'''
cursor.execute(create_slot_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
