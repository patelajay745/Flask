from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + "/todo.db"  # Include the correct path here

db = SQLAlchemy(app)

from flask_migrate import Migrate

migrate = Migrate(app, db)

from app import routes, models