# _*_ encoding:utf-8 _*_
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from utils.email_send import send_register_email
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord


# 重载 authenticate 方法
class CustomBackend(ModelBackend):
    # 默认写法
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 可以使用 username 或 email 登录
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # password 已加密，需要使用继承的 AbstractUser 中的 check_password 方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录页。继承 Django 内置的 View
class LoginView(View):
    def get(self, request):
        # GET method
        return render(request, 'login.html')

    def post(self, request):
        # 接收到 post method 后，首先使用 form 验证
        login_form = LoginForm(request.POST)
        # 有时需要先执行这个 is_valid 才会出现正常的错误提示信息
        login_form.is_valid()
        if login_form.is_valid():
            # 格式验证通过
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 验证数据库信息
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    # 用户存在且激活，进入首页
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    # 未激活，返回到登录页面
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                # 用户名密码错误。因为要保存用户上次使用的表单信息，所以将 login_form 传递进来
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            # 格式验证未通过。login_form 返回错误信息
            return render(request, 'login.html', {'login_form': login_form})


# 激活页
class ActiveUserView(View):
    # 获取 URL 中的 active_code
    def get(self, request, active_code):
        # 查询数据库记录中是否有此 active_code 的记录
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            # 取到的是数组，所以这里要循环
            for record in all_records:
                email = record.email
                # 取到匹配的 Model
                user = UserProfile.objects.get(email=email)
                # 激活用户
                user.is_active = True
                # 将修改保存在数据库中
                user.save()
        else:
            # 没有查到记录
            return HttpResponse('链接失效！')
        return render(request, 'login.html')


# 注册页。因为返回视图响应，所以命名后缀为-View
class RegisterView(View):
    def get(self, request):
        # 实例化 RegisterForm ，因为要用到 register_form 生成验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 需要传入 POST 信息
        register_form = RegisterForm(request.POST)
        register_form.is_valid()
        if register_form.is_valid():
            # 从 POST 请求中获取参数，不存在则为空
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                # 数据库中已有此用户邮箱
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')

            # 实例化一个 Model
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 设置用户为未激活状态
            user_profile.is_active = False
            # 要对密码进行加密保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送验证码到邮箱
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 忘记密码页
class ForgetPwdView(View):
    def get(self, request):
        # 实例化 ForgetForm ，因为要用到 register_form 生成验证码
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        forget_form.is_valid()
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送邮件
            send_register_email(email, 'forget')
            return HttpResponse('邮件已发送，请查收！')
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码页 GET
class ResetUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return HttpResponse('链接失效！')
        return render(request, 'login.html')


# 重置密码页 POST。因为GET 的 URL 中有 active_code 参数，表单 action 无法获取其值，所以对于 POST 我们需要另写一个 View
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        modify_form.is_valid()
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                # 两次密码不一致
                return render(request, 'password_reset.html', {'email': email, 'msg': '两次密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            # 格式验证未通过
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})

# # 使用函数的方法，被使用类的方法重写
# # 不能和默认的 login 名称重复
# def user_login(request):
#     print request.method
#     print request
#     # 注意 POST 大写
#     if request.method == 'POST':
#         # 通过表单数据提交
#         # 取请求中的字段
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         # 向数据库验证，参数为需要检查的字段
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             # 通过验证，转到 index 页面
#             # 自带的 login ，原理：session cookie
#             login(request, user)
#             # Django会向前端模板页面注入request对象，并能通过它完成身份验证
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':
#         # 通过URL地址
#         return render(request, 'login.html', {})
