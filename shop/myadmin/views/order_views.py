from django.http import JsonResponse
from django.shortcuts import render

from myadmin import models


def editorder(request):
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        orderob = models.Order.objects.get(id=cid)
        if int(cname) in [0,1,2]:
            orderob.status=cname
            orderob.save()
        else:
            orderob.total = cname
            orderob.save()
        return JsonResponse({'msg':1})
    except:
        return JsonResponse({'msg':0})


def orderlist(request):
    orderobj = models.Order.objects.all()
    return render(request,'myadmin/order/orderlist.html',{'orderobj':orderobj})