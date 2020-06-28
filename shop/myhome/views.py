from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from myadmin import models

def index(request):
    cates = models.Cates.objects.all()
    goods = models.Goods.objects.all()
    return render(request,'myhome/index.html',{'cates':cates,'goods':goods})


def adminlogin(request):
    if request.method == 'GET':
        # 记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'myhome/login.html')
    elif request.method == 'POST':
        info = request.POST.dict()
        try:
            user = models.Users.objects.get(phone=info['user'])
            status = user.status
            print(status,type(status))
            if status == 0:
                upass = check_password(info['password'],user.password)
                if upass:
                    request.session['userinfo'] = {'vipuser':user.username,'uid':user.id}
                    if request.session['login_from'] == 'http://127.0.0.1:8000/adminregister/':
                        return HttpResponse(
                            '<script>alert("登录成功");location.href="' + reverse("myhome_index") + '"</script>')
                    return HttpResponseRedirect(request.session['login_from'])
                else:
                    return HttpResponse('<script>alert("帐号或密码错误");history.back(-1)</script>')
            else:
                return HttpResponse('<script>alert("帐号已经被禁用");history.back(-1)</script>')
        except:
            return HttpResponse('<script>alert("帐号或密码错误");history.back(-1)</script>')



def adminlist(request,cid,bid):
    ob1 = models.Cates.objects.get(id=cid)
    ob2 = models.Cates.objects.filter(upid=cid)
    goods = []
    bid = int(bid)
    for cate2 in ob2:
        if bid == 0:
            goods.append(cate2.goods_set.all())
        else:
            if cate2.id == bid:
                goods.append(cate2.goods_set.all())
    content = {'cate1':ob1,'cate2':ob2,'goods':goods,'color':bid}
    return render(request,'myhome/list.html',content)


def reigster(request):
    if request.method == 'GET':
        return render(request, 'myhome/register.html')
    elif request.method == 'POST':
        # 接受用户的数据
        userinfo = request.POST.dict()
        # 1.判断用户是否输入信息
        if userinfo['phone'] == '' or userinfo['password'] == '':
            return HttpResponse(
                '<script>alert("你的信息填写不完整");location.href="' + reverse("myhome_register") + '"</script>')

        # 2.判断手机号是否已经被注册
        flage = models.Users.objects.filter(phone=userinfo['phone']).count()
        print(flage)
        if flage:
            # 如果已经存在 就返回提示信息
            return HttpResponse('<script>alert("手机好已经存在");history.back(-1)</script>')
        else:
            # 手机号可用
            # 判断验证码
            try:
                # 存数据
                newuser = models.Users()
                newuser.phone = userinfo['phone']
                newuser.password = make_password(userinfo['password'], None, 'pbkdf2_sha256')
                newuser.save()
                return HttpResponse(
                    '<script>alert("注册成功，请登录");location.href="' + reverse("myhome_login") + '"</script>')
            # try:
            #     if userinfo['yzm'] == request.session['msgcode']['code'] and userinfo['phone'] == \
            #             request.session['msgcode']['phone']:
            #         # 存数据
            #         newuser = models.Users()
            #         newuser.username = userinfo['username']
            #         newuser.phone = userinfo['phone']
            #         newuser.password = make_password(userinfo['password'], None, 'pbkdf2_sha256')
            #         newuser.save()
            #         return HttpResponse(
            #             '<script>alert("注册成功，请登录");location.href="' + reverse("myhome_login") + '"</script>')
            #     else:
            #         return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
            except:
                return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')



def admincheck(request):
    import urllib
    import urllib.request
    import json
    import random
    # 用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account = "C90975192"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "870d779f233aa6b2065406c09f6c02fc"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000, 99999))
    # 把验证码存入session
    request.session['msgcode'] = {'code': code, 'phone': mobile}
    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'}
    req = urllib.request.urlopen(
        url='http://106.ihuyi.com/webservice/sms.php?method=Submit',
        data=urllib.parse.urlencode(data).encode('utf-8')
    )
    content = req.read()
    res = json.loads(content.decode('utf-8'))
    print(res)
    # return HttpResponse(res)
    return JsonResponse(res)


def outlogin(request):
    del request.session['userinfo']
    return HttpResponse('<script>alert("退出成功");location.href="' + reverse('myhome_index') + '"</script>')


def admincart(request):
    uid = request.session.get('userinfo')
    if not uid:
        return HttpResponse('<script>alert("请您先登录");location.href="'+reverse('myhome_login')+'"</script>')
    carts = models.Carts.objects.all()
    content = {'carts':carts}
    return render(request,'myhome/cart.html',content)


def adminorder(request):
    try:
        cart = request.GET.get('cid').split(',')
        cargoods=models.Carts.objects.filter(id__in=cart)
        citys = models.Citys.objects.filter(upid=0)
        address = models.Adress.objects.all()
        return render(request,'myhome/pay.html',{'cargoods':cargoods,'citys':citys,'address':address})
    except:
        return HttpResponse(
            '<script>alert("请把商品加入购物车!");location.href="' + reverse("myhome_index") + '"</script>')


