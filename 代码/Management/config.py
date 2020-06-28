#-*-coding:utf-8-*-
import os


class Config:
    SECRET_KEY = 'biyesoft'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/uploads/users/")  # 文件上传路径

    Debug=True


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/company'
    DEBUG = True


config = {
    'default':DevelopmentConfig
}