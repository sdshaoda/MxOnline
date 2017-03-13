# coding:utf-8
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # 设置显示的别名
    verbose_name = u'用户信息'