def admindetail(request,gid,cid):
    goods = models.Goods.objects.get(id=gid)
    if request.method == 'GET':
        cname = models.Cates.objects.get(id=cid)
        content = {'goods':goods,'cname':cname}
        return render(request,'myhome/detail.html',content)
    elif request.method == 'POST':
        try:
            uobj = models.Users.objects.get(id=request.session['userinfo']['uid'])
            cnum = request.POST.dict()
            num = cnum['num']
            cart = models.Carts()
            cobj = models.Carts.objects.filter(uid=request.session['userinfo']['uid'])
            print(cobj,'/n========================')
            print([i.cgid for i in cobj])
            if goods.id in [i.cgid.id for i in cobj]:
                for i in cobj:
                    if goods.id == i.cgid.id:
                        cobj1 = models.Carts.objects.get(cgid=goods.id)
                        cobj1.num += int(num)
                        cobj1.save()
            else:
                cart.num=num
                cart.cdprice = goods.price
                cart.cgoods_name = goods.title
                cart.cgoods_pic = goods.g_url
                cart.cgid = goods
                cart.uid = uobj
                cart.save()
            return HttpResponse(
                        '<script>location.href="' + reverse("myhome_cart") + '"</script>')
        except:
            return HttpResponse('<script>alert("请您先登录！");history.back(-1)</script>')

def admincartdelcate(request):
    gid = request.GET.get('id')
    ginfo = models.Carts.objects.get(id=gid)
    ginfo.delete()
    return HttpResponse(
                        '<script>location.href="' + reverse("myhome_cart") + '"</script>')


def caredit(request):
    cinfo = request.GET.dict()
    cobj = models.Carts.objects.get(id=cinfo['cid'])
    cobj.num = int(cinfo['num'])
    cobj.save()
    return JsonResponse({'error':1,'msg':'修改成功'})


def getcitys(request):
    upid = request.GET['upid']
    citys = models.Citys.objects.filter(upid=upid).values()
    return JsonResponse(list(citys),safe=False)


def saveaddress(request):
    addinfo = request.GET.dict()
    address = models.Adress()
    address.name = addinfo['name']
    address.phone = addinfo['phone']
    address.sheng = models.Citys.objects.get(id=addinfo['sheng']).name
    address.xian = models.Citys.objects.get(id=addinfo['xian']).name
    address.shi = models.Citys.objects.get(id=addinfo['shi']).name
    address.addinfo = addinfo['addinfo']
    address.uid = models.Users.objects.get(id=request.session['userinfo']['uid'])
    address.save()
    return JsonResponse({'error': 0, 'msg': '添加成功'})


def createorder(request):
    oinfo = request.POST.dict()
    order = models.Order()
    order.uid = models.Users.objects.get(id=request.session['userinfo']['uid'])
    try:
        order.phone = models.Adress.objects.get(id=oinfo['dizhi']).phone
        order.name = models.Adress.objects.get(id=oinfo['dizhi']).name
        # 地址
        sheng = models.Adress.objects.get(id=oinfo['dizhi']).sheng
        shi = models.Adress.objects.get(id=oinfo['dizhi']).shi
        xian = models.Adress.objects.get(id=oinfo['dizhi']).xian
        addinfo = models.Adress.objects.get(id=oinfo['dizhi']).addinfo
        addinfo = sheng + shi + xian + addinfo
        order.addinfo = addinfo
        order.wl = int(oinfo['wuliu'])
        order.pay = int(oinfo['zhifu'])
        order.total = 0
        order.save()
        total = 0
        carts = models.Carts.objects.filter(id__in=oinfo['car'].split(','))
        for i in carts:
            orderinfo = models.Orderinfo()
            orderinfo.orderid = order
            orderinfo.num = i.num
            orderinfo.price = i.cgid.price
            orderinfo.gid = i.cgid
            orderinfo.save()
            total += i.num * i.cgid.price
            i.delete()
        order.total = total
        order.save()
        return HttpResponse('<script>location.href="'+reverse('myhome_order_pay')+'?orderid='+str(order.id)+'"</script>')
    except:
        return HttpResponse('<script>alert("请您选择地址！");history.back(-1)</script>')


# 订单支付
def myhome_order_pay(request):
    # 接收订单号
    orderid = request.GET.get('orderid')
    # 获取订单对象
    order = models.Order.objects.get(id=orderid)
    print(orderid)
    # 获取支付对象
    alipay = Get_AliPay_Object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="魅族旗舰官网",  # 商品简单描述
        out_trade_no = orderid,# 用户购买的商品订单号
        total_amount = order.total,  # 交易金额(单位: 元 保留俩位小数)
    )
    print(query_params)
    # 支付宝网关地址（沙箱应用）
    pay_url = settings.ALIPAY_URL+"?{0}".format(query_params)
    print(pay_url)
    # 页面重定向到支付页面
    return redirect(pay_url)




# 支付的回调函数
# 支付宝回调地址
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def myhome_pay_result(request):
    # 获取对象
    alipay = Get_AliPay_Object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        models.Order.objects.filter(id=out_trade_no).update(status=1)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')

        return HttpResponse('<script>alert("支付成功");location.href="' + reverse("myhome_myorder") + '"</script>')


from shop import settings
from utils.pay import AliPay

# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,# APPID （沙箱应用）
        app_notify_url=settings.ALIPAY_NOTIFY_URL, # 回调通知地址
        return_url=settings.ALIPAY_NOTIFY_URL,# 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH, # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay


def adminpersonal(request):
    try:
        uojb = models.Users.objects.get(id=request.session['userinfo']['uid'])
        info = {'info':uojb}
        return render(request,'myhome/member.html',info)
    except:
        return HttpResponse('<script>alert("请您先登录！");history.back(-1)</script>')


def adminmyorder(request):
    try:
        uojb =models.Order.objects.filter(uid = request.session['userinfo']['uid'])
        print(uojb)
        myobj = []
        for i in uojb:
            print(i.id)
            myobj.append(models.Orderinfo.objects.filter(orderid=i.id))
        print(myobj)
        return render(request,'myhome/order.html',{'myobj':myobj,'uojb':uojb})
    except:
        return HttpResponse('<script>alert("请您先登录！");history.back(-1)</script>')