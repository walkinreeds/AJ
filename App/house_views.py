import os

from flask import session, Flask, Blueprint, render_template, jsonify, redirect, request

from App.models import User, House, Area, Facility, db, HouseImage
from utils.status_code import *
from utils.functions import is_login
from utils.setting import UPLOAD_DIRS

house_blueprint = Blueprint('house', __name__)

@house_blueprint.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')


@house_blueprint.route('/auth_myhouse/', methods=['GET'])
@is_login
def auth_myhouse():

    user = User.query.get(session['user_id'])
    if user.id_card:
        houses = House.query.filter(House.user_id==user.id).order_by(House.id.desc())
        hlist_list = []
        for house in houses:
            hlist_list.append(house.to_dict())
        return jsonify(hlist_list=hlist_list, code=OK)
    else:
        return jsonify(MYHOUSE_USER_IS_NOT_AUTH)


@house_blueprint.route('/newhouse/', methods=['GET'])
@is_login
def newhouse():

    return render_template('newhouse.html')


@house_blueprint.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilitys = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilitys]

    return jsonify(area_list=area_list, facility_list=facility_list)

@house_blueprint.route('/newhouse/', methods=['POST'])
@is_login
def save_info():
    house_dict = request.form
    title = house_dict.get('title')
    price = house_dict.get('price')
    address= house_dict.get('address')
    room_count= house_dict.get('room_count')
    acreage= house_dict.get('acreage')
    unit = house_dict.get('unit')
    capacity= house_dict.get('capacity')
    beds= house_dict.get('beds')
    deposit= house_dict.get('deposit')
    min_days= house_dict.get('min_days')
    max_days= house_dict.get('max_days')
    area_id= house_dict.get('area_id')
    facilitys= house_dict.getlist('facility')
    user_id = session['user_id']

    house = House()
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    house.area_id = area_id
    house.user_id = user_id

    # try:
    #     house.add_update()
    #     for facility in facilitys:
    #         sql = 'insert into ihome_house_facility(house_id, facility_id) values(%s, %s)' % (house.id, facility)
    #         db.session.execute(sql)
    #         db.session.commit()
    #     return jsonify(SUCCESS)
    # except Exception as e:
    #     return jsonify(DATABASE_ERROR)
    if facilitys:
        facility = Facility.query.filter(Facility.id.in_(facilitys)).all()
        house.facilities = facility
    house.add_update()
    return jsonify(code=OK, house_id=house.id)


@house_blueprint.route('/images/', methods=['POST'])
def newhouse_images():

    images = request.files.get('house_image')
    house_id = request.form.get('house_id')

    # 保存成功
    url = os.path.join(UPLOAD_DIRS, images.filename)
    images.save(url)

    image_url = os.path.join(os.path.join('/static', 'upload'), images.filename)

    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image_url
    try:
        house_image.add_update()
    except:
        return jsonify(DATABASE_ERROR)
    house = House.query.get(house_id)

    if not house.index_image_url:
        house.index_image_url = image_url
        try:
            house.add_update()
        except:
            return jsonify(DATABASE_ERROR)

    return jsonify(code=OK, image_url=image_url)


@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')

@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):

    house = House.query.get(id)

    facility_list = house.facilities

    facility_dict_list = [facility.to_dict() for facility in facility_list]

    index_image_url = house.index_image_url

    booking = 1
    if 'user_id' in session:
        if house.user_id == session['user_id']:
            booking = 0

    return jsonify(house=house.to_full_dict(),
                   facility_list=facility_dict_list,
                   booking=booking,
                   index_image_url=index_image_url,
                   code=OK
                   )

@house_blueprint.route('/booking/', methods=['GET'])
def booking():

    return render_template('booking.html')