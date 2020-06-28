#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, RadioField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length


#完善个人信息
class PersonForm(FlaskForm):

    phone = StringField(
        label="手机号",
        validators=[
            DataRequired("手机号不能为空！")
        ],
        description="手机号",
        render_kw={
            "class": "input-xlarge",
            "placeholder": "请输入手机号！"
        }
    )
    age = StringField(
        label='年龄',
        validators=[
            DataRequired("年龄不能为空")
        ],
        description="年龄",
        render_kw={
            "class":"input-xlarge"
        }
    )
    id_card = StringField(
        label="身份证号",
        validators=[
            DataRequired("身份证号不能为空！")
        ],
        description="身份证号",
        render_kw={
            "class": "input-xlarge",
            "placeholder": "请输入身份证号！"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("邮箱不能为空！")
        ],
        description="邮箱",
        render_kw={
            "class": "input-xlarge",
            "placeholder": "请输入邮箱！"
        }
    )
    address = StringField(
        label="地址",
        validators=[
            DataRequired("地址不能为空！")
        ],
        description="地址",
        render_kw={
            "class": "input-xlarge",
            "placeholder": "请输入地址！"
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            "class": "btn btn-primary",
        }
    )
class AttendForm(FlaskForm):
    submit = SubmitField(
        '生成考勤记录表',
        render_kw={
            "class": "btn btn-primary",
        }
    )