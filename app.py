from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import sqlite3
import bcrypt
from datetime import date, datetime, timedelta
# import schedule
import time
import smtplib
import random
import math

app = Flask(__name__)
app.secret_key = 'ghf5yr7698iyf5463fhgfytytr9'  # Set a secret key for session encryption


def next_n_days(n):
    current_date = datetime.now().date()
    next_n_dates = []
    for i in range(1, n+1):
        delta = timedelta(days=i)
        future_date = current_date + delta
        formatted_date = future_date.strftime("%Y-%m-%d")
        next_n_dates.append(formatted_date)
    return next_n_dates

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

def g__mail(to_email,subject,body):

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
        return 1
    except Exception as e:
        print(e)
        print('Something went wrong...')
        return 0

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
            print(otp)
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
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
            print(otp)
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
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
            conn.execute('PRAGMA foreign_keys = ON;')
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

@app.route('/send_otp')
def send_otp():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic

            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']

            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM user WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()
            otp=OTP()
            cursor.execute('''UPDATE user SET otp = ? WHERE id = ?''', (otp, user[0]))
            conn.commit()
            conn.close()

            check=g__mail(user_id, f"Welcome to DevRev's Vaccination Booking {user[1]}!", f"Your OTP is {otp}. \n Verify it and Book your Slot Today!")
            if check==1:
                return render_template('verify_otp.html', success="OTP Sent! Check Mail!", name=user[1])
            else:
                return render_template('verify_otp.html', error="Email is invalid and does not exists!", name=user[1])
        else:
            return redirect('/')
    except:
        return render_template('verify_otp.html', error="Server Down try again Later!", name=user[1])

            

# User login logic
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic

            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']

            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM user WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()

            status = user[6]

            if status == 0:

                if request.method == 'POST':
                    # Get the user login form data
                    otp = int(request.form['otp'])


                    if otp == user[5]:
                        cursor.execute('''UPDATE user SET status = ? WHERE id = ?''', (1, user[0]))
                        conn.commit()
                        conn.close()

                        return redirect('/')
                    else:
                        return render_template('verify_otp.html', error="Invalid OTP!", name=user[1])
                
                return render_template('verify_otp.html', name=user[1])
            else:
                return redirect('/')
        else:
            return redirect('/')     
    except:
        return render_template('verify_otp.html', error="Server Down Try Again Later.", name=user[1])

@app.route("/forget_password", methods=["POST","GET"])
def forget_password():
    try:
        if request.method == "POST":
            email = request.form["email"]
            otp = OTP()
            g_mail(email,f"Recover Your Account DevRev Vaccination Booking!", f"Change the Password! \nVerify your Email by entering this OTP to change Password. \n Your OTP is {otp}.")
            return render_template("user_forget_password.html", status = 1, success="OTP sent. Check mail.")
        return render_template("user_forget_password.html", status = 0)
    except:
        return render_template('user_forget_password.html', error = "Email id not found! Please your Email.")
    


@app.route('/admin/send_otp')
def admin_send_otp():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic

            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']

            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()
            otp=OTP()
            cursor.execute('''UPDATE admin SET otp = ? WHERE id = ?''', (otp, user[0]))
            conn.commit()
            conn.close()

            check=g__mail(user_id, f"Welcome to DevRev's Vaccination Booking {user[1]}!", f"Your OTP is {otp}. \n Verify it and Book your Slot Today!")
            if check==1:
                return render_template('admin_otp.html', success="OTP Sent! Check Mail!", name=user[1])
            else:
                return render_template('admin_otp.html', error="Email is invalid and does not exists!", name=user[1])
        else:
            return redirect('/')
    except:
        return render_template('admin_otp.html', error="Server Down try again Later!", name=user[1])

            

