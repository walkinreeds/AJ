import os

from utils.functions import get_db_url

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 页面模板
template_dir = os.path.join(BASE_DIR, 'templates')
# 静态模板
static_dir = os.path.join(BASE_DIR, 'static')

DATABASE = {
    # 用户
    'USER': 'root',
    # 密码
    'PASSWORD': '123456',
    # 地址
    'HOST': '47.106.122.64',
    # 端口
    'PORT': '3306',
    # 数据库
    'DB': 'mysql',
    # 驱动
    'DRIVER': 'pymysql',
    # 数据库名称
    'NAME': 'aj'
}
# 连接数据库
SQLALCHEMY_DATABASE_URI = get_db_url(DATABASE)

UPLOAD_DIRS = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
