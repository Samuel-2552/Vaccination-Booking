import sqlite3

# Connect to the database
conn = sqlite3.connect('vaccination.db')
cursor = conn.cursor()

# Create Admin table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email_id TEXT UNIQUE,
        password TEXT,
        ph_no INTEGER,
        otp INTEGER DEFAULT 0,
        status INTEGER DEFAULT 0,
        date DATE
    )
''')

# Create User table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email_id TEXT UNIQUE,
        password TEXT,
        ph_no INTEGER,
        otp INTEGER DEFAULT 0,
        status INTEGER DEFAULT 0,
        date DATE
    )
''')

# Create Vacc Center table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vacc_Center (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        place TEXT,
        working_hour INTEGER DEFAULT 10,
        dosage INTEGER DEFAULT 0,
        slots INTEGER DEFAULT 10,
        slot_time_status INTEGER DEFAULT 0,
        slot_vaccine INTEGER DEFAULT 1,
        vaccine_name TEXT,
        date DATE,
        admin_id INTEGER,
        FOREIGN KEY (admin_id) REFERENCES Admin(id)
    )
''')

# Create Slots table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        center_id INTEGER,
        user_id INTEGER,
        slot_timing TEXT,
        status INTEGER DEFAULT 0,
        date DATE,
        FOREIGN KEY (center_id) REFERENCES Vacc_Center(id),
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (slot_timing) REFERENCES slots_timing(slot_timing)
    )
''')

#create slots_timing table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS slots_timing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        center_id INTEGER,
        center_name TEXT,
        slot_timing TEXT,
        FOREIGN KEY (center_id) REFERENCES Vacc_Center(id),
        FOREIGN KEY (center_name) REFERENCES Vacc_Center(name),
    )
 ''')

# Create User History table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User_History (
        user_id INTEGER,
        center_id INTEGER,
        slot_date DATE,
        slot_timing TEXT,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES User(id),
        FOREIGN KEY (center_id) REFERENCES Vacc_Center(id),
        FOREIGN KEY (slot_date) REFERENCES Slots(date),
        FOREIGN KEY (slot_timing) REFERENCES Slots(slot_timing),
        FOREIGN KEY (status) REFERENCES Slots(status)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
