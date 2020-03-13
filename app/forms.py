from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField,PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired

class AddProfile(FlaskForm):
 fname = StringField('First Name', validators=[DataRequired()])
 lname = StringField('Last Name', validators=[DataRequired()])
 gender = StringField('Gender', validators=[DataRequired()])
 email = StringField('Email', validators=[DataRequired(), Email()])
 location = StringField('Location', validators=[DataRequired()])
 biography = TextAreaField('Biography', validators=[DataRequired()])
 photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])
    ])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

