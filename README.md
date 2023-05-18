# Vaccination-Booking
A Web Application for covid vaccination booking using Flask framework.

# TODO List for COVID Vaccination Booking Web Application

## Backend Setup
1. Create a new Replit project for your application.
2. Initialize a new Git repository in your Replit project.
3. Connect your Replit project to a GitHub repository for backup and version control.
4. Set up a virtual environment for the project.
   - Run the command: `python3 -m venv venv`
   - Activate the virtual environment:
     - For Windows: `venv\Scripts\activate`
     - For Linux/Mac: `source venv/bin/activate`
5. Install Flask and SQLite packages in the virtual environment:
   - Run the command: `pip install flask sqlite3`

## Database Setup
1. Create a new file called `database.py` in your Replit project.
2. Import the required packages (`sqlite3`).
3. Create a connection to the SQLite database and a cursor object.
4. Write SQL queries to create the necessary tables for the application.
   - User table: id, username, email-id, password
   - VaccinationCenter table: id, name, working_hours, gps_location
   - Slot table: id, center_id, date, capacity, available_slots, user_names.
5. Commit the changes and push them to your GitHub repository for backup.

## Rough Wireframe for Each Page
1. Home.html
   ![Home](https://github.com/Samuel-2552/Vaccination-Booking/assets/104893913/128f2ce2-4f40-40ce-b276-6ef9e21da247)


## Flask App Setup
1. Create a new file called `app.py` in your Replit project.
2. Import the required packages (`flask`, `sqlite3`).
3. Initialize a Flask application object.
4. Create a route for the home page ('/') and a function to render it.
5. Create routes and functions for user-related use cases:
   - Sign up ('/signup')
   - Login ('/login')
   - Searching for Vaccination Centre and working hours ('/search')
   - Apply for a vaccination slot ('/apply')
   - Logout ('/logout')
6. Create routes and functions for admin-related use cases:
   - Admin login ('/admin/login')
   - Add Vaccination Centres ('/admin/add_centre')
   - Get dosage details ('/admin/dosage_details')
   - Remove vaccination centres ('/admin/remove_centre')
7. Run the Flask application:
   - Set the `FLASK_APP` environment variable: `export FLASK_APP=app.py`
   - Start the server: `flask run`

## User-related Functionality
1. Implement the sign-up functionality.
   - Create a template file called `signup.html` in your Replit project.
   - Define a function in `app.py` to handle the sign-up route.
   - Extract the form data from the request and insert it into the User table in the database.
2. Implement the login functionality.
   - Create a template file called `login.html` in your Replit project.
   - Define a function in `app.py` to handle the login route.
   - Verify the user's credentials against the User table in the database.
3. Implement the searching functionality.
   - Create a template file called `search.html` in your Replit project.
   - Define a function in `app.py` to handle the search route.
   - Retrieve the vaccination centers and their working hours from the VaccinationCenter table.
   - Pass the data to the template for rendering.
4. Implement the slot application functionality.
   - Create a template file called `apply.html` in your Replit project.
   - Define a function in `app.py` to handle the apply route.
   - Retrieve the selected vaccination center and date from the request.
   - Check if the slot capacity for the selected date is available and update the Slot table accordingly.
   - Display a success message or an error message to the user.
5. Implement the logout functionality.
   - Define a function in `app.py` to handle the logout route.
   - Clear the user's session data and redirect them to the login page.

## Admin-related Functionality
1. Implement the admin login functionality.
   - Create a template file called `admin_login.html` in your Replit project.
   - Define a function in `app.py` to handle the admin login route.
   - Verify the admin's credentials against a separate table in the database.
2. Implement the vaccination center addition functionality.
   - Create a template file called `add_centre.html` in your Replit project.
   - Define a function in `app.py` to handle the add center route.
   - Extract the form data from the request and insert it into the VaccinationCenter table in the database.
3. Implement the dosage details functionality.
   - Create a template file called `dosage_details.html` in your Replit project.
   - Define a function in `app.py` to handle the dosage details route.
   - Retrieve the dosage details by grouping the Slot table based on vaccination centers.
   - Pass the data to the template for rendering.
4. Implement the vaccination center removal functionality.
   - Create a template file called `remove_centre.html` in your Replit project.
   - Define a function in `app.py` to handle the remove center route.
   - Delete the selected vaccination center from the VaccinationCenter table in the database.
5. Secure admin routes.
   - Use decorators or middleware to restrict access to admin-related routes only for authenticated admin users.

## UI Improvements
1. Create HTML templates for all the routes mentioned in the previous steps and store them in your Replit project.
2. Style the templates using CSS to provide a better user experience.
3. Add appropriate form validations on the frontend using JavaScript.

## Testing and Deployment
1. Test the application by running it in your Replit project and going through all the use cases.
2. Once the application is working as expected, commit and push the final changes to your GitHub repository.
3. Set up automatic deployment from your GitHub repository to Replit.
4. Monitor the deployed application for any errors or issues and make necessary adjustments if required.

Note: The above steps may change with respect to the changes in the websites to implement the COVID Vaccination Booking Web Application. It is recommended to refer to Flask, SQLite and Replit documentation for more detailed information on how to implement each step.
