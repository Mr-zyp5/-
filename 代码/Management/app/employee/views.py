#-*-coding:utf-8-*-
from datetime import datetime
from functools import wraps

from flask import render_template, session, request, redirect, url_for, make_response
from sqlalchemy import or_, and_, extract

from Management.app import db
from .forms import PersonForm, AttendForm
from ..models import Employee, Notice, Leave, Department, Sign, Attendance, Salary
from . import employee

def user_login(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "work_id" not in session:
            return redirect(url_for("employee.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@employee.route('/')
@user_login
def index():
    count = Notice.query.count()
    print(session)
    #职位
    post=0
    work_id = session.get('work_id')
    # 签到状态
    is_sign = 0
    sign_data = Sign.query.filter(or_(Sign.work_id==session['work_id']))
    if sign_data:
        sign_data = sign_data.order_by(Sign.id.desc()).first()
        if sign_data and (sign_data.signtime.date() == datetime.now().date()):
            is_sign = sign_data.status
    emp = Employee.query.filter(Employee.work_num==work_id).first()
    if emp.post == '部门经理':
        filters = and_(Leave.status == 3, Leave.manager_id == work_id)
        leave_count = Leave.query.filter(filters).count()
        print(leave_count)
        leave_data = Leave.query.filter(filters).order_by(Leave.id)
        post=1
    return render_template("employee/index.html",notice_count=count,is_sign=is_sign,
                           leave_count=leave_count,leave_data=leave_data,post=post)


@employee.route('/login/',methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form
        work_id = data['work_id']
        pwd = data['pwd']
        emp = Employee.query.filter(Employee.work_num==work_id).first()
        if emp:
            if emp.pwd == pwd:
                session['work_id'] = work_id
                return redirect(url_for('employee.index'))
            return make_response(
                "<script>alert('密码错误！');location.href='" + url_for('employee.login') + "'</script>")
        return make_response("<script>alert('工号不存在');location.href='"+url_for('employee.login')+"'</script>")


    # session['work_id'] = '123544'

    return render_template("employee/login.html")

@employee.route('/logout/')
def logout():
    session.pop("work_id", None)
    return make_response("<script>alert('退出成功！');location.href='" + url_for('employee.login') + "'</script>")


@employee.route('/personal/',methods=["GET","POST"])
def personal():
    work_id = session['work_id']
    employee = Employee.query.filter(Employee.work_num==work_id).first()
    form = PersonForm()
    if request.method=="POST":
        data = request.form
        sex = request.form.get('sex')
        age = request.form.get('age')
        employee.age = age
        employee.email = data['email']
        employee.phone = data.get('phone')
        employee.id_card = data.get('id_card')
        employee.address = data['address']
        employee.sex = int(sex)
        db.session.add(employee)
        db.session.commit()
        return make_response("<script>alert('修改成功');location.href='"+url_for('employee.personal')+"'</script>")
    return render_template('employee/personal.html', form=form, data=employee)

#公告
@employee.route('/noticedetail/')
def noticedetail():
    page = request.args.get('page', 1, type=int)
    work_id = session['work_id']
    employee = Employee.query.filter(Employee.work_num==work_id).first()
    filters = or_(Notice.type_id == employee.depart_id,Notice.type_id == 0)
    sign = Notice.query.filter(filters).order_by(Notice.id.desc()).paginate(page=page, per_page=5)
    print(sign)
    return render_template('employee/noticedetail.html',data=sign)

#请假
@employee.route('/leave/',methods=['GET','POST'])
def leave():
    work_id = session['work_id']
    leave_list = Leave.query.filter(or_(Leave.work_id==work_id)).order_by(Leave.addtime.desc())[:3]
    emp = Employee.query.filter(Employee.work_num==work_id).first()
    manager_id = Department.query.get(work_id).manager_id
    post = 0
    if emp.post == '部门经理':
        manager_id = '000001'
        untreat_list = Leave.query.filter(and_(Leave.status == 3,Leave.manager_id == work_id)).order_by(Leave.addtime)
        post = 1
    if request.method == "POST":
        reason = request.form.get('reason')
        day = int(request.form.get('day'))
        leave_data = Leave(
            work_id=work_id,
            leave_name=emp.name,
            vacat_time=day,
            manager_id=manager_id,
            reason=reason
        )
        db.session.add(leave_data)
        db.session.commit()
        return make_response("<script>alert('提交成功，请等待结果');location.href='"+url_for('employee.leave')+"'</script>")
    return render_template('employee/leave.html',data=leave_list,post=post,undata=untreat_list)


@employee.route('/dealleave/<int:id>/<int:agree>')
def deal_leave(id,agree):
    leave_data = Leave.query.get(id)
    leave_data.status = agree
    db.session.add(leave_data)
    db.session.commit()
    return make_response("<script>alert('操作成功！');location.href='"+url_for('employee.leave')+"'</script>")

# 签到
@employee.route('/sign/<int:status>')
def sign_in(status):
    if status == 1:
        is_late = 0
        if datetime.now().time() > datetime(2020,3,1,8,0).time():
            is_late = 1
        sign_data = Sign(
            work_id=session['work_id'],
            is_late=is_late,
            status=status,
            signtime=datetime.now()
        )
        db.session.add(sign_data)
        db.session.commit()
        return make_response("<script>alert('签到成功！');location.href='" + url_for('employee.index') + "'</script>")
    elif status == 2:
        is_early = 0
        if datetime.now().time() < datetime(2020,3,1,18,0).time():
            is_early = 1
        sign_data = Sign.query.filter(or_(Sign.work_id==session['work_id'])).order_by(Sign.id.desc()).first()
        sign_data.is_lvearly = is_early
        sign_data.status = status
        sign_data.outtime = datetime.now()
        db.session.add(sign_data)
        db.session.commit()
        return make_response("<script>alert('签退成功！');location.href='"+url_for('employee.index')+"'</script>")

#考勤
@employee.route('/attendetail/',methods=['GET','POST'])
@user_login
def attendtail():
    attend_data = Attendance.query.all()
    form = AttendForm()
    if request.method == "POST":
        work_id = session['work_id']
        month = request.form.get('month')
        name = Employee.query.filter(Employee.work_num == work_id).first().name
        real_days = Sign.query.filter(and_(Sign.work_id==work_id)).count()
        late_data = Sign.query.filter(and_(Sign.work_id==work_id,Sign.is_late==1,extract('month',Sign.signtime)==month)).count()
        early_data = Sign.query.filter(and_(Sign.work_id == work_id, Sign.is_lvearly == 1,extract('month',Sign.signtime)==month)).count()
        leave_data = Leave.query.filter(and_(Leave.work_id==work_id))
        days = 0
        for i in leave_data:
            days += i.vacat_time
        absen_days = Attendance.query.filter(or_(Attendance.month==month)).first().work_hours-days-real_days
        return render_template('employee/attendance.html', form=form, data=attend_data,
                               name=name,late_data=late_data,early_data=early_data,
                               days=days,absen_days=absen_days)

    return render_template('employee/attendance.html',form=form,data=attend_data)

#工资详情
@employee.route('/salarydetail/',methods=['GET','POST'])
@user_login
def salarydtail():
    months = Attendance.query.all()
    page = request.args.get('page', 1, type=int)
    work_id = session['work_id']
    employee = Employee.query.filter(Employee.work_num == work_id).first()
    keyword = request.args.get('keyword', '', type=str)
    print(keyword)
    page_data = Salary.query.order_by(Salary.id).paginate(page=page, per_page=5)
    if keyword:
        filters = or_(Salary.month == keyword)
        page_data = Salary.query.filter(filters).order_by(Salary.id).paginate(page=page, per_page=5)
    return render_template('employee/salary.html', data=page_data, employee=employee,months=months)