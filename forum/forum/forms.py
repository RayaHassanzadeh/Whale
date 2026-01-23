#Creating forms using wtfForms.  Create a class of the requried data.

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from forum.models import User
from flask_wtf.file import FileAllowed
from flask_login import current_user

def validate_category(form, field):
    allowed_categories = ['General', 'Tech', 'Sports', 'Entertainment']
    if field.data not in allowed_categories:
        raise ValidationError('Invalid category selected.')

def validate_rating(form, field):
    allowed_categories = ['1 - Poor', '2 - Fair', '3 - Good', '4 - Very Good', '5 - Excellent']
    if field.data not in allowed_categories:
        raise ValidationError('Invalid category selected.')

class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # check if the same username exists in the database.
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
        
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('New Password', validators=[])  # romove
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message="Passwords must match")])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Save Changes')

    # check username
    def validate_username(self, username):
        if username.data != current_user.username:  
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')

    # validate the length when and only when password is provided
    def validate_password(self, password):
        if password.data:  
            if len(password.data) < 4 or len(password.data) > 20:
                raise ValidationError('Field must be between 4 and 20 characters long.')



class Login(FlaskForm): #Don't forget to inherit FlaskForm, see forms.html to display form.
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Create_Post(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    content = StringField('Content', validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[('General', 'General'), ('Tech', 'Tech'), ('Sports', 'Sports'), ('Entertainment', 'Entertainment')],
        validators=[DataRequired(), validate_category]  
    )
    submit = SubmitField('Create Post')

class Edit_Post(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    content = StringField('Content', validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[('General', 'General'), ('Tech', 'Tech'), ('Sports', 'Sports'), ('Entertainment', 'Entertainment')],
        validators=[DataRequired(), validate_category]  
    )
    submit = SubmitField('Submit Edit')

class Create_Comment(FlaskForm):
    text = StringField('Leave your comment...', validators=[DataRequired(), Length(min=2, max=800)])
    rating = SelectField(
        'Category',
        choices=[('1 - Poor', '1 - Poor'), ('2 - Fair', '2 - Fair'), ('3 - Good', '3 - Good'), ('4 - Very Good', '4 - Very Good'), ('5 - Excellent', '5 - Excellent')],
        validators=[DataRequired(), validate_rating]  
    )
    submit = SubmitField('Create Post')
#The validators will display errors on your website live (see forms.html) 
