from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    nickname = StringField("nickname:", validators=[DataRequired("用户名不能为空")])
    content = TextAreaField(validators=[DataRequired('评论内容不能为空')])