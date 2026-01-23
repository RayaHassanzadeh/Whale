from forum import app, db, bcrypt, allowed_file
from flask import redirect, request, render_template, flash, url_for, abort
from forum.forms import Signup, Login, Create_Post, Edit_Post, Create_Comment, UpdateAccountForm
from forum.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import secrets
from PIL import Image
import os

#displays all the current users that have been created and added to the database
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)
#grabs user id from index.html link.

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) #Grabs specific user from database
    db.session.delete(post) #db.session.delete() deltes user instead of making a change
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect(url_for('index'))

#import form class from forms.py
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()
    if(request.method =='POST'): #if getting a post request it means user hit the submit button
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, password=hashed_password) #grabs data from form and creates user object
            db.session.add(user)
            db.session.commit() #adds to database
            flash('You have Signed UP!!', 'success')
            return redirect(url_for('index'))
        else:
            flash("sign up failed, check errors", 'danger')
    return render_template('signup.html', form=form) #this is passing in the form for the html document to read.


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST': 
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You have logged in!', 'success')
                
                next_page = request.args.get('next')  # 获取重定向目标
                return redirect(next_page) if next_page else redirect(url_for('index'))
            
            flash('Login failed. Check username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", 'success')
    return redirect(url_for('index'))

@app.route('/posts')
def posts():
    posts = Post.query.all()
    user = current_user
    return render_template('posts.html', posts=posts, user=user)

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form = Create_Post()
    if(request.method =='POST'): #if getting a post request it means user hit the submit button
        if form.validate_on_submit():
            user_id = current_user.id
            post = Post(
                subject=form.subject.data,
                content=form.content.data,
                user_id=user_id,  # 将帖子与当前用户关联
                category=form.category.data  # 假设表单中有分类字段
            )
            db.session.add(post)
            db.session.commit() #添加至数据库
            flash('Your post has been created!', 'success')
            return redirect(url_for('index'))
        else:
            flash("Failed to create post, please check the errors", 'danger')
    return render_template('createpost.html', form=form) #this is passing in the form for the html document to read.

@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    post = Post.query.get_or_404(post_id)  # 根据 post_id 查找帖子，如果不存在返回 404
    if post.user_id != current_user.id:  # 确保当前用户只能编辑自己的帖子
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('index'))
    
    form = Edit_Post()
    if request.method == 'POST':  # 如果收到 POST 请求
        if form.validate_on_submit():
            post.subject = form.subject.data  # 更新帖子标题
            post.content = form.content.data  # 更新帖子内容
            post.category = form.category.data  # 更新分类
            post.edited = True  # 标记为已编辑

            db.session.commit()  # 提交更改
            flash('Your post has been updated!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to submit edit, please check the errors', 'danger')
    else:
        # 填充表单初始值
        form.subject.data = post.subject
        form.content.data = post.content
        form.category.data = post.category

    return render_template('editpost.html', form=form)  # 渲染编辑页面

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()  # 按时间排序评论

    form = Create_Comment()
    if request.method == 'POST':
        # 提交评论
        if form.validate_on_submit():
            user_id = current_user.id
            post_id = post_id
            comment = Comment(
                text=form.text.data,
                user_id=user_id,
                post_id=post_id,
                rating=form.rating.data 
            )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment and rating have been submitted!', 'success')
            return redirect(url_for('view_post', post_id=post_id))
        else:
            flash('Comment or rating cannot be empty!', 'danger')

    return render_template('view_post.html', post=post, comments=comments, form=form, user=current_user)


@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('You are not authorized to delete this comment.', 'danger')
        return redirect(url_for('view_post', post_id=comment.post_id))
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('view_post', post_id=comment.post_id))

@app.route('/users')
@login_required
def users():
    if current_user.id != 1:
        abort(403)
    users = User.query.all()
    return render_template('users.html', users = users, title="users", current_user_id = current_user.id)
    
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id) #Grabs specific user from database
    user.username = "changed" #db.session.delete() deltes user instead of making a change
    db.session.commit()
    flash("Your user has been deleted", 'success')
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # 更新用户名
        if form.username.data:
            current_user.username = form.username.data

        # 更新密码（仅当用户输入了新密码时）
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        # 更新头像
        if form.picture.data:
            # 生成随机文件名
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.picture.data.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_fn)

            # 保存图片并调整大小
            output_size = (125, 125)
            i = Image.open(form.picture.data)
            i.thumbnail(output_size)
            i.save(picture_path)

            # 删除旧头像（如果不是默认头像）
            if current_user.image_file != 'default.jpg':
                old_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.image_file)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)

            current_user.image_file = picture_fn

        # 提交更改
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))  # 防止表单重复提交

    elif request.method == 'GET':
        # 预填充用户名
        form.username.data = current_user.username

    # 渲染模板
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
