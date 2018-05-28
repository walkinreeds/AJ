
from datetime import datetime


from flask import render_template, jsonify, Blueprint, request, session

from App.models import Order, House
from utils.status_code import *


order_blueprint = Blueprint('order', __name__)

@order_blueprint.route('/', methods=['POST'])
def order():

    order_dict = request.form

    house_id = order_dict.get('house_id')
    start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
    end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')

    if not all([house_id, start_time, end_time]):
        return jsonify(PARAMS_ERROR)

    if start_time > end_time:
        return jsonify(ORDER_START_TIME_GT_END_TIME)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days + 1
    order.amount = order.days * order.house_price
    try:
        order.add_update()
        return jsonify(code=OK)
    except:
        return jsonify(DATABASE_ERROR)


@order_blueprint.route('/order/', methods=['GET'])
def orders():

    return render_template('orders.html')

@order_blueprint.route('/orders/', methods=['GET'])
def my_orders():

    # order = Order.query.get(id)

    orders = Order.query.filter(Order.user_id == session['user_id']).order_by(Order.id.asc())
    order_list = []
    # for order in orders:
    #     order_list.append(order)

    order_list = [order.to_dict() for order in orders]

    return jsonify(code=OK, order=order_list)


@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():

    return render_template('lorders.html')



@order_blueprint.route('/mylorders/', methods=['GET'])
def my_lorders():
    # 第一种方式
    # 先查询房东房屋的id
    user_id = session['user_id']
    houses = House.query.filter(House.user_id==user_id)
    house_ids = [house.id for house in houses]
    # 再通过房屋的id去查找订单
    orders = Order.query.filter(Order.house_id.in_(house_ids)).order_by(Order.id.asc())
    order_list = [order.to_dict() for order in orders]

    # # 第二种方式
    # houses = House.query.filter(House.user_id == user_id)
    # order_list = []
    # for house in houses:
    #     orders = house.orders
    #     order_list.append(orders)
    #
    # olist = [order.to_dict() for order in order_list]


    return jsonify(code=OK, order=order_list)


@order_blueprint.route('/order/<int:id>/', methods=['PATCH'])
def order_status(id):

    status = request.form.get('status')

    order = Order.query.get(id)



    if status == 'REJECTED':
        comment = request.form.get('comment')
        order.comment = comment

    order.status = status

    try:
        order.add_update()
        return jsonify(code=OK)
    except:
        return jsonify(DATABASE_ERROR)



