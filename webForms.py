from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, equal_to
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    name = StringField("Name",
                       validators=[DataRequired()])

    username = StringField("username",
                           validators=[DataRequired()])
    email = StringField("Email",
                        validators=[DataRequired()])
    fav_color = StringField("Favorite Color")
    password_hash = PasswordField("Password",
                                  validators=[DataRequired(), equal_to('password_hash_2',
                                                                       message='Password must to match')])
    password_hash_2 = PasswordField("Confirm Password",
                                    validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired()])
    content = StringField("Content",
                          validators=[DataRequired()],
                          widget=TextArea())
    author = StringField("Author",
                         validators=[DataRequired()])
    slug = StringField("Slug",
                       validators=[DataRequired()])
    submit = SubmitField("Submir")



# create form class
class NamerForm(FlaskForm):
    name = StringField("What is your name?",
                       validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("What is your email?",
                        validators=[DataRequired()])
    password_hash = PasswordField("What is your password?",
                                  validators=[DataRequired()])
    submit = SubmitField("Submit")
