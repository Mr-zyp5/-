from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from myadmin import models


def addcate(request):
    if request.method=='GET':
        cates = models.Cates.objects.all()
        print(cates)
        for i in cates:
            num = i.paths.count(',')-1
            i.newname=num*'|----'
        return render(request,'myadmin/cate/addcate.html',{'cates':cates})
    elif request.method=='POST':
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        if pid == '0':
            cate = models.Cates()
            cate.name=name
            cate.upid=int(pid)
            cate.paths='0,'
            cate.save()
        else:
            pobj = models.Cates.objects.get(id=pid)
            c = models.Cates()
            c.name=name
            c.upid=pobj.id
            c.paths=pobj.paths+pid+','
            c.save()
        return HttpResponse("<script>alert('添加成功！');location.href='addcate'</script>")


def tab():
    cates = models.Cates.objects.extra(select={'newpath':'concat(paths,id)'}).order_by('newpath')
    for i in cates:
        num = i.paths.count(',')-1
        i.newname=num*'|----'
    return cates

def catelist(request):
    cates = tab()
    return render(request,'myadmin/cate/catelist.html',{'cates':cates})


def delcate(request):
    #接收id
    pid = int(request.GET.get('pid'))
    # 查看有没有子类
    cnum = models.Cates.objects.filter(upid=pid).count()
    print(cnum)
    if cnum:
        return  JsonResponse({'msg':0})
    else:
        c = models.Cates.objects.get(id=pid)
        c.delete()
    return JsonResponse({'msg':1})


def editcate(request):
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        cate = models.Cates.objects.get(id=cid)
        cate.name=cname
        cate.save()
        return JsonResponse({'msg':1})
    except:
        return JsonResponse({'msg':0})