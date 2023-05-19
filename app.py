from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    # Signup logic
    return "Signup page"

@app.route('/login')
def login():
    # Login logic
    return "Login page"

@app.route('/search')
def search():
    # Search logic
    return "Search page"

@app.route('/apply')
def apply():
    # Apply logic
    return "Apply page"

@app.route('/logout')
def logout():
    # Logout logic
    return "Logout page"

@app.route('/admin/login')
def admin_login():
    # Admin login logic
    return "Admin login page"

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
