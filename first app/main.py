from flask import Flask,render_template,request, flash, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.utils import secure_filename
import os


# Define the allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/assets/img/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

class Posts(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(80), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


@app.route("/")
def home():
    posts=Posts.query.filter_by().all()
    # Get all unique categories
    categories = db.session.query(Posts.category).distinct().all()

    # print(categories)

    # Create a dictionary to store posts for each category
    category_posts = {}

    # Fetch posts for each category
    for category in categories:
        category_name = category[0]
        # print(Posts.query.filter_by(category=category_name).all())
        category_posts[category_name] = Posts.query.filter_by(category=category_name).all()

    print(category_posts)

    return render_template('index.html',params=params,posts=posts, categories=categories, category_posts=category_posts)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):

    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('single-post.html',params=params,post=post)

@app.route("/edit/<string:id>", methods=['GET', 'POST'])
@app.route("/edit", defaults={'id': None} ,methods=['GET', 'POST'])
def edit_route(id):
    if 'user' in session and session['user'] == 'admin':
        # To Add New post
        if id is None:
            if request.method == 'POST':
                input_title = request.form.get('title')
                input_slug = request.form.get('slug')
                input_category = request.form.get('category')
                input_content = request.form.get('Content')

                # Handle file upload
                if 'img_url' in request.files:
                    file = request.files['img_url']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        img_url = os.path.join('static/assets/img', filename)
                        file.save(os.path.join(app.static_folder, 'assets/img', filename))
                    else:
                        img_url = None
                else:
                    img_url = None

            
                # Add new post
                post = Posts(title=input_title, slug=input_slug, content=input_content, category=input_category,img_url=filename)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('dashboard'))
            else:
                return render_template('edit-post.html', params=params)
        #To edit post        
        else:

            if request.method == 'POST':
                post=Posts.query.filter_by(id=id).first()
                


                # Check if a new image was uploaded
                if 'img_url' in request.files:
                    new_img = request.files['img_url']

                    # Check if the file has a name and is allowed
                if new_img.filename and allowed_file(new_img.filename):
                    filename = secure_filename(new_img.filename)

                    # Delete the old image if it exists
                    if post.img_url:
                        old_img_path = os.path.join('static/assets/img', post.img_url)
                        if os.path.exists(old_img_path):
                            os.remove(old_img_path)

                    # Save the new image to the upload folder
                    new_img.save(os.path.join('static/assets/img', filename))

                    # Update the post with the new image filename
                    post.img_url = filename
                else:
                    # No new image uploaded, keep the existing one
                    post = Posts.query.filter_by(id=id).first()

                post.title=request.form.get('title')
                post.slug=request.form.get('slug')
                post.category=request.form.get('category')
                post.content=request.form.get('Content')

                db.session.add(post)
                db.session.commit()
                return redirect(url_for('dashboard'))
            else:
                post=Posts.query.filter_by(id=id).first()
                return render_template('edit-post.html', params=params,post=post)
            

    return "Unauthorized", 401


@app.route("/delete/<int:id>")
def delete_post(id):
    if 'user' in session and session['user'] == 'admin':
        post = Posts.query.get(id)

        if post:

           
            # Delete the image file
            if post.img_url:
                img_path = os.path.join(app.static_folder, 'assets', 'img', post.img_url)
                if os.path.exists(img_path):
                    os.remove(img_path)

            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully!', 'success')
        else:
            flash('Post not found!', 'danger')

        return redirect(url_for('dashboard'))
    
    return "Unauthorized", 401


@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/dashboard")
def dashboard():
    posts=Posts.query.filter_by().all()
    return render_template('dashboard.html',params=params,posts=posts)

@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html',params=params)

@app.route("/login",methods=['GET','POST'])
def login():
    if 'user' in session and  session['user']=='admin':
        return redirect(url_for('dashboard'))
        
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user']=username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')


    return render_template('login.html',params=params)

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