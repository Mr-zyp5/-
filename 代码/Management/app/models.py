#-*-coding:utf-8-*-
from datetime import datetime
from sqlalchemy.dialects.mysql import FLOAT

from . import db
class Department(db.Model):
    __tablename__ = "department"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    depart_name = db.Column(db.String(100),unique=True)
    depart_manager = db.Column(db.String(100))
    manager_id = db.Column(db.String(6))
    people_num = db.Column(db.Integer,default=1)

class Employee(db.Model):
    __table__name = 'employee'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    work_num = db.Column(db.String(6))
    name = db.Column(db.String(100))
    sex = db.Column(db.Boolean(),default=1)
    age = db.Column(db.String(2))
    depart = db.Column(db.String(100))
    post = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(11),unique=True)
    email = db.Column(db.String(100),unique=True)
    face = db.Column(db.String(255),unique=True)
    id_card = db.Column(db.String(18),unique=True)
    pwd = db.Column(db.String(25),default='123456')
    depart_id = db.Column(db.Integer)
    addtime = db.Column(db.DateTime,default=datetime.now)

class Notice(db.Model):
    __table__name = 'employee'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    message = db.Column(db.Text)
    author = db.Column(db.String(20),default='管理员')
    pubtime = db.Column(db.DateTime,default=datetime.now)
    user_type = db.Column(db.String(100))
    type_id = db.Column(db.Integer)

class Sign(db.Model):
    __table__name = 'sign'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    work_id = db.Column(db.String(6))
    signtime = db.Column(db.DateTime)
    is_late = db.Column(db.Integer,default=0)
    outtime = db.Column(db.DateTime)
    is_lvearly = db.Column(db.Integer,default=0)
    status = db.Column(db.Integer,default=1)

class Attendance(db.Model):
    __table__name = 'attendnace'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    work_hours = db.Column(db.Integer)



class Leave(db.Model):
    __table__name = 'leave'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(6))
    leave_name = db.Column(db.String(30))
    manager_id = db.Column(db.String(6))
    reason = db.Column(db.Text)
    status = db.Column(db.Integer,default=3)
    vacat_time = db.Column(db.Integer)
    addtime = db.Column(db.DateTime,default=datetime.now)


class Salary(db.Model):
    __table__name = 'leave'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.String(6),)
    base_salary = db.Column(db.Float(10,2))
    grant = db.Column(db.Float(10,2))
    insur_fund = db.Column(db.Float(10,2))
    fine = db.Column(db.Float(10,2))
    real_salary = db.Column(db.Float(10,2))
    month = db.Column(db.String(6))
    addtime = db.Column(db.DateTime,default=datetime.now)
