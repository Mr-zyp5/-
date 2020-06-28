import time

from django.db import models

# Create your models here.
#会员信息
class Users(models.Model):
    username = models.CharField(max_length=50,default='meiyou')
    password = models.CharField(max_length=100,default='123456')
    status = models.IntegerField(default=0)
    phone = models.CharField(max_length=11)
    sex = models.CharField(max_length=1,null=True,default=1)
    age = models.CharField(max_length=3,null=True,default=18)
    pic_url = models.CharField(max_length=100,default='/static/pics/default.png')
    addtime = models.DateTimeField(auto_now_add=True)
#商品分类
class Cates(models.Model):
    name = models.CharField(max_length=50)
    upid = models.IntegerField()
    paths = models.CharField(max_length=50)
# 商品
class Goods(models.Model):
    title = models.CharField(max_length=100)
    g_url = models.CharField(max_length=200)
    price = models.IntegerField()
    ordernum = models.IntegerField()
    ginfo = models.TextField()
    status = models.IntegerField(default=0)
    clickum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    cateid=models.ForeignKey(to='Cates',to_field='id',on_delete=models.CASCADE)

class Order(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)
    total = models.IntegerField()
    # 0 顺丰 1 申通 2圆通
    wl = models.IntegerField()

    pay = models.IntegerField()

    status = models.IntegerField(default=0)

    createtime = models.DateTimeField(auto_now_add=True)

    paytime = models.DateTimeField(null=True)

class Carts(models.Model):
    cdprice = models.IntegerField(default=0)
    cprice = models.IntegerField(default=0)
    csprice = models.IntegerField(default=0)
    cgoods_name = models.CharField(max_length=50)
    cgoods_pic = models.CharField(max_length=50)
    cgid = models.ForeignKey(to="Goods",to_field="id",on_delete=models.CASCADE)
    num = models.IntegerField(default=0)
    uid = models.ForeignKey(to="Users",to_field="id",on_delete=models.CASCADE)


class Citys(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    upid = models.IntegerField()
    class Meta():
        db_table='citys'


class Adress(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    sheng = models.CharField(max_length=100)
    shi = models.CharField(max_length=100)
    xian = models.CharField(max_length=100)
    addinfo = models.CharField(max_length=255)
    isselect = models.IntegerField(default=0)
    uid=models.ForeignKey(to="Users",to_field="id",on_delete=models.CASCADE)


class Orderinfo(models.Model):
    orderid =  models.ForeignKey(to="Order",to_field="id",on_delete=models.CASCADE)
    gid = models.ForeignKey(to="Goods",to_field="id",on_delete=models.CASCADE)
    num = models.IntegerField()
    price = models.IntegerField()

