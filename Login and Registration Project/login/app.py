from flask import Flask,render_template,request,redirect,url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import logging
import re

app=Flask(__name__)

app.secret_key='f5a1c200730b983ea35af4bbcff9748f'



# Use environment variables for database configuration
app.config['MYSQL_HOST'] = os.environ.get('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('DB_NAME', 'login')
mysql = MySQL(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/",methods=['GET'])
def home():
    logged_in = session.get('loggedin', False)
    msg = session.get('username', '') if logged_in else ''
    return render_template('index.html', msg=msg)


@app.route("/login",methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username= % s AND password = % s', (username, password, ))
        account=cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html',msg=msg)
        else:
            msg= 'Incorrect username/passowrd !'
    return render_template('login.html',msg=msg)

        
@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/register",methods=['GET','POST'])
def register():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email= request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg ='You have successfully registered !'    
            
            flash(msg, 'success')  # Flash the success message
    elif request.method=='POST':
        msg='Please fill out the form !'
    return render_template('register.html', msg=msg)        


app.run(host='0.0.0.0', port=5000)
