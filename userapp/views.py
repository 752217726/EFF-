import hashlib
import random
import string
import traceback
import uuid

from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
# Create your views here.
from EFF import settings
from userapp.captcha.image import ImageCaptcha
from userapp.models import Users


def register(request):
    return render(request,'userapp/register.html')

def register_logic(request):
    try:
        name=request.POST.get('user_name')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')
        email=request.POST.get('email')
        allow=request.POST.get('allow')
        #密码加盐
        salt=str(uuid.uuid4())
        ha=hashlib.sha256()
        new_pwd=pwd + salt
        ha.update(new_pwd.encode())
        rst=ha.hexdigest()
        if pwd==cpwd and allow:
            rst1=Users.objects.create(name=name,pwd=rst,email=email,salt=salt)
            if rst1:
                id=rst1.id
                ser=serializer(settings.SECRET_KEY,expires_in=180)
                s=ser.dumps({'id':id}).decode()
                try:
                    send_mail('账户激活','http://127.0.0.1:8000/userapp/active/?token='+s,'752217726@qq.com',['78798465@qq.com'])
                    return JsonResponse({'msg':'注册成功,请等待管理员激活账户','status':1})
                except:
                    return JsonResponse({'msg':'发送邮件失败','status':0})
            else:
                return JsonResponse({'msg':'注册失败','status':0})
    except:
        return JsonResponse({'msg':'注册失败','status':0})

#检查注册的用户名是否存在
def check_name(request):
    name=request.POST.get('name')
    print(name)
    if Users.objects.filter(name=name):
        return HttpResponse('error')
    return HttpResponse('ok')


#生成验证码图片
def setImage(request):
    # 1.使用ImageCaptcha
    img=ImageCaptcha()
    # 2.生成随机码 大小写数字
    rst=random.sample(string.ascii_letters+string.digits,5)  #列表
    # 3.完成最终验证码图片
    # 对  列表进行 转换 成字符串
    code=''.join(rst)
    request.session['randcode']=code
    data=img.generate(code)
    return HttpResponse(data,'image/jpg')

# 验证逻辑
def captch_logic(request):
    rst = request.GET.get('val')
    print(rst)
    sessioncode = request.session.get('randcode')
    print(rst.lower(),sessioncode.lower())
    if rst.lower() == sessioncode.lower():
        return HttpResponse('验证成功')
    return HttpResponse('error')


def login(request):
    rst1 = request.COOKIES.get('user')
    rst2 = request.COOKIES.get('pwd')
    print(rst1,rst2)
    if rst1 and rst2:
        request.session['login']=True
        return redirect('operations:show')
    return render(request,'userapp/login.html')

def login_logic(request):
    try:
        name=request.POST.get('username')
        rst=Users.objects.filter(name=name)
        rem = request.POST.get('rem')
        print(rem)
        if rst:
            obj=rst[0]
            if obj.is_active:
                request.session['login'] = True
                pwd=request.POST.get('pwd')
                salt=obj.salt
                ha = hashlib.sha256()
                new_pwd = pwd + salt
                ha.update(new_pwd.encode())
                if ha.hexdigest() == obj.pwd:
                    res=JsonResponse({'msg':'登录成功','status':1})
                    if rem:
                        res.set_cookie('user','true',max_age=7*24*3600)
                        res.set_cookie('pwd','true',max_age=7*24*3600)
                    return res
                else:
                    return JsonResponse({'msg':'用户名或密码有误!','status':0})
            else:
                return JsonResponse({'msg':'该账户未做激活','status':-1})
        else:
            return JsonResponse({'msg':'用户名或密码有误!','status':0})
    except:
        return JsonResponse({'msg': '登录 失败', 'status': 0})


def forget_pwd(request):
    return render(request,'userapp/forget_pwd.html')

