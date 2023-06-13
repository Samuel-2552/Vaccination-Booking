from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import bcrypt
from datetime import date, datetime
import schedule
import time
import smtplib
import random

app = Flask(__name__)
app.secret_key = 'ghf5yr7698iyf5463fhgfytytr9'  # Set a secret key for session encryption

def curr_date():
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    return formatted_date

def OTP():
    return random.randint(100000, 999999)

def g_mail(to_email,subject,body):

    # Sender's email and password
    gmail_user = "201501502@rajalakshmi.edu.in"
    gmail_password = "#"


    # Prepare the email
    email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, to_email, subject, body)

    try:
        # Send the email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')

# User signup logic
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    try:
        if request.method == 'POST':
            # Get the user signup form data
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            ph_no = request.form['ph_no']

            otp=OTP()
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO Admin (name, email_id, password, ph_no, otp, date) VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (name, email, hashed_password, ph_no, otp, curr_date()))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()

            
            
            g_mail(email,f"Welcome to DevRev's Vaccination Booking {name} Admin!", f"Create your Centers for booking vaccines slots! \nVerify your Email by entering this OTP once you LogIn. \n Your OTP is {otp}.")
            # Redirect to the login page after successful signup
            return redirect('/admin/login')
    except:
        return render_template('admin_signup.html',error="Email-Id already Exists!")
    
    # Render the user signup form
    return render_template('admin_signup.html')


# User signup logic
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    try:
        if request.method == 'POST':
            # Get the user signup form data
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            ph_no = request.form['ph_no']

            otp=OTP()
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO User (name, email_id, password, ph_no, otp, date) VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (name, email, hashed_password, ph_no, otp, curr_date()))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()

            
            
            g_mail(email,f"Welcome to DevRev's Vaccination Booking {name}!", f"Book your slot Today! \nVerify your Email by entering this OTP once you LogIn. \n Your OTP is {otp}.")
            # Redirect to the login page after successful signup
            return redirect('/login')
    except:
        return render_template('signup.html',error="Email-Id already Exists!")
    
    # Render the user signup form
    return render_template('signup.html')

# User login logic
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    try:
        if request.method == 'POST':
            # Get the user login form data
            email = request.form['email']
            password = request.form['password']
            
            # Retrieve the user from the database
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            user_query = '''
            SELECT * FROM User WHERE email_id = ?
            '''
            cursor.execute(user_query, (email,))
            user = cursor.fetchone()
            
            if user:
                # Verify the password
                stored_password = user[3]  # Assuming the password is stored in the 4th column
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Set the user ID in the session
                    session['user_id'] = user[2]  # Assuming the user ID is stored in the 1st column
                    
                    # Close the connection
                    cursor.close()
                    conn.close()
                    
                    # Redirect to the home page after successful login
                    return redirect('/')
            
            # Invalid credentials, display an error message or redirect to the login page
            cursor.close()
            conn.close()
            return render_template('login.html', error="Invalid Credentials!")
    except:
        render_template('login.html', error="Server Down Try Again Later.")
    
    # Render the user login form
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic

            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']

            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()

            # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT name FROM Vacc_Center")
            centers = cursor.fetchall()

            cursor.execute("SELECT DISTINCT slot_timing FROM Slots")
            hours = cursor.fetchall()

            cursor.execute("SELECT * FROM User WHERE email_id = ?",(user_id,))
            user = cursor.fetchone() 
            name=user[1]
            print("slot :", user)

            # Check if the search form is submitted
            if request.method == 'POST':
                center = request.form['center']
                hour = request.form['hour']

                # Query the database to fetch the rows matching the selected criteria
                cursor.execute("SELECT * FROM Vacc_Center WHERE center_name = ? OR working_hour = ?", (center, hour))
                rows = cursor.fetchall()
                

                # Close the connection and cursor
                cursor.close()
                conn.close()

                # Render the template with the search results
                return render_template('user_dash.html', show_logout=True, vaccination_centers=centers, hours=hours, rows=rows, name=name)

            # Close the connection and cursor
            cursor.close()
            conn.close()

            return render_template('user_dash.html', show_logout=True, vaccination_centers=centers, hours=hours, name= name)
        else:
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()

            # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT name FROM Vacc_Center")
            centers = cursor.fetchall()

            cursor.execute("SELECT DISTINCT slot_timing FROM Slots")
            hours = cursor.fetchall()
            # Check if the search form is submitted
            if request.method == 'POST':
                center = request.form['center']
                hour = request.form['hour']

                print("This is debugging",center,hour)

                # Query the database to fetch the rows matching the selected criteria
                cursor.execute("SELECT * FROM VaccinationCenter WHERE center_name = ? OR working_hour = ?", (center, hour))
                rows = cursor.fetchall()
                print(rows)
                # Close the connection and cursor
                cursor.close()
                conn.close()

                # Render the template with the search results
                return render_template('home.html', show_logout=False, vaccination_centers=centers, hours=hours, rows=rows)

            # Close the connection and cursor
            cursor.close()
            conn.close()
            
    # User is not logged in, redirect to the home page
            return render_template('home.html', show_logout=False, vaccination_centers=centers, hours=hours)
    except Exception as e:
        print(e)
        return "Ran into Some Issues. Please go back and try again."



