#-*-coding:utf-8-*-
from datetime import datetime
import os
import uuid
from functools import wraps

from flask import render_template, request, url_for, make_response, flash, redirect, current_app, session
from sqlalchemy import or_, and_, extract
from werkzeug.utils import secure_filename

from Management.app import db
from .forms import DepForm, EmpForm, NotForm, AttendForm, SalaryForm
from ..models import Department, Employee, Notice, Attendance, Sign, Leave, Salary
from . import management


def admin_login(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("management.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def gen_rnd_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)


def change_filename(filename):
    """
    修改文件名称
    """
    fileinfo = os.path.splitext(filename)
    filename =  gen_rnd_filename() + fileinfo[-1]
    return filename


@management.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get("user")
        pwd = request.form.get("pwd")
        if user == "admin" and pwd == "123456":
            session['admin'] = 'admin'
            print(session)
            return render_template("management/index.html")
        return make_response("<script>alert('账户密码错误,重新输入');location.href='"+url_for('management.login')+"'</script>")
    return render_template("management/login.html")


@management.route('/index/',methods=['GET','POST'])
def index():

    return render_template("management/index.html")



@management.route('/logout/')
@admin_login
def logout():
    session.pop("admin",None)
    return make_response("<script>alert('退出成功！');location.href='"+url_for('management.login')+"'</script>")


#-----------------部门---------------------
@management.route('/departlist/',methods=['GET','POST'])
@admin_login
def departlist():
    page = request.args.get('page',1,type=int)
    keyword = request.args.get('keyword','',type=str)
    print(keyword)
    page_data = Department.query.order_by(Department.id).paginate(page=page, per_page=5)
    if keyword:
        filters = or_(Department.depart_name == keyword,Department.depart_manager == keyword)
        page_data = Department.query.filter(filters).order_by(Department.id).paginate(page=page,per_page=5)
    return render_template("management/depart/dep_table.html", data=page_data)


@management.route('/adddepart/',methods=['GET','POST'])
@admin_login
def adddepart():
    form = DepForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        department = Department(depart_name=data['dep_name'],
                                depart_manager=data['man_name'])
        db.session.add(department)
        db.session.commit()
        return make_response("<script>alert('添加成功');location.href='"+url_for('management.adddepart')+"'</script>")
    return render_template("management/depart/adddepart.html",form=form)


@management.route('/deldep/<int:id>/',methods=['GET'])
@admin_login
def del_depart(id=None):
    department = Department.query.get_or_404(int(id))
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('management.departlist'))


@management.route('/updatedep/<int:id>',methods=['GET','POST'])
@admin_login
def update_depart(id=None):
    form = DepForm()
    form.submit.label.text = "提交"
    department = Department.query.get_or_404(id)
    if request.method == "GET":
        form.dep_name.data = department.depart_name
        form.man_name.data = department.depart_manager
    if form.validate_on_submit():
        data = form.data
        department.depart_name = data["dep_name"]
        department.depart_manager = data["man_name"]
        db.session.add(department)
        db.session.commit()
        return make_response("<script>alert('修改成功');location.href='"+url_for('management.departlist')+"'</script>")
    return render_template("management/depart/updatedep.html",form=form)


#-----------------员工---------------------
@management.route('/addemp/',methods=['GET','POST'])
@admin_login
def addemp():
    form = EmpForm()
    dep_data = Department.query.order_by(Department.id)
    if request.method == 'POST':
        data = form.data
        dep_id = request.form.get('depart', '')
        dep_d = Department.query.get_or_404(dep_id)
        face_img = secure_filename(form.face_img.data.filename)
        if not os.path.exists(current_app.config['UP_DIR']):
            os.makedirs(current_app.config['UP_DIR'])
            os.chmod(current_app.config['UP_DIR'],"rw")
        face_dir = change_filename(face_img)
        form.face_img.data.save(current_app.config['UP_DIR'] + face_dir)

        employ = Employee(
            name=data['name'],
            depart=dep_d.depart_name,
            post='职员',
            face=face_dir,
            work_num=data['work_num'],
            depart_id = dep_d.id
        )
        dep_d.people_num = dep_d.people_num + 1
        db.session.add(employ)
        db.session.commit()
        db.session.add(dep_d)
        db.session.commit()
        return make_response("<script>alert('添加成功');location.href='"+url_for('management.addemp')+"'</script>")
    return render_template("management/employee/addemp.html",form=form,dep_data=dep_data)


@management.route('/emplist/',methods=['GET','POST'])
@admin_login
def emplist():
    page = request.args.get('page',1,type=int)
    keyword = request.args.get('keyword','',type=str)
    print(keyword)
    page_data = Employee.query.order_by(Employee.id).paginate(page=page, per_page=5)
    if keyword:
        filters = or_(Employee.name == keyword,Employee.depart == keyword)
        page_data = Employee.query.filter(filters).order_by(Employee.id).paginate(page=page,per_page=5)
    return render_template("management/employee/emp_table.html", data=page_data)


@management.route('/delemp/<int:id>',methods=['GET'])
@admin_login
def del_emp(id=None):
    employee = Employee.query.get_or_404(int(id))
    dep_data = Department.query.get_or_404(id)
    dep_data.people_num -= 1
    db.session.delete(employee)
    db.session.commit()
    db.session.add(dep_data)
    db.session.commit()
    return redirect(url_for('management.emplist'))


@management.route('/updateemp/<int:id>',methods=['GET','POST'])
@admin_login
def update_emp(id=None):
    form = EmpForm()
    form.submit.label.text = "提交"
    employee = Employee.query.get_or_404(id)
    dep_data = Department.query.order_by(Department.id)
    if request.method == "GET":
        form.post.data = employee.post
        form.name.data = employee.name
    if request.method == 'POST':
        data = form.data
        old_d = Department.query.get_or_404(employee.depart_id)
        employee.post = data["post"]
        employee.name = data["name"]
        dep_id = request.form.get('depart', '')
        dep_d = Department.query.get_or_404(dep_id)
        employee.depart = dep_d.depart_name
        employee.depart_id = dep_d.id
        if dep_id != employee.depart_id:
            dep_d.people_num = dep_d.people_num + 1
            old_d.people_num -= 1
        db.session.add(employee)
        db.session.commit()
        db.session.add(old_d)
        db.session.commit()
        return make_response("<script>alert('修改成功');location.href='"+url_for('management.emplist')+"'</script>")
    return render_template("management/employee/updateemp.html",form=form,emp=employee,dep_data=dep_data)


#-----------------公告---------------------
@management.route('/addnot/',methods=['GET','POST'])
@admin_login
def addnotice():
    form = NotForm()
    dep_data = Department.query.order_by(Department.id)
    if form.validate_on_submit():
        data = form.data
        dep_id = request.form.get('depart', '')
        dep_name = "全部"
        if dep_id != '0':
            dep_d = Department.query.get_or_404(dep_id)
            dep_name = dep_d.depart_name
            print(dep_name)
        notice = Notice(
            user_type=dep_name,
            type_id=dep_id,
            title=data['title'],
            author=data['author'],
            message=data['message']
        )
        db.session.add(notice)
        db.session.commit()
        return make_response("<script>alert('添加成功');location.href='"+url_for('management.addnotice')+"'</script>")
    return render_template("management/notice/addnotice.html",form=form,dep_data=dep_data)


@management.route('/noticelist/',methods=['GET','POST'])
@admin_login
def noticelist():
    page = request.args.get('page',1,type=int)
    keyword = request.args.get('keyword','',type=str)
    print(keyword)
    page_data = Notice.query.order_by(Notice.id).paginate(page=page, per_page=5)
    if keyword:
        filters = or_(Notice.user_type == keyword,Notice.title == keyword)
        page_data = Notice.query.filter(filters).order_by(Notice.id).paginate(page=page,per_page=5)
    return render_template("management/notice/notice_table.html", data=page_data)


@management.route('/notdetail/<int:id>',methods=['GET'])
@admin_login
def not_detali(id=None):
    notice = Notice.query.get_or_404(id)
    return render_template("management/notice/not_detail.html",notice=notice)


@management.route('/notdel/<int:id>',methods=['GET'])
@admin_login
def not_del(id=None):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for('management.noticelist'))

