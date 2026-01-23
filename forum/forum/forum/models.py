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
    posts = db.relationship('Post', backref='author', lazy=True)  # 用户与帖子之间的关系
    comments = db.relationship('Comment', backref='user', lazy=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # 默认头像

    def __repr__(self):
        return f"User('{self.username}', 'Created on: {self.date_created}', 'Avatar: {self.image_file}')"

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键，唯一标识每个帖子
    subject = db.Column(db.String(100), nullable=False)  # 帖子的标题，不能为空
    content = db.Column(db.Text, nullable=False)  # 帖子的内容，没有长度限制
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 发帖时间，默认当前时间
    edited = db.Column(db.Boolean, default=False) #是否更改过，用于显示具体时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联发帖用户的 ID
    category = db.Column(db.String(20), nullable=False, default='General')  # 帖子的分类
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', 'Category: {self.category}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)  # 评论内容
    rating = db.Column(db.Integer, nullable=True)  # 评分（1~5）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 评论者
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # 评论所属帖子
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 评论时间