# Logout
@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect('/')

#admin login logic
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic
            
            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']
            
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            user_query = '''
            SELECT * FROM Admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()
            
            if user:
                # Display user-specific information or perform other operations
                
                # Example: Get the user's name
                name = user[1]  # Assuming the name is stored in the 2nd column
                
                # Close the connection and cursor
                cursor.close()
                conn.close()
                
                return redirect('/admin/dashboard')
    except:
        return "Ran into Some Issues go back and Try Again."
        
    try:
        if request.method == 'POST':
            # Get the user login form data
            email = request.form['email']
            password = request.form['password']
            
            # Retrieve the user from the database
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            user_query = '''
            SELECT * FROM Admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (email,))
            user = cursor.fetchone()
            
            if user:
                # Verify the password
                stored_password = user[3]  # Assuming the password is stored in the 4th column
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Set the user ID in the session
                    session['user_id'] = user[2]  # Assuming the user ID is stored in the 1st column
                    
                    # Close the connection
                    cursor.close()
                    conn.close()
                    
                    # Redirect to the home page after successful login
                    return redirect('/admin/dashboard')
            
            # Invalid credentials, display an error message or redirect to the login page
            cursor.close()
            conn.close()
            return "Invalid credentials"
    except:
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user login form
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic
            
            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']
            
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            user_query = '''
            SELECT * FROM Admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()
            
            if user and user_id == '201501502@rajalakshmi.edu.in':
                # Display user-specific information or perform other operations
                
                # Example: Get the user's name
                name = user[1]  # Assuming the name is stored in the 2nd column

                # Retrieve the table data from the database
                table_query = '''
                SELECT * FROM Admin
                '''
                cursor.execute(table_query)
                table_data = cursor.fetchall()

                table_query2 = '''
                SELECT * FROM Vacc_Center
                '''
                cursor.execute(table_query2)
                table_data2 = cursor.fetchall()
                
                # Close the connection and cursor
                cursor.close()
                conn.close()
                
                return render_template('admin_dash.html', name=name, table_data=table_data, table_data2=table_data2)
        else:
            return redirect('/admin/login')
        if user:
            # Display user-specific information or perform other operations
            
            # Example: Get the user's name
            name = user[1]  # Assuming the name is stored in the 2nd column
            id = user[0]
            center_query = '''
            SELECT * FROM Vacc_Center WHERE admin_id = ?
            '''
            cursor.execute(center_query, (id,))
            table_data = cursor.fetchall()
            
            # Close the connection and cursor
            cursor.close()
            conn.close()
            
            return render_template('vacc_center.html', name=name, table_data=table_data)
        
    except:
        return "Ran into Some Issues go back and Try Again."

    
    # User is not logged in, redirect to home page

    return redirect('/admin/login')


@app.route('/admin/add_admin', methods=['GET', 'POST'])
def add_admin():
    try:
        if request.method == 'POST':
            # Get the user signup form data
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            ph_no = request.form['ph_no']
            otp=OTP()
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            

            # Perform user signup logic here
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO Admin ( name, email_id, password, ph_no, otp, date) VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (name, email, hashed_password, ph_no, otp, curr_date()))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()

            g_mail(email,f"Welcome to DevRev's Vaccination Booking {name} Admin!", f"Create your Centers for booking vaccines slots! \nVerify your Email by entering this OTP once you LogIn. \n Your OTP is {otp}.")
            
            # Redirect to the login page after successful signup
            return  redirect('/admin/dashboard')
    except Exception as e:
        print(e)
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user signup form
    return redirect('/admin/dashboard')


@app.route('/admin/remove/<int:id>', methods=['GET', 'POST'])
def remove_admin(id):
    try:
        if request.method == 'POST':
            # Delete the admin with the given ID from the database
            connection = sqlite3.connect('vaccination.db')
            cursor = connection.cursor()
            
            try:
                cursor.execute("DELETE FROM Admin WHERE id = ?", (id,))
                connection.commit()
                flash('Admin successfully removed')
            except sqlite3.Error as e:
                connection.rollback()
                flash('An error occurred while removing the admin')
                print('SQLite error occurred:', e.args[0])

            connection.close()
    except:
        return "Ran into Some Issues go back and Try Again."

    return redirect('/admin/dashboard')


@app.route('/admin/add_center', methods=['GET', 'POST'])
def add_centre():

    try:
        if request.method == 'POST' and 'user_id' in session:

            admin_email_id = session['user_id']

            # Get the user signup form data
            center_name = request.form['center_name']
            place = request.form['place']
            working_hour = request.form['working_hour']
            dosage = request.form['dosage']
            slots = request.form['slots']

            
            
            # Perform add center logic here
            conn = sqlite3.connect('vaccination.db')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM Admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (admin_email_id,))
            user = cursor.fetchone()
            
            insert_user_query = '''
            INSERT INTO Vacc_Center (name, place, working_hour, dosage, slots, date, admin_id) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (center_name, place, working_hour, dosage, slots, curr_date(), user[0]))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()
            
            # Redirect to the login page after successful signup
            return  redirect('/admin/dashboard')
        
    except Exception as e:
        print(e)
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user signup form
    return redirect('/admin/dashboard')


