#-*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Management.config import config

db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    #注册蓝图
    from .employee import employee as employee_blueprint
    from .management import management as management_blueprint
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(management_blueprint,url_prefix="/admin")


    return app