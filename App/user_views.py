import re
import os

from flask import Blueprint, session, render_template, request, jsonify, redirect, url_for
from sqlalchemy import or_

from App.models import db, User, Area, House, Order
from utils.setting import UPLOAD_DIRS
from utils.status_code import *
from utils.functions import is_login

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/createdb/')
def create_db():

    db.create_all()
    return '创建成功'


@user_blueprint.route('/login/')
def hello_user():

    return render_template('login.html')


@user_blueprint.route('/register/', methods=['GET'])
def register():

    return render_template('register.html')

@user_blueprint.route('/register/', methods=['POST'])
def suer_register():

    register_dict = request.form
    mobile = register_dict.get('mobile')
    password = register_dict.get('password')
    password2 = register_dict.get('password2')

    # 如果有一个参数为空 则为False
    if not all([mobile, password, password2]):

        return jsonify(USER_REGISTER_PARAMS_ERROR)

    if not re.match(r'^1[345789]\d{9}$', mobile):

        return jsonify(USER_REGISTER_MOBILE_ERROR)

    if User.query.filter(User.phone == mobile).count():
        return jsonify(USER_REGISTER_MOBILE_IS_EXSITS)

    if password != password2:
        return jsonify(USER_REGISTER_PASSWORD_IS_ERROR)

    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password

    try:
        user.add_update()
        return jsonify(SUCCESS)
    except:
        return jsonify(USER_REGISTER_PARAMS_ERROR)

'''
登陆页面
'''
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')

'''
post登陆api
'''
@user_blueprint.route('/login/', methods=['POST'])
def user_login():

    user_dict = request.form
    mobile = user_dict.get('mobile')
    password = user_dict.get('password')

    if not all([mobile, password]):
        return jsonify(PARAMS_ERROR)

    if not re.match(r'^1[345789]\d{9}$', mobile):
        return jsonify(USER_REGISTER_MOBILE_ERROR)

    user = User.query.filter(User.phone==mobile).first()
    if user:
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(SUCCESS)
        else:
            return jsonify(USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(USER_LOGIN_IS_NOT_EXSIST)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('my.html', user=user.to_basic_dict())

@user_blueprint.route('/user/', methods=['GET'])
@is_login
def get_user_profile():

    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict(), code='200')


@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user_blueprint.route('/user/', methods=['PUT'])
@is_login
def user_profile():
    user_dict = request.form
    file_dict = request.files
    if 'avatar' in file_dict:

        f1 = file_dict['avatar']

        if not re.match(r'^image/.*$', f1.mimetype):

            return jsonify(USER_UPLOAD_IMAGE_IS_ERROR)

        # 优化：可以写在setting里面
        # url = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # url = os.path.join(url, 'static')
        # url = os.path.join(url, 'upload')
        # url = os.path.join(url, f1.filename)

        url = os.path.join(UPLOAD_DIRS, f1.filename)
        f1.save(url)

        user = User.query.filter(User.id==session['user_id']).first()
        image_url = os.path.join('/static/upload/', f1.filename)
        user.avatar = image_url
        try:
            user.add_update()
            return jsonify(code=OK, url=image_url)
        except Exception as e:
            return jsonify(DATABASE_ERROR)
    elif 'name' in user_dict:

        name = user_dict.get('name')

        if User.query.filter(User.name==name).count():

           return jsonify(USER_UPLOAD_USERNAME_IS_EXSITS)

        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(SUCCESS)
        except Exception as e:
            return jsonify(DATABASE_ERROR)

    else:
        return jsonify(PARAMS_ERROR)



# @user_blueprint.route('/readauth/<int:myphone>/', methods=['GET'])
# def auth(myphone):
#     user = User.query.filter(User.phone==myphone).first()
#     return render_template('auth.html', user=user)
#
# @user_blueprint.route('/auth/', methods=['POST'])
# def change_auth():
#     auth_dict = request.form
#     card = auth_dict.get('id_card')
#     real_name = auth_dict.get('real_name')
#
#     user = User.query.filter(User.id_card == card).first()
#
#     if not user:
#         user.add_update()
#         return jsonify(SUCCESS)
#     else:
#         return jsonify(USER_UPLOAD_USER_IS_EXSITS)


