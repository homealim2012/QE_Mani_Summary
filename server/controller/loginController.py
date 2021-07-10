# coding=utf-8

from flask import Blueprint
from flask import g
from flask import request, session, url_for, redirect, render_template
from server.service.loginService import LoginService
login_opt = Blueprint('login_opt', __name__, static_url_path='/resources')

@login_opt.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        res = LoginService(username, password).main()
        if res.response == 'success':
            session['username'] = username
        return res
    else:
        return render_template('index.html')

@login_opt.route('/logout')
def logout():
    session.clear()
    return redirect('/login', code=302)
