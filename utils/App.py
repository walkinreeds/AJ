from flask import Flask

from utils.setting import template_dir, static_dir
from App.user_views import user_blueprint
from utils.functions import init_ext
from App.house_views import house_blueprint
from App.order_views import order_blueprint

def create_app(config):
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(house_blueprint, url_prefix='/house')
    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.config.from_object(config)

    init_ext(app)


    return app