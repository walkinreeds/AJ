import redis

from utils.setting import SQLALCHEMY_DATABASE_URI


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session配置
    SECRET_KEY = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')
    SESSION_KEY_PREFIX = 'aj'

