#-*-coding:utf-8-*-
from werkzeug.routing import BaseConverter


class ReConverter(BaseConverter):
    def __init__(self):
        super(ReConverter,self)