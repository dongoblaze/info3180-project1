from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField,PasswordField,SelectField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired

class AddProfile(FlaskForm):
 fname = StringField('First Name', validators=[DataRequired()])
 lname = StringField('Last Name', validators=[DataRequired()])
 gender = SelectField(label='Gender', choices=[("Male", "Male"), ("Female", "Female")])
 email = StringField('Email', validators=[DataRequired(), Email()])
 location = StringField('Location', validators=[DataRequired()])
 biography = TextAreaField('Biography', validators=[DataRequired()])
 photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])
    ])