from flask import render_template, redirect, request, url_for, flash
from flask.globals import current_app
from flask_login import login_user, logout_user, login_required, current_user
from Auth.init import auth
from Auth.form import LoginForm, RegistrationForm, ChangePasswordForm
from app.init import db
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        curr_username=form.username.data
        user=User.get_user_by_username(curr_username)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('密码错误')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功登出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.checkout_username(form.username.data):
            flash("用户名已存在，请重新输入")
            return redirect(url_for('auth.register'))
        User.create(username=form.username.data, password=form.password.data)
        flash('注册成功，跳转至登录界面')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经确认你的账户')
    else:
        flash('确认失败')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            User.update_password(form.password.data)
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('无效密码')
    return render_template("auth/change_password.html", form=form)
