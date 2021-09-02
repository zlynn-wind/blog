from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields.core import SelectMultipleField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired('标题不能为空'), Length(max=60, message='标题最长不能超过 60 个字符')])
    content_markdown = TextAreaField()
    content = TextAreaField()
    categories = SelectMultipleField(validators=[DataRequired('必须选择一个分类')], coerce=int)
    can_comment = BooleanField(label='允许评论')
    description = TextAreaField(validators=[Length(max=150, message='SEO 描述信息不能超过 150 个字符')])
    publish = SubmitField('发布')
    save = SubmitField('保存为草稿')
