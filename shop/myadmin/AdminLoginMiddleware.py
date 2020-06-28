import re

from django.http import HttpResponse


class AdminLoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request):
        urlist = ['/myadmin/login/','/myadmin/verifycode/']
        print(request.path)
        if re.match('/myadmin/',request.path) and request.path not in urlist:
            if request.session.get('adminuser','')=='':
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/";</script>')
        response = self.get_response(request)
        return response