@app.route('/admin/remove_center/<int:center_id>', methods=['GET', 'POST'])
def remove_center(center_id):
    try:
        if request.method == 'POST':
            # Delete the vaccination center with the given ID from the database
            connection = sqlite3.connect('vaccination.db')
            cursor = connection.cursor()
            
            try:
                cursor.execute("DELETE FROM Vacc_center WHERE id = ?", (center_id,))
                connection.commit()
                flash('Vaccination center successfully removed')
            except sqlite3.Error as e:
                connection.rollback()
                flash('An error occurred while removing the vaccination center')
                print('SQLite error occurred:', e.args[0])

            connection.close()
    except:
        return "Ran into Some Issues go back and Try Again."

    return redirect('/admin/dashboard')  # Redirect to the admin page after deleting

@app.route('/book-slot', methods=['POST'])
def book_slot():
    if 'user_id' in session:            
        email_id = session['user_id']
        center_id = request.json['center_id']
        conn = sqlite3.connect('vaccination.db')
        cursor = conn.cursor()
        # Update the user's slot
        cursor.execute("UPDATE User SET slot = 0 WHERE email_id = ?", (email_id,) )

        # Check if slots already booked
        cursor.execute("SELECT slot FROM user WHERE email_id = ?", (email_id,))
        slot= cursor.fetchone()[0]
        if slot > 0:
            conn.close()
            return 'Slot already Booked! Maximium 1 booking!'
        
        # Check if slots are available
        cursor.execute("SELECT slots FROM VaccinationCenter WHERE center_id = ?", (center_id,))
        slots_available = cursor.fetchone()[0]
        if slots_available <= 0:
            conn.close()
            return 'No slots available'
        
        # Update the user's slot
        cursor.execute("UPDATE User SET slot = 1, date = ?, center_id = ? WHERE email_id = ?", (date.today(), center_id, email_id))
        
        # Update the vaccination center's slots
        cursor.execute("UPDATE VaccinationCenter SET slots = slots - 1 WHERE center_id = ?", (center_id,))
        
        conn.commit()
        conn.close()
        print("Center Id received is: ", center_id)
        return 'Slot booked successfully'
    else:
        return 'Try Again Later!'



@app.route('/search')
def search():
    # Search logic
    return "Search page"

@app.route('/apply')
def apply():
    # Apply logic
    return "Apply page"


@app.route('/admin/dosage_details')
def dosage_details():
    # Get dosage details logic
    return "Get dosage details page"


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
