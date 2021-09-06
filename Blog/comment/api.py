from flask import render_template, flash, jsonify

from app.models import Comment
from comment.init import comment
from comment.form import CommentForm


@comment.route('/add_comment', methods=['POST'])
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        content = form.content.data
        Comment.create(nickname=nickname, content=content)
        flash("add comment success")
    return render_template('content.html', form=form)


@comment.route('/list_comment', methods=['GET'])
def list_comment():
    form = CommentForm()
    if form.validate_on_submit():
        post_id = ""
        resp = jsonify(Comment.list_comment(post_id))
    return resp
