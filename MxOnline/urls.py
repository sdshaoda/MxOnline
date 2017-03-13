# coding:utf-8
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from MxOnline.settings import MEDIA_ROOT
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, ModifyPwdView

urlpatterns = [
    # 后台管理系统，使用了 xadmin
    url(r'^xadmin/', xadmin.site.urls),
    # 首页，注意不能写成 r'^/$'，在这里我们直接返回一个模板文件
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # 验证码，使用了第三方库
    url(r'^captcha/', include('captcha.urls')),
    # 文件上传
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 退出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 注册
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 激活。取 URL 中的字符， active_code 将作为参数传递到 ActiveUserView
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 忘记密码
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 重置密码的 GET URL
    url(r'^reset/(?P<active_code>.*)/$', ResetUserView.as_view(), name='reset_pwd'),
    # 重置密码的 POST URL
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构相关 URL ，注意这里不能有 $ 符号
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程相关 URL
    url(r'^course/', include('courses.urls', namespace='course')),
]
