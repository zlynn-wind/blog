from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField("username:", validators=[DataRequired()])
    password = PasswordField("password:", validators=[DataRequired()])
    password2 = PasswordField(
        "confirm password:", validators=[DataRequired(), EqualTo("password", "密码填写输入不一致")])
    submit = SubmitField("提交")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Register')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    confirm_new_password = PasswordField("Confirm_new_password:", validators=[
        DataRequired(), EqualTo("new_password", "密码填写输入不一致")])
    submit = SubmitField('Update Password')
