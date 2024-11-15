# Donald Larson
# CIS256 Fall 2024
# Programming 5
"""
This file demonstrates a Flask-based user login application.  A simple in-memory
dictionary is used as the credential database.  Three routes are implemented:

route('/')
Prints a greeting and provides links to login or registration pages.

route('/login')
Prompts user to enter a username and password.  Looks up username and compares
the entered password with the stored hashed value.  Reports if the username
is not in the dictionary or if the password does not match the hashed value.

route('/register')
Prompts user to enter a new username and password (entered twice) to be added
to the user dictionary.  Validates that the selected username is not already
in use and that the username and password meet various basic security practices
such as minimal length, etc.
"""

from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt
# Regular expression support
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Define user dictionary with initial set of members for test purposes
users = {
    "Alex": bcrypt.generate_password_hash("Alex1234"),
    "Bill": bcrypt.generate_password_hash("Bill1234"),
    "Chaz": bcrypt.generate_password_hash("Chaz1234"),
    "test_user": bcrypt.generate_password_hash("TestPassword123"),
}


# Route to display the login form
@app.route('/login', methods=['GET'])
def login_form():
    form_html = '''
    <h2>Login to your account.</h2>
    <p>New user?  Click here to 
    <a href="http://localhost:5000/register">register</a>.</p><br>
    <form method="POST" action="/login">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''
    return render_template_string(form_html)


# Route to display the register form
@app.route('/register', methods=['GET'])
def register_form():
    form_html = '''
    <h2>Register for a user account.</h2>
    <p>Username must contain letters and numbers only.</p>
    <p>Password must be 8 or more characters long and contain both letters and
    numbers.  Repeat password choice to confirm.</p>
    <p>Have an existing account?  Click here to 
    <a href="http://localhost:5000/login">login</a>.</p><br>
    <form method="POST" action="/register">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <label for="password">Confirm:</label><br>
        <input type="password" id="password2" name="password2"><br>
        <input type="submit" value="Register">
    </form>
    '''
    return render_template_string(form_html)


# Add home route
@app.route('/')
def index():
    return '<h2>Welcome!</h2>' \
        + '<p>New user?  Click here to ' \
        + '<a href="http://localhost:5000/register">register</a>.</p>' \
        + '<p>Have an existing account?  Click here to ' \
        + '<a href="http://localhost:5000/login">login</a>.</p>'


# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Handle the login logic here
    # Check for username in dictionary
    if username in users:
        # Username good, test password
        if bcrypt.check_password_hash(users[username], password):
            # All good, return username/password string
            ret_string = f'Username: {username}. Password: {users[username]}'\
                         + '\nlogin confirmed.'
        else:
            # Wrong password
            ret_string = f'Invalid password for username: {username}. '\
                         + '<a href="http://localhost:5000/login">Retry.</a>'
    else:
        # Username is not in dictionary
        ret_string = f'Unknown username: {username}. '\
                     + '<a href="http://localhost:5000/login">Retry.</a>'
    return ret_string


# Constant for enforcing minimum password length
MIN_PWD_LENGTH = 8


# Route to handle register form submission
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    # Perform validation checks on entered username and password
    if len(username) == 0:
        # Textbox is empty
        ret_string = f'No username entered. '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    elif username in users:
        # The username is already taken
        ret_string = f'Username: \"{username}\" is already in use. '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    elif not username.isalnum():
        # The username contains a non-alphanumeric character
        ret_string = f'Invalid username. \"{username}\" contains special character(s). '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    elif len(password) < MIN_PWD_LENGTH:
        # The password is too short
        ret_string = f'Password must be at least {MIN_PWD_LENGTH} characters. '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    elif not (re.search(r'[a-zA-Z]', password)
              and re.search(r'\d', password)):
        # Password doesn't contain both letters and numbers
        ret_string = f'Password must contain both letters and numbers. '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    elif password != password2:
        # Password confirmation fails, strings do not match
        ret_string = f'Entered passwords do not match. '\
                     + '<a href="http://localhost:5000/register">Retry.</a>'
    else:
        # username and password are both good. Add to dictionary.
        users.update({username: bcrypt.generate_password_hash(password)})
        ret_string = f'Username: \"{username}\" registered.  Go to login '\
                     + '<a href="http://localhost:5000/login">here.</a>'
    return ret_string


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