# User login logic
@app.route('/admin/verify_otp', methods=['GET', 'POST'])
def admin_verify_otp():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic

            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']

            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()

            status = user[6]

            if status == 0:

                if request.method == 'POST':
                    # Get the user login form data
                    otp = int(request.form['otp'])


                    if otp == user[5]:
                        cursor.execute('''UPDATE admin SET status = ? WHERE id = ?''', (1, user[0]))
                        conn.commit()
                        conn.close()

                        return redirect('/admin/dashboard')
                    else:
                        return render_template('admin_otp.html', error="Invalid OTP!", name=user[1])
                
                return render_template('admin_otp.html', name=user[1])
            else:
                return redirect('/admin/login')
        else:
            return redirect('/admin/login')     
    except:
        return render_template('admin_otp.html', error="Server Down Try Again Later.", name=user[1])


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
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

           # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT name FROM Vacc_Center")
            centers = cursor.fetchall()
            # print(centers)
            cursor.execute("SELECT DISTINCT place FROM Vacc_Center")
            places = cursor.fetchall()
            # print(places)
            cursor.execute("SELECT DISTINCT slot_timing FROM Slots")
            hours = cursor.fetchall()
            # print(hours)
            cursor.execute("SELECT DISTINCT date FROM Slots")
            dates = cursor.fetchall()
            # print(dates)

            cursor.execute("SELECT * FROM User WHERE email_id = ?",(user_id,))
            user = cursor.fetchone() 

            status = user[6]
            if status == 0:
                return redirect('/verify_otp')
            name=user[1]
            print("slot :", user)

            # Check if the search form is submitted
            if request.method == 'POST':
                center = request.form['center']
                place = request.form['place']
                hour = request.form['hour']
                date = request.form['date']


                # Query the database to fetch the rows matching the selected criteria
                if center == "No Filter" and hour == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots")
                elif center == "No Filter" and hour == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE date = ?", (date,))
                elif center == "No Filter" and hour == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE place = ?", (place,))
                elif center == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ?", (hour,))
                elif hour == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ?", (center,))
                elif center == "No Filter" and hour == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE place = ? AND date = ?", (place, date))
                elif center == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND date = ?", (hour, date))
                elif center == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ?", (hour, place))
                elif hour == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND date = ?", (center, date))
                elif hour == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ?", (center, place))
                elif place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ?", (center, hour))
                elif center == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ? AND date = ?", (hour, place, date))
                elif hour == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ? AND date = ?", (center, place, date))
                elif place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND date = ?", (center, hour, date))
                elif date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ?", (center, hour, place))
                else:
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ? AND date = ?", (center, hour, place, date))

                rows = cursor.fetchall()
                # Close the connection and cursor
                cursor.close()
                conn.close()

                # Render the template with the search results
                return render_template('user_dash.html', show_logout=True, centers=centers, places=places, hours = hours, dates=dates, rows=rows, name=name)

            # Close the connection and cursor
            cursor.close()
            conn.close()

            return render_template('user_dash.html', show_logout=True, centers=centers, places=places, hours = hours, dates=dates, name= name)
        else:
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

           # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT name FROM Vacc_Center")
            centers = cursor.fetchall()
            # print(centers)
            cursor.execute("SELECT DISTINCT place FROM Vacc_Center")
            places = cursor.fetchall()
            # print(places)
            cursor.execute("SELECT DISTINCT slot_timing FROM Slots")
            hours = cursor.fetchall()
            # print(hours)
            cursor.execute("SELECT DISTINCT date FROM Slots")
            dates = cursor.fetchall()
            # print(dates)
            # Check if the search form is submitted
            if request.method == 'POST':
                center = request.form['center']
                place = request.form['place']
                hour = request.form['hour']
                date = request.form['date']

                print("This is debugging",center,place,hour,date)

                # Query the database to fetch the rows matching the selected criteria
                if center == "No Filter" and hour == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots")
                elif center == "No Filter" and hour == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE date = ?", (date,))
                elif center == "No Filter" and hour == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE place = ?", (place,))
                elif center == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ?", (hour,))
                elif hour == "No Filter" and place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ?", (center,))
                elif center == "No Filter" and hour == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE place = ? AND date = ?", (place, date))
                elif center == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND date = ?", (hour, date))
                elif center == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ?", (hour, place))
                elif hour == "No Filter" and place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND date = ?", (center, date))
                elif hour == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ?", (center, place))
                elif place == "No Filter" and date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ?", (center, hour))
                elif center == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ? AND date = ?", (hour, place, date))
                elif hour == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ? AND date = ?", (center, place, date))
                elif place == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND date = ?", (center, hour, date))
                elif date == "No Filter":
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ?", (center, hour, place))
                else:
                    cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ? AND date = ?", (center, hour, place, date))

                rows = cursor.fetchall()

                # Close the connection and cursor
                cursor.close()
                conn.close()

                # Render the template with the search results
                return render_template('home.html', show_logout=False, centers=centers, places=places, hours = hours, dates=dates, rows=rows)

            # Close the connection and cursor
            cursor.close()
            conn.close()
            
    # User is not logged in, redirect to the home page
            return render_template('home.html', show_logout=False, centers=centers, places=places, hours = hours, dates=dates)
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
            conn.execute('PRAGMA foreign_keys = ON;')
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
            conn.execute('PRAGMA foreign_keys = ON;')
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
            return render_template("admin_login.html", error="Invalid Credntials!!")
    except:
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user login form
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # User is logged in, perform required logic
            
            # Retrieve the user from the database using session['user_id']
            user_id = session['user_id']
            
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
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

                # Retrieve the admin data from the database
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

                center_details = '''
                SELECT * FROM Vacc_Center WHERE admin_id = ?
                '''
                cursor.execute(center_details, (int(user[0]),))
                center_details = cursor.fetchall()
                

                # Retrieve the user data from the database
                table_query = '''
                SELECT * FROM User
                '''
                cursor.execute(table_query)
                table_data3 = cursor.fetchall()

                table_query5= '''SELECT * FROM Slots'''
                cursor.execute(table_query5)
                table_data5 = cursor.fetchall()

                table_data4=[]

                for i in range(len(center_details)):

                    # Retrieve the slot timing data from the database
                    table_query = '''
                    SELECT * FROM slots_timing WHERE center_id = ?
                    '''
                    cursor.execute(table_query, (center_details[i][0],))
                    table_data4.append(cursor.fetchall())

                # Query the database to fetch the list of vaccination centers
                cursor.execute("SELECT DISTINCT name FROM Vacc_Center")
                centers = cursor.fetchall()
                # print(centers)
                cursor.execute("SELECT DISTINCT place FROM Vacc_Center")
                places = cursor.fetchall()
                # print(places)
                cursor.execute("SELECT DISTINCT slot_timing FROM Slots")
                hours = cursor.fetchall()
                # print(hours)
                cursor.execute("SELECT DISTINCT date FROM Slots")
                dates = cursor.fetchall()
                # print(dates)

                # Check if the search form is submitted
                if request.method == 'POST':
                    center = request.form['center']
                    place = request.form['place']
                    hour = request.form['hour']
                    date = request.form['date']

                    print("This is debugging",center,place,hour,date)

                    # Query the database to fetch the rows matching the selected criteria
                    if center == "No Filter" and hour == "No Filter" and place == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots")
                    elif center == "No Filter" and hour == "No Filter" and place == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE date = ?", (date,))
                    elif center == "No Filter" and hour == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE place = ?", (place,))
                    elif center == "No Filter" and place == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE slot_timing = ?", (hour,))
                    elif hour == "No Filter" and place == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ?", (center,))
                    elif center == "No Filter" and hour == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE place = ? AND date = ?", (place, date))
                    elif center == "No Filter" and place == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND date = ?", (hour, date))
                    elif center == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ?", (hour, place))
                    elif hour == "No Filter" and place == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND date = ?", (center, date))
                    elif hour == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ?", (center, place))
                    elif place == "No Filter" and date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ?", (center, hour))
                    elif center == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE slot_timing = ? AND place = ? AND date = ?", (hour, place, date))
                    elif hour == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND place = ? AND date = ?", (center, place, date))
                    elif place == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND date = ?", (center, hour, date))
                    elif date == "No Filter":
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ?", (center, hour, place))
                    else:
                        cursor.execute("SELECT * FROM Slots WHERE center_name = ? AND slot_timing = ? AND place = ? AND date = ?", (center, hour, place, date))

                    table_data5 = cursor.fetchall()

                


                
                # Close the connection and cursor
                cursor.close()
                conn.close()
                
                return render_template('admin_dash.html', name=name, table_data=table_data, table_data2=table_data2, 
                                       table_data3=table_data3, table_data4=table_data4, table_data5=table_data5,
                                       centers=centers, places=places, hours = hours, dates=dates)
            else:
                # Display user-specific information or perform other operations
                status = user[6]
                if status == 0:
                    return redirect('/admin/verify_otp')
                # Example: Get the user's name
                name = user[1]  # Assuming the name is stored in the 2nd column
                id = user[0]
                center_query = '''
                SELECT * FROM Vacc_Center WHERE admin_id = ?
                '''
                
                center_details = '''
                SELECT * FROM Vacc_Center WHERE admin_id = ?
                '''
                cursor.execute(center_details, (int(user[0]),))
                center_details = cursor.fetchall()
                # print(center_details)

                table_data4=[]
                for i in range(len(center_details)):

                    # Retrieve the slot timing data from the database
                    table_query = '''
                    SELECT * FROM slots_timing WHERE center_id = ?
                    '''
                    cursor.execute(table_query, (center_details[i][0],))
                    table_data4.append(cursor.fetchall())

                # print(table_data4)

                cursor.execute(center_query, (id,))
                table_data = cursor.fetchall()
                
                # Close the connection and cursor
                cursor.close()
                conn.close()
                print("working fine")
                
                return render_template('vacc_center.html', name=name, table_data=table_data, table_data4=table_data4)
        else:
            return redirect('/admin/login')
        
    except Exception as e:
        print("Isuue is raising here in admin dashboard", e)
        return "Ran into Some Issues, go back and Try Again."


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
            conn.execute('PRAGMA foreign_keys = ON;')
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

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
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
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO user ( name, email_id, password, ph_no, otp, date) VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (name, email, hashed_password, ph_no, otp, curr_date()))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()

            g_mail(email,f"Welcome to DevRev's Vaccination Booking {name}!", f"Book your slot Today! \nVerify your Email by entering this OTP once you LogIn. \n Your OTP is {otp}.")
            
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

