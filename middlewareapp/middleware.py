from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin

from userapp.models import Users

class MyMiddleware(MiddlewareMixin):          # 自定义的中间件
    def __init__(self ,get_response)  :  # 初始化
        super().__init__(get_response)
        print("init1")

    # view处理请求前执行
    def process_request(self ,request):  # 某一个view
        if 'userapp/' not in  request.path:
            print('登录验证')
            session=request.session
            if session.get('login'):
                print('已登录')
            else:
                print('未登录')
                return render(request,'userapp/login.html')
        else:
            print('正在登录')

    def process_response(self, request, response):
        print("response:", request, response)
        return response  # 持续返回响应