@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():

    user = User.query.get(session['user_id'])
    if user.id_card:
        return jsonify(code=OK,
                   id_name=user.id_name,
                   id_card=user.id_card
                   )
    else:
        return jsonify(NO)





@user_blueprint.route('/auths/', methods=['PUT'])
@is_login
def user_auth():

    user_dict = request.form

    id_name = user_dict.get('id_name')
    id_card = user_dict.get('id_card')

    if not all([id_card, id_name]):
        return jsonify(PARAMS_ERROR)

    # if not re.match(r'\d{18}'):
    #     return jsonify(USER_UPLOAD_USER_IDCARD_IS_ERROR)

    try:
        user = User.query.get(session['user_id'])
        user.id_card = id_card
        user.id_name = id_name

        user.add_update()
        return jsonify(SUCCESS)
    except Exception as e:
        return jsonify(DATABASE_ERROR)


@user_blueprint.route('/logout/')
@is_login
def user_logout():
    session.clear()
    return jsonify(SUCCESS)

# 主页面
@user_blueprint.route('/index/', methods=['GET'])
def index():

    return render_template('index.html')

@user_blueprint.route('/index_search/', methods=['GET'])
def index_search():

    areas = Area.query.all()

    area_list = [area.to_dict() for area in areas]

    user_name = ''

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlist = [house.to_dict() for house in houses]


    return jsonify(code=OK,
                   alist=area_list,
                   hlist=hlist,
                   user_name=user_name
                   )


# @user_blueprint.route('/index/', methods=['POST'])
# def index_post():
#
#     search_list = request.form
#
#     area = search_list.get('')



@user_blueprint.route('/search/', methods=['GET'])
def search():

    return render_template('search.html')

# @user_blueprint.route('/search/<aid>:')

@user_blueprint.route('/allsearch/', methods=['GET'])
def house_search():
    # 从get请求中拿数据
    search_dict = request.args

    area_id = search_dict.get('aid')
    start_data = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_key = search_dict.get('sk')

    if area_id:
        houses = House.query.filter(House.area_id==area_id)
    else:
        houses = House.query.filter()  # xxx.query.all() 返回为列表 .filter不写条件则为全部对象.
    if all([start_data, end_date]):
        # 对房屋houses进行处理
        orders1 = Order.query.filter(Order.begin_date>=start_data,
                           Order.end_date<=end_date)

        orders2 = Order.query.filter(Order.begin_date<=end_date,
                           Order.end_date>=end_date)

        orders3 = Order.query.filter(Order.begin_date <= start_data,
                           Order.end_date >= start_data)

        orders4 = Order.query.filter(Order.begin_date <= start_data,
                           Order.end_date >= end_date)

        # orders = Order.query.filter(or_(Order.begin_date<=end_date,
        #                        Order.end_date>=start_data))

        orders_list1 = [o1.house_id for o1 in orders1]
        orders_list2 = [o2.house_id for o2 in orders2]
        orders_list3 = [o3.house_id for o3 in orders3]
        orders_list4 = [o4.house_id for o4 in orders4]

        orders_list = orders_list1 + orders_list2 + orders_list3 + orders_list4
        orders_list = list(set(orders_list))


        order_list = [order.house_id for order in orders_list]
        houses = houses.filter(House.id.notin_(order_list))


    if sort_key:
        if sort_key == 'booking':
            sort_key = House.room_count.desc()
        if sort_key == 'price-inc':
            sort_key = House.price.asc()
        if sort_key == 'price-des':
            sort_key = House.price.desc()
    else:
        sort_key = House.id.desc()

    houses = houses.order_by(sort_key)


    hlist = [house.to_dict() for house in houses]


    # 区域处理
    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=OK,
                   hlist=hlist,
                   alist=alist,
                   )
