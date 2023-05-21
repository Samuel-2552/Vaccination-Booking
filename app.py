from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'ghf5yr7698iyf5463fhgfytytr9'  # Set a secret key for session encryption



# User signup logic
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    try:
        if request.method == 'POST':
            # Get the user signup form data
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination_app.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO User (name, email_id, password) VALUES (?, ?, ?)
            '''
            cursor.execute(insert_user_query, (name, email, hashed_password))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()
            
            # Redirect to the login page after successful signup
            return redirect('/login')
    except:
        return "Ran into Some Issues go back and Try Again."
    
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
            conn = sqlite3.connect('vaccination_app.db')
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
            return "Invalid credentials"
    except:
        return "Ran into Some Issues go back and Try Again."
    
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
            conn = sqlite3.connect('vaccination_app.db')
            cursor = conn.cursor()

            # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT center_name FROM VaccinationCenter")
            centers = cursor.fetchall()

            cursor.execute("SELECT DISTINCT working_hour FROM VaccinationCenter")
            hours = cursor.fetchall()

            cursor.execute("SELECT * FROM User WHERE email_id = ?",(user_id,))
            user = cursor.fetchone() 
            name=user[1]

            # Check if the search form is submitted
            if request.method == 'POST':
                center = request.form['center']
                hour = request.form['hour']

                # Query the database to fetch the rows matching the selected criteria
                cursor.execute("SELECT * FROM VaccinationCenter WHERE center_name = ? OR working_hour = ?", (center, hour))
                rows = cursor.fetchall()
                

                # Close the connection and cursor
                cursor.close()
                conn.close()

                # Render the template with the search results
                return render_template('home.html', show_logout=True, vaccination_centers=centers, hours=hours, rows=rows, name=name)

            # Close the connection and cursor
            cursor.close()
            conn.close()

            return render_template('home.html', show_logout=True, vaccination_centers=centers, hours=hours, name= name)
        else:
            # Create a new connection and cursor
            conn = sqlite3.connect('vaccination_app.db')
            cursor = conn.cursor()

            # Query the database to fetch the list of vaccination centers
            cursor.execute("SELECT DISTINCT center_name FROM VaccinationCenter")
            centers = cursor.fetchall()

            cursor.execute("SELECT DISTINCT working_hour FROM VaccinationCenter")
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
            conn = sqlite3.connect('vaccination_app.db')
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
            conn = sqlite3.connect('vaccination_app.db')
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
            conn = sqlite3.connect('vaccination_app.db')
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
                SELECT * FROM VaccinationCenter
                '''
                cursor.execute(table_query2)
                table_data2 = cursor.fetchall()
                
                # Close the connection and cursor
                cursor.close()
                conn.close()
                
                return render_template('admin_dash.html', name=name, table_data=table_data, table_data2=table_data2)
        
        if user:
            # Display user-specific information or perform other operations
            
            # Example: Get the user's name
            name = user[1]  # Assuming the name is stored in the 2nd column

            center_query = '''
            SELECT * FROM VaccinationCenter WHERE admin_email_id = ?
            '''
            cursor.execute(center_query, (user_id,))
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
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Perform user signup logic here
            conn = sqlite3.connect('vaccination_app.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO Admin (id, name, email_id, password) VALUES (?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (id, name, email, hashed_password))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()
            
            # Redirect to the login page after successful signup
            return  redirect('/admin/dashboard')
    except:
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user signup form
    return redirect('/admin/dashboard')


@app.route('/admin/remove/<int:id>', methods=['GET', 'POST'])
def remove_admin(id):
    try:
        if request.method == 'POST':
            # Delete the admin with the given ID from the database
            connection = sqlite3.connect('vaccination_app.db')
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
            
            # Perform add center logic here
            conn = sqlite3.connect('vaccination_app.db')
            cursor = conn.cursor()
            
            insert_user_query = '''
            INSERT INTO VaccinationCenter (admin_email_id, place, center_name, dosage, working_hour) VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_user_query, (admin_email_id, place, center_name, dosage, working_hour))
            conn.commit()
            
            # Close the connection
            cursor.close()
            conn.close()
            
            # Redirect to the login page after successful signup
            return  redirect('/admin/dashboard')
        
    except:
        return "Ran into Some Issues go back and Try Again."
    
    # Render the user signup form
    return redirect('/admin/dashboard')


@app.route('/admin/remove_center/<int:center_id>', methods=['GET', 'POST'])
def remove_center(center_id):
    try:
        if request.method == 'POST':
            # Delete the vaccination center with the given ID from the database
            connection = sqlite3.connect('vaccination_app.db')
            cursor = connection.cursor()
            
            try:
                cursor.execute("DELETE FROM VaccinationCenter WHERE center_id = ?", (center_id,))
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
