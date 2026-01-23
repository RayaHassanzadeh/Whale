from datetime import datetime
from forum import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    posts = db.relationship('Post', backref='author', lazy=True)  # realationhip between users and posts
    comments = db.relationship('Comment', backref='user', lazy=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') 

    def __repr__(self):
        return f"User('{self.username}', 'Created on: {self.date_created}', 'Avatar: {self.image_file}')"

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary key
    subject = db.Column(db.String(100), nullable=False)  # be careful remind urself to do not put this empy
    content = db.Column(db.Text, nullable=False)  # mo length limit
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)  
    edited = db.Column(db.Boolean, default=False) # whether it has been changed to disply specific time 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID
    category = db.Column(db.String(20), nullable=False, default='General')  
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', 'Category: {self.category}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True
    rating = db.Column(db.Integer, nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  
