from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'ghf5yr7698iyf5463fhgfytytr9'  # Set a secret key for session encryption



# User signup logic
@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
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
    
    # Render the user signup form
    return render_template('signup.html')

# User login logic
@app.route('/login', methods=['GET', 'POST'])
def user_login():
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
    
    # Render the user login form
    return render_template('login.html')

@app.route('/')
def home():
    # Check if the user is logged in
    if 'user_id' in session:
        # User is logged in, perform required logic
        
        # Retrieve the user from the database using session['user_id']
        user_id = session['user_id']
        
        # Create a new connection and cursor
        conn = sqlite3.connect('vaccination_app.db')
        cursor = conn.cursor()
        
        user_query = '''
        SELECT * FROM User WHERE email_id = ?
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
            
            return f"Welcome, {name}!"
    
    # User is not logged in, redirect to home page

    return render_template('home.html')

# Logout
@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect('/login')

#admin login logic
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
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
            
            return f"Welcome, {name}!"
        
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
    
    # Render the user login form
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
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
            
            return f"Welcome, {name}!"
    
    # User is not logged in, redirect to home page

    return render_template('home.html')

@app.route('/search')
def search():
    # Search logic
    return "Search page"

@app.route('/apply')
def apply():
    # Apply logic
    return "Apply page"

@app.route('/admin/add_centre')
def add_centre():
    # Add Vaccination Centres logic
    return "Add Vaccination Centres page"

@app.route('/admin/dosage_details')
def dosage_details():
    # Get dosage details logic
    return "Get dosage details page"

@app.route('/admin/remove_centre')
def remove_centre():
    # Remove vaccination centres logic
    return "Remove vaccination centres page"

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
