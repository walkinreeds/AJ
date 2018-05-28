from flask import session, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_ext(app):
    db.init_app(app=app)

def get_db_url(DATABASE):
    user = DATABASE.get('USER')
    password = DATABASE.get('PASSWORD')
    host = DATABASE.get('HOST')
    port = DATABASE.get('PORT')
    name = DATABASE.get('NAME')
    driver = DATABASE.get('DRIVER')
    db = DATABASE.get('DB')

    return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver,user, password,host, port, name)


import functools
def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            # 验证用户是否登陆
            # if session['user_id']
           if 'user_id' in session:
               return view_fun()
           else:
               return redirect('/user/login/')
        except:
            return redirect('/user/login/')
    return decorator