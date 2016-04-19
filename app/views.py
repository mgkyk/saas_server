# encoding: utf8
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import *
from app.models import *
from app.forms import *
from app import host
import threading

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# 在任何request请求开始之前会提前执行
@app.before_request
def before_request():
    g.user = current_user

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.username.data
        passwd = form.passwd.data
        re_passwd = form.retype_passwd.data
        # compare two passwd
        if passwd != re_passwd:
            flash('two passwd is not the same')
            return render_template('login.html', form=form)
        # add this user into database
        if db.session.query(User).filter(User.user==user).first() is not None:  # this user has existed
            flash('this user has existed')
            return render_template('login.html', form=form)
        new_user = User(user=user, id=create_id())  # append a recode
        new_user.hash_password(passwd)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        g.user = user  # remember the user
        return redirect(url_for('user_info', user_name=user))

    return render_template('sign_up.html', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        user_name = str(form.username.data)
        passwd = str(form.passwd.data)
        user = User.query.filter_by(user=user_name).first()
        if not user or not user.verify_password(passwd):
            print("nop")
            return render_template('sign_in.html', form=form)
        else:
            g.user = user
            login_user(user)  # remember the user
            return redirect(url_for('user_info', user_name=user_name))

    return render_template('sign_in.html', form=form)

@app.route('/sign_out', methods=['POST'])
def sign_out():
    pass

@app.route('/srclist', methods=['GET'])
@login_required
def srclist():
    records = db.session.query(Resource).all()
    source_info = []
    for i in range(len(records)):  # list sources
        tmp = {'source_name': records[i].source_name, 'detail': records[i].detail}
        source_info.append(tmp)
    user = g.user
    return render_template('srclist.html', source_info=source_info, user=user)

@app.route('/<string:user_name>/<string:src_name>/get_src', methods=['GET', 'POST'])
#@login_required
def get_src(user_name, src_name):  # user need to put a excel, how to do that
    # 判断是否是集群
    src = db.session.query(Resource).filter(Resource.source_name==src_name).first()
    print(src.map, user_name)
    form = GetClusterSource(request.form)
    if request.method == 'POST' and form.validate():  # 如果是post请求并且表格符合结构
        num = form.node.data
        try:
            num = int(num)
        except:
            print('非数字输入')
        return redirect(url_for('wait', user_name=g.user.user, src_name=src.source_name))  # 重定位到等到界面
    return render_template('cluster_sheet.html', form=form, src=src)

@app.route('/<string:user_name>/user_info', methods=['GET'])
def user_info(user_name):  # 包括user的所有的信息
    return render_template('hello_world.html')

@app.route('/<string:user_name>/<string:src_name>/wait', methods=['GET'])
def wait(user_name, src_name):  # 提醒等待
    # installing software
    t = threading.Thread(target=host.install_software, args=(user_name, src_name))
    t.setDaemon(True)
    t.start()
    return render_template('wait.html', current_user=user_name)