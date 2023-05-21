import bcrypt
import sqlite3

connection = sqlite3.connect('vaccination_app.db')
cursor = connection.cursor()



# Data to be inserted
data = [
    (1, 'Master Admin', '201501502@rajalakshmi.edu.in', '2552', 1)
]

# Iterate over the data and insert into the Admin table
for item in data:
    id, name, email_id, password, otp = item
    hashed_password = bcrypt.hashpw('2552'.encode('utf-8'), bcrypt.gensalt())
    
    # SQL query to insert data into the Admin table
    sql_query = "INSERT INTO Admin (id, name, email_id, password, otp) VALUES (?, ?, ?, ?, ?)"
    
    # Execute the query with the data values
    cursor.execute(sql_query, (id, name, email_id, hashed_password, otp))

# Commit the changes to the database
connection.commit()
connection.close()
