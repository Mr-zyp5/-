import os
import time

from django.core.paginator import Paginator

from shop.settings import BASE_DIR
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from .. import models




def adduser(request):
    if request.method=='GET':
        return render(request,'myadmin/adduser.html')
    elif request.method=='POST':
        #转换字典
        userinfo = request.POST.dict()
        userinfo.pop('csrfmiddlewaretoken')
        myfile = request.FILES.get('pic_url',None)
        print(myfile)
        if not myfile:
            return HttpResponse("<script>alert('请选择头像');location.href=''</script>")
        userinfo['pic_url'] = upload(myfile)
        userinfo['password'] = make_password(userinfo['password'],None,'pbkdf2_sha256')
        try:
            user = models.Users(**userinfo)
            user.save()
            return redirect(reverse('myadmin_vipuser'))
        except:
            return HttpResponse("<script>alert('添加失败！');location.href=''</script>")


def upload(myfile):
    filename = str(int((time.time())))+"."+myfile.name.split('.').pop()
    destination = open('./static/pics/'+filename,'wb+')
    for chunk in myfile.chunks():
        destination.write(chunk)
    destination.close()
    return '/static/pics/'+filename


def vipuser(request):
    userinfo = models.Users.objects.all()
    types = request.GET.get('type')
    search = request.GET.get('search')
    if types=='all':
        from django.db.models import Q
        userinfo = models.Users.objects.filter(Q(id__contains=search)|Q(username__contains=search)|Q(phone__contains=search))
    elif types=='uname':
        userinfo = models.Users.objects.filter(username=search)
    elif types=='uphone':
        userinfo = models.Users.objects.filter(phone=search)
    elif types=='uid':
        userinfo = models.Users.objects.filter(id=search)
    #实例化分页对象
    p = Paginator(userinfo,10)
    #一共可以分多少页
    sumpage=p.num_pages
    page = int(request.GET.get('p',1))
    page1 = p.page(page)
    # 判断显示前五个页码
    if page<=3:
        # 页码迭代
        prange = p.page_range[:5]
    elif page+2>=sumpage:
        prange = p.page_range[-5:]
    else:
        prange = p.page_range[page-3:page+2]
    return render(request,'myadmin/table-list.html',{'userinfo':page1,'prange':prange,'page':page,'sumpage':sumpage})


def dele(request):
    uid = request.GET.get('id')
    userinfo = models.Users.objects.get(id = uid)
    userinfo.delete()
    return render(request,'myadmin/table-list.html')


def updat(request):
    uid = request.GET.get('id')
    if request.method=='GET':
        userinfo = models.Users.objects.get(id=uid)
        return render(request,'myadmin/updateuser.html',{'info':userinfo})
    elif request.method=='POST':
        #转换字典
        try:
            userinfo = request.POST.dict()
            uinfo = models.Users.objects.get(id=uid)
            uinfo.username = userinfo['username']
            uinfo.phone = userinfo['phone']
            uinfo.age = userinfo['age']
            uinfo.sex = userinfo['sex']
            myfile = request.FILES.get('pic_url',None)
        except:
            return HttpResponse("<script>alert('信息有误，请重填信息');location.href=''</script>")
        if myfile:
            os.remove('.'+uinfo.pic_url)
            uinfo.pic_url = upload(myfile)
        try:
            uinfo.save()
            return redirect(reverse('myadmin_vipuser'))
        except:
            return HttpResponse("<script>alert('信息有误，修改失败！');location.href=''</script>")


def changes(request):
    uid = request.GET.get('uid')
    status = request.GET.get('status')
    user = models.Users.objects.get(id=uid)
    user.status = int(status)
    user.save()
    msg={'msg':'修改成功'}
    return JsonResponse(msg)


def changepwd(request):
    uid = request.GET.get('uid')
    user = models.Users.objects.get(id=uid)
    user.password = make_password('123456',None,'pbkdf2_sha256')
    user.save()
    data={'msg':'修改成功'}
    return JsonResponse(data)