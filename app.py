# Donald Larson
# CIS256 Fall 2024
# Programming 5
"""
This file demonstrates a Flask-based login application.
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)


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
    return f'Username: {username}. Password: {password}'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
