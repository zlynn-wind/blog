from flask import render_template, flash, jsonify

from app.models import Post
from Post.init import post
from Post.form import PostForm


@post.route('/add_post', methods=['POST'])
def add_comment():
    form = PostForm()
    if form.validate_on_submit():
        text = form.content.data
        Post.create(text)
        flash("add comment success")
    return render_template('content.html', form=form)
