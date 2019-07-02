from flask import Flask, request, redirect
import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/validate-info")
def index():

    template = jinja_env.get_template('form.html')
    return template.render()

@app.route('/validate-info', methods=['POST'])
def validate_info():
    username = request.form['username']  
    password = request.form['password']
    passwordtwo = request.form['passwordtwo']
    email = request.form['email']

    username_error = ''
    password_error = ''
    passwordtwo_error = ''
    email_error = ''

    if username == '':
        username_error = "That's not a valid username"
        if len(username) < 3 or len(username) > 20:
          username_error = "That's not a valid username" 
          username = ''
          password = ''
          passwordtwo = ''

    if password == '' and passwordtwo == '':
        password_error = "That's not a valid password"
        passwordtwo_error = "Passwords don't match"
        password = ''
        passwordtwo = ''

    if username != '' and password != '' and passwordtwo == '':
        passwordtwo_error = "Passwords don't match"
        password = ''
        passwordtwo = ''

    if len(password) < 3 or len(password) > 20:
        password_error = "That's not a valid password"
        password = ''
        passwordtwo = ''

    if re.search(' ', password):
        password_error = "That's not a valid password"
        password = ''
        passwordtwo = ''

    if username != '' and password != '' and passwordtwo != '' and re.search('@', email) is None or re.search('.', email) is None or re.search(' ', email):
        email_error = "Invalid Email"
        password = ''
        passwordtwo = ''
    if username != '' and password != '' and passwordtwo == '' and re.search('@', email) or re.search('.', email) or re.search(' ', email):
        passwordtwo_error = "Passwords don't match"
        password = ''
        passwordtwo = ''
    if not username_error and not password_error and not passwordtwo_error and not email_error:
        greet_user = username
        return redirect('/valid_info?greet_user={0}'.format(greet_user))
    else:    
        template = jinja_env.get_template('form.html')
        return template.render(username=username, password=password, passwordtwo=passwordtwo, email=email, username_error=username_error, 
        password_error=password_error, passwordtwo_error=passwordtwo_error, email_error=email_error)

@app.route('/valid_info')
def valid_info():
    greet_user = request.args.get('greet_user')
    return "<h1> Welcome, {0}</h1>".format(greet_user)
    
app.run()