@app.route('/admin/remove_user/<int:id>', methods=['GET', 'POST'])
def remove_user(id):
    try:
        if request.method == 'POST':
            # Delete the admin with the given ID from the database
            connection = sqlite3.connect('vaccination.db')
            cursor = connection.cursor()
            
            try:
                cursor.execute("DELETE FROM user WHERE id = ?", (id,))
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
            slot_vaccine=request.form['per_slot']
            vacc_name=request.form['vacc_name']

            
            
            # Perform add center logic here
            conn = sqlite3.connect('vaccination.db')
            conn.execute('PRAGMA foreign_keys = ON;')
            cursor = conn.cursor()

            user_query = '''
            SELECT * FROM Admin WHERE email_id = ?
            '''
            cursor.execute(user_query, (admin_email_id,))
            user = cursor.fetchone()
            
            
            insert_user_query = '''
            INSERT INTO Vacc_Center (name, place, working_hour, dosage, slots, slot_vaccine, vaccine_name, date, admin_id, admin_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (center_name, place, working_hour, dosage, slots, slot_vaccine, vacc_name, curr_date(), user[0], user[1]))
            conn.commit()
            # print("not working")
            


            dates = next_n_days(math.ceil(int(dosage)/(int(slots)*int(slot_vaccine))))

            cursor.execute("SELECT * FROM Vacc_Center where name = ? AND admin_id = ?", (center_name, user[0]))
            table_data2 = cursor.fetchall()

            for i in range(int(slots)):
                cursor.execute('''INSERT INTO slots_timing (center_id, center_name) VALUES (?,?)''', (table_data2[0][0],center_name,))
                conn.commit()
            
            cursor.execute("Select * FROM slots_timing where center_id = ?", (table_data2[0][0],))
            slot_timing_ids = cursor.fetchall()
            print(slot_timing_ids)

            for i in range(int(dosage)):
                insert_user_query= '''
                        INSERT INTO Slots (center_id, center_name, slot_timing_id, date, place) VALUES (?,?,?,?,?)
                        '''
                cursor.execute(insert_user_query, (table_data2[0][0],center_name,slot_timing_ids[(i//int(slot_vaccine))%int(slots)][0],dates[i//(int(slots)*int(slot_vaccine))], place))
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

@app.route('/admin/edit_time/<int:admin_id>', methods=['GET', 'POST'])
def edit_time(admin_id):
    try:
        if request.method == 'POST':
            # Delete the vaccination center with the given ID from the database
            connection = sqlite3.connect('vaccination.db')
            cursor = connection.cursor()
            slot_timing = request.form.get('slot_timing')
            if slot_timing:
            
                try:
                    cursor.execute('UPDATE slots_timing SET slot_timing = ? WHERE id = ?', (slot_timing, admin_id))
                    connection.commit()
                    flash('Vaccination center successfully removed')
                except sqlite3.Error as e:
                    connection.rollback()
                    flash('An error occurred while removing the vaccination center')
                    print('SQLite error occurred:', e.args[0])

                connection.close()
                return jsonify(success=True)
            else:
                return jsonify(success=False, error='Invalid slot timing')

    except:
        return "Ran into Some Issues go back and Try Again."

    return redirect('/admin/dashboard')  # Redirect to the admin page after deleting


@app.route('/book-slot', methods=['POST'])
def book_slot():
    if 'user_id' in session:            
        email_id = session['user_id']
        center_id = request.json['center_id']
        conn = sqlite3.connect('vaccination.db')
        conn.execute('PRAGMA foreign_keys = ON;')
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
