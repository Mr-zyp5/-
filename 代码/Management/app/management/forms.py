#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired

#部门
class DepForm(FlaskForm):
    """添加/编辑地区的表单"""
    dep_name = StringField(
        label="部门名称",
        validators=[
            DataRequired("部门名称不能为空")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入部门名称！"
        }
    )
    man_name = StringField(
        label = '是否推荐',
        validators=[
            DataRequired("经理名称不能为空")
        ],
        description="经理",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入经理名称！"
        }

    )

    submit = SubmitField(
        '添加',
        render_kw={
            "class": "am-btn am-btn-primary tpl-btn-bg-color-success",
        }
    )


#员工
class EmpForm(FlaskForm):
    name = StringField(
        label="姓名",
        validators=[
            DataRequired("姓名不能为空！")
        ],
        description="姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入员工姓名！"
        }
    )
    post = StringField(
        label="职位",
        validators=[
            DataRequired("职位不能为空！")
        ],
        description="职位",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入职位名称！"
        }
    )
    work_num = StringField(
        label="工号",
        validators=[
            DataRequired("工号不能为空！")
        ],
        description="工号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入工号！"
        }
    )

    face_img = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像！"),
            FileAllowed(['jpg', 'png'], '请上传jpg或png格式图片!')
        ],
        description="头像",
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "am-btn am-btn-primary tpl-btn-bg-color-success",
        }
    )


#公告
class NotForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题名称不能为空")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题！"
        }
    )
    author = StringField(
        label="发布人",
        validators=[
            DataRequired("发布人名称不能为空")
        ],
        description="发布人",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入发布人名称！"
        }
    )
    message = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空！")
        ],
        description="内容",
        render_kw={
            "class": "form-control",
            "rows": 5
        }
    )
    submit = SubmitField(
        '发布',
        render_kw={
            "class": "am-btn am-btn-primary tpl-btn-bg-color-success",
        }
    )
#考勤
class AttendForm(FlaskForm):
    work_hours = IntegerField(
        label="部门名称",
        validators=[
            DataRequired("部门名称不能为空")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入每个月要工作的天数（整数）！"
        }
    )
    submit = SubmitField(
        '保存',
        render_kw={
            "class": "am-btn am-btn-primary tpl-btn-bg-color-success",
        }
    )

#薪资
class SalaryForm(FlaskForm):
    work_id = StringField(
        label="工号",
        validators=[
            DataRequired("工号不能为空")
        ],
        description='工号',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入工号！"
        }
    )
    base_wage = FloatField(
        label="底薪",
        validators=[
            DataRequired("底薪不能为空")
        ],
        description='底薪',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入底薪数目！"
        }
    )
    fine = FloatField(
        label="罚款",
        validators=[
            DataRequired('罚款数目不能为空！')
        ],
        description='罚款',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入罚款数目！"
        }
    )
    grant = FloatField(
        label="奖金及其他补助",
        validators=[
            DataRequired('奖金及其他补助数目不能为空！')
        ],
        description='奖金及其他补助',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入奖金及其他补助数目！"
        }
    )
    submit = SubmitField(
        '结算',
        render_kw={
            "class": "am-btn am-btn-primary tpl-btn-bg-color-success",
        }
    )