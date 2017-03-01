# _*_ coding:utf-8 _*_
from captcha.fields import CaptchaField
from django import forms


# 继承 Django 内置的 form 验证，并结合验证码验证

# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=6, max_length=20)
    password = forms.CharField(required=True, min_length=6, max_length=20)


# 注册表单
class RegisterForm(forms.Form):
    # EmailField 会自动验证邮箱格式
    email = forms.EmailField(required=True)
    # 验证名需同 POST 传递的字段名一致
    password = forms.CharField(required=True, min_length=6, max_length=20)
    # error_messages 自定义错误信息
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 忘记密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 重置密码表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)
