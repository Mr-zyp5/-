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
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path('^$', views.index,name='myhome_index'),
    re_path(r'^adminlogin/$',views.adminlogin,name='myhome_login'),
    re_path(r'^out/',views.outlogin,name='myhome_out'),
    re_path(r'^adminregister/',views.reigster,name='myhome_register'),
    re_path(r'^adminlist/(?P<cid>[0-9]+)/(?P<bid>[0-9]+)/$',views.adminlist,name='myhome_list'),
    re_path(r'^admincheck/',views.admincheck,name='myhome_check'),
    re_path(r'^admindetail/(?P<gid>[0-9]+)/(?P<cid>[0-9]+)/$', views.admindetail, name='myhome_detail'),
    #购物车
    re_path(r'^admincart/', views.admincart, name='myhome_cart'),
    re_path(r'^admindelcart/', views.admincartdelcate, name='myhome_delcart'),
    re_path(r'^caredit/', views.caredit, name='myhome_caredit'),
    # 订单
    re_path(r'^adminorder/', views.adminorder, name='myhome_order'),
    re_path(r'^adminmyorder/', views.adminmyorder, name='myhome_myorder'),
    re_path(r'^adminpersonal/', views.adminpersonal, name='myhome_personal'),
    #地址
    re_path(r'^getcitys/', views.getcitys, name='myhome_getcitys'),
    re_path(r'^saveaddress/$',views.saveaddress,name='myhome_saveaddress'),
    #生成订单
    re_path(r'^createorder/$',views.createorder,name='myhome_create'),
    # 支付页面
    re_path(r'^myhome_order_pay/$', views.myhome_order_pay, name='myhome_order_pay'),

    # 支付回调
    re_path(r'^order/pay_result/', views.myhome_pay_result, name="myhome_pay_result"),
]
