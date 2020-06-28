"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from myadmin.views import user_views,index_views,cate_views,goods_views
from myadmin.views import order_views

urlpatterns = [
    re_path(r'^index/$', index_views.index, name='myadmin_index'),
    re_path(r'^login/$',index_views.login,name='myadmin_login'),
    re_path(r'^verifycode/$',index_views.verifycode,name='myadmin_yzm'),
    re_path(r'^outlogin/$',index_views.outlogin,name='myadmin_out'),
    #用户管理
    re_path(r'^vipuser/$',user_views.vipuser,name='myadmin_vipuser'),
    re_path(r'^adduser/$',user_views.adduser,name='myadmin_adduser'),
    re_path(r'^deleteuser/$',user_views.dele),
    re_path(r'^updateuser/$',user_views.updat,name='myadmin_updateuser'),
    re_path(r'^changes/$',user_views.changes,name='myadmin_changes'),
    re_path(r'^changepwd',user_views.changepwd,name='myadmin_changepwd'),
    #商品分类
    re_path(r'^catelist',cate_views.catelist,name='myadmin_catelist'),
    re_path(r'^addcate',cate_views.addcate,name='myadmin_addcate'),
    re_path(r'^delcate',cate_views.delcate,name='myadmin_delcate'),
    re_path(r'^editcate',cate_views.editcate,name='myadmin_editcate'),
    #商品管理
    re_path(r'^addgoods',goods_views.addgoods,name='myadmin_addgoods'),
    re_path(r'^goodslist',goods_views.goodslist,name='myadmin_goodslist'),
    re_path(r'^goodsinsert',goods_views.goodsinsert,name='myadmin_goodsinsert'),
    re_path(r'^goodsdelete',goods_views.goodsdelete,name='myadmin_goodsdelete'),
    re_path(r'^goodsedit',goods_views.goodsedit,name='myadmin_goodsedit'),
    #订单管理
    re_path(r'^orderlist', order_views.orderlist, name='myadmin_orderlist'),
    re_path(r'^editorder', order_views.editorder, name='myadmin_editorder'),
]
