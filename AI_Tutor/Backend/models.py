from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String, nullable=False)
    output = db.Column(db.String)
    errors = db.Column(db.String)
    feedback = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(255), nullable=False)
    


def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        

def get_session():
    session_factory = sessionmaker(bind=db.engine)
    return scoped_session(session_factory)