#考勤
@management.route('/attendset/',methods=['GET','POST'])
@admin_login
def attendset():
    form = AttendForm()
    if request.method == "POST":
        data = request.form
        work_hours = data['work_hours']
        month = data['month']
        print(type(month))
        # h1 = data['sh']
        # m1 = data['sm']
        # h2 = data['lh']
        # m2 = data['lm']
        attend_data = Attendance.query.filter(or_(Attendance.month==month)).first()
        if attend_data:
            attend_data.work_hours = work_hours
        else:
            attend_data = Attendance(
                month = month,
                work_hours=work_hours
            )
        db.session.add(attend_data)
        db.session.commit()
        return make_response("<script>alert('保存成功');location.href='"+url_for('management.attendset')+"'</script>")
    return render_template('management/attendance/setting.html',form=form)


@management.route('/attendtable/',methods=['GET','POST'])
@admin_login
def attendtable():
    attend_data = Attendance.query.all()
    return render_template('management/attendance/attentable.html',data=attend_data)


#薪资
@management.route('/salaryaccount/',methods=['GET','POST'])
@admin_login
def salaryaccount():
    attend_data = Attendance.query.all()
    form = SalaryForm()
    if request.method == 'POST':
        month = request.form.get('month')
        a = int(month)
        print(type(a),a)
        data = form.data
        insur_fund = (data['base_wage']+data['grant']-data['fine'])*0.12
        real_salary = data['base_wage']+data['grant']-data['fine']-insur_fund
        salary = Salary(
            work_id=data['work_id'],
            base_salary=data['base_wage'],
            grant=data['grant'],
            month=month,
            insur_fund=insur_fund,
            fine=data['fine'],
            real_salary=real_salary
        )
        db.session.add(salary)
        db.session.commit()
        return make_response("<script>alert('结算成功');location.href='"+url_for('management.attendset')+"'</script>")
    return render_template('management/salary/accountsalary.html',attend_data=attend_data,form=form)


@management.route('/salarytable/',methods=['GET'])
@admin_login
def salarytable():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '', type=str)
    print(keyword)
    page_data = Salary.query.order_by(Salary.id).paginate(page=page, per_page=5)
    if keyword:
        filters = or_(Salary.work_id == keyword, Salary.month == keyword)
        page_data = Salary.query.filter(filters).order_by(Salary.id).paginate(page=page, per_page=5)
    return render_template("management/salary/salarytable.html", data=page_data)


@management.route('/delsal/<int:id>',methods=['GET'])
@admin_login
def del_sal(id=None):
    salary = Salary.query.get_or_404(int(id))
    db.session.delete(salary)
    db.session.commit()
    return redirect(url_for('management.salarytable'))



