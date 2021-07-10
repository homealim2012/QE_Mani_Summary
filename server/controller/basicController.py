# coding=utf-8

from flask import Blueprint
from flask import session, redirect, url_for, render_template
import functools

basic_opt = Blueprint('basic_opt', __name__, static_url_path='/resources', static_folder='resources')

class CheckUserSession:
    def __init__(self):
        pass

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if session.get('username'):
                return func(*args, **kwargs)
            return redirect('/login', code=302)
        return wrapper

@basic_opt.route('/', methods=['GET'])
def index():
    return render_template('index.html')
