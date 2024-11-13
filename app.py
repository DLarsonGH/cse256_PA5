# Donald Larson
# CIS256 Fall 2024
# Programming 5
"""
This file demonstrates a Flask-based login application.
"""

from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

users = {
    "Alex": bcrypt.generate_password_hash("Alex1234"),
    "Bill": bcrypt.generate_password_hash("Bill1234"),
    "Chaz": bcrypt.generate_password_hash("Chaz1234"),
    "test_user_CSE": bcrypt.generate_password_hash("testPassword123"),
}


# Route to display the login form
@app.route('/login', methods=['GET'])
def login_form():
    form_html = '''
    <form method="POST" action="/login">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <input type="submit" value="Login">
    </form>
    '''
    return render_template_string(form_html)


# Add home route
@app.route('/')
def index():
    return 'Programming 5 app is running!'


# Route to handle form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Handle the login logic here
    if username in users:
        if bcrypt.check_password_hash(users[username], password):
            ret_string = f'Username: {username}. Password: {users[username]}'
        else:
            ret_string = f'Invalid password for username: {username}.'
    else:
        ret_string = f'Unknown username: {username}.'
    return ret_string


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
