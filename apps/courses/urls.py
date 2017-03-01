# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/27 17:47'

from django.conf.urls import url

from .views import CourseListView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
]