#忘记密码处理逻辑
def forget_pwd_logic(request):
    try:
        name=request.POST.get('user_name')
        email=request.POST.get('email')
        user=Users.objects.filter(name=name,email=email)
        print(user)
        if user:
            #邮件内容加密
            id=user[0].id
            ser=serializer(settings.SECRET_KEY,expires_in=180)
            s=ser.dumps({'id':id}).decode()
            try:
                #发送邮件
                send_mail('忘记密码','http://127.0.0.1:8000/userapp/resetpwd/?token='+s,'752217726@qq.com',['78798465@qq.com'])
                return JsonResponse({'msg': '发送忘记密码邮件成功,请等待管理员审核', 'status': 1})
            except:
                return JsonResponse({'msg': '用户或者邮箱不存在,请重新输入', 'status': 0})
        else:
            return JsonResponse({'msg': '用户或者邮箱不存在,请重新输入', 'status': 0})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '用户或者邮箱不存在,请重新输入', 'status': 0})

def reset_pwd(request):
    token=request.GET.get('token')
    print(token)
    try:
        ser = serializer(settings.SECRET_KEY, expires_in=180)
        user_id = ser.loads(token).get("id")
        print(user_id)
        if Users.objects.filter(pk=user_id):
            request.session['user_id'] = user_id
            return render(request, 'userapp/reset_pwd.html')
        return HttpResponse('token无效！')
    except:
        return HttpResponse('不好意思，链接已经失效！')

#重置密码处理逻辑
def reset_pwd_logic(request):
    user_id=request.session.get('user_id')
    try:
        rst = Users.objects.get(pk=user_id)
        print(rst)
        pwd=request.POST.get('user-pwd')
        print(pwd)
        pwd1=request.POST.get('confirm-pwd')
        if pwd == pwd1:
            try:
                if rst:
                    with transaction.atomic():
                        #密码加盐
                        ha = hashlib.sha256()
                        salt = rst.salt
                        new_pwd = pwd + salt
                        ha.update(new_pwd.encode())
                        rst.pwd = ha.hexdigest()
                        rst.save()
                        del request.session['user_id']
                        print(rst.pwd)
                        return JsonResponse({'msg': '重置密码成功，即将回到登陆页面', 'status': 1})
                else:
                    return JsonResponse({'msg': '重置密码失败', 'status': 0})
            except:
                traceback.print_exc()
                return JsonResponse({'msg': '重置密码失败', 'status': 0})
        else:
            return JsonResponse({'msg': '两次输入不一致', 'status': 0})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '重置密码失败', 'status': 0})

def home(request):
    status=request.session.get('login')
    if status:
        return render(request, 'operations/home.html')
    return redirect('userapp:login')

def logout(request):
    return render(request,'userapp/logout.html')

# 激活视图函数
def active(request):
    # 1.激活账户
    # 2.数据库查询该条数据(接收),修改is_active 字段值 修改成True，并保存，则激活成功
    temp_s=request.GET.get('token')
    # 解密 得到id
    ser = serializer(settings.SECRET_KEY, expires_in=180)
    s = ser.loads(temp_s)  #反序列化之后是一个字典 取键值
    print(s.get('id'))
    rst=Users.objects.filter(id=s.get('id'))
    if rst:
        obj=rst[0]
        if obj.is_active:
            return HttpResponse('该账户'+ str(obj.name) + '已经审核过了!')
        else:
            obj.is_active=True
            obj.save()
            return HttpResponse('恭喜'+ str(obj.name) + '账户成功激活!')

def reactive(request):
    try:
        name=request.GET.get('username')
        user=Users.objects.get(name=name)
        id=user.id
        print(id)
        ser = serializer(settings.SECRET_KEY, expires_in=180)
        s = ser.dumps({'id': id}).decode()
        send_mail('账户激活', 'http://127.0.0.1:8000/userapp/active/?token=' + s, '752217726@qq.com', ['78798465@qq.com'])
        return JsonResponse({'msg':'发送激活邮件成功','status':1})
    except:
        traceback.print_exc()
        return JsonResponse({'msg':'发送激活邮件失败','status':0})