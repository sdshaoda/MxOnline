# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# import 顺序：Python、Django、自定义


# 用户信息，继承默认的 AbstractUser
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    # 可以为空 null=True, blank=True
    birthday = models.DateField(null=True, blank=True, verbose_name=u"生日")
    # choices 显示：get_gender_display
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="female")
    address = models.CharField(max_length=100, default="", verbose_name=u'地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'联系电话')
    # 存储的实际上是图片地址 根据时间存储 /%Y/%m  默认为default.png
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        # 重载显示的信息
        return self.username


# 邮箱验证码
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 邮箱及验证码在注册和找回密码处都会使用到
    send_type = models.CharField(
        max_length=10,
        choices=(("register", u"注册"), ("forget", u"找回密码")),
        verbose_name=u'验证码类型'
    )
    # datetime.now 注意不要带括号，否则会生成编译时的时间，而不是实例化时的时间；此字段可供设置过期时间
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        # 返回第一个参数是code，第二个是email，并且用一个括号
        return '{0}({1})'.format(self.code, self.email)


# 首页轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/&m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
