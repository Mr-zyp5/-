#-*-coding:utf-8-*-
from flask import Blueprint
management = Blueprint("management",__name__,static_url_path='/app/static')
from . import views