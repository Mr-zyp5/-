import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from myadmin import models
from myadmin.views import cate_views, user_views
from myadmin.views.user_views import upload


def addgoods(request):
    types = cate_views.tab()
    return render(request,'myadmin/goods/addgoods.html',{'types':types})


def goodslist(request):
    goods = models.Goods.objects.all()
    return render(request,'myadmin/goods/goodslist.html',{'goods':goods})


def goodsinsert(request):
    ginfo = request.POST.dict()
    ginfo.pop('csrfmiddlewaretoken')
    file = request.FILES.get('g_url')
    if not file:
        return HttpResponse('<script>alert("请选择图片");history.back(-1)</script>')
    g_url = user_views.upload(file)
    goods = models.Goods()
    try:
        goods.title = ginfo['title']
        goods.g_url=g_url
        goods.ginfo=ginfo['ginfo']
        goods.ordernum = ginfo['ordernum']
        goods.price = ginfo['price']
        goods.cateid = models.Cates.objects.get(id=ginfo['cateid'])
        goods.save()
        return redirect(reverse('myadmin_goodslist'))
    except:
        return HttpResponse("<script>alert('信息有误,添加失败！');location.href=''</script>")


def goodsdelete(request):
    gid = request.GET.get('id')
    ginfo = models.Goods.objects.get(id=gid)
    ginfo.delete()
    return redirect(reverse('myadmin_goodslist'))


def goodsedit(request):
    gid = request.GET.get('id')
    if request.method=='GET':
        types = cate_views.tab()
        ginfo = models.Goods.objects.get(id=gid)
        return render(request,'myadmin/goods/editgoods.html',{'ginfo':ginfo,'types':types})
    elif request.method=='POST':
        try:
            ninfo = request.POST.dict()
            ginfo = models.Goods.objects.get(id=gid)
            ginfo.title = ninfo['title']
            ginfo.ordernum = ninfo['ordernum']
            ginfo.cateid_id = ninfo['cateid']
            ginfo.price = ninfo['price']
        except:
            return HttpResponse("<script>alert('信息填写有误，请检查！');location.href=''</script>")
        myfile = request.FILES.get('g_url')
        if myfile:
            os.remove('.'+ginfo.g_url)
            ginfo.g_url = upload(myfile)
        try:
            ginfo.save()
            return redirect(reverse('myadmin_goodslist'))
        except:
            return HttpResponse("<script>alert('信息有误,修改失败！');location.href=''</script>")


