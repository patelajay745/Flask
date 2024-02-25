from flask import Flask,render_template,request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)


with open('config.json','r')as c:
    params=json.load(c)["params"]

if bool(params['local_server']):
    app.secret_key ="410cdca69e7974296cd526eb9e9765a1cbe7aff7432fa29b"

    userpass = 'mysql+pymysql://root:@'
    basedir  = '127.0.0.1'
    dbname   = '/'+ params['dbname']
    socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    dbname   = dbname + socket
    app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_uri']

db = SQLAlchemy(app)

class Contact(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)

@app.route("/")
def home():
    return render_template('index.html',params=params)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':

        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        subject=request.form.get('subject')

        entry=Contact(name=name,email=email,message=message,subject=subject)

        db.session.add(entry)
        db.session.commit()

        

        flash('Your message has been sent. Thank you!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html',params=params)

@app.route("/single-post")
def singlePost():
    return render_template('single-post.html',params=params)



app.run(debug=True)