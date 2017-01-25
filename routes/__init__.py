from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from functools import wraps
from models.user import User
from models.topic import Topic
import os
from werkzeug.utils import secure_filename
import random




def current_user(f):
    @wraps(f)
    def function(*args,**kw):
        user_id = session.get('uid')
        if user_id != None:
            u = User.query.get(user_id)
            return f(u, *args,**kw)
        else:
            form = {
                'username' : '游客',
                'avatar' :'0001.jpeg'
            }
            u = User(form)

            return f(u, *args,**kw)
    return function


def valid_id(f):
    @wraps(f)
    def function(id):
        user_id = session.get('uid')
        topic = Topic.query.get(id)
        if user_id != None:
            if user_id == topic.user_id:
                return f(id)
            else:
                abort(401)
        else:
            return redirect(url_for('user.login_index'))
    return function

