# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/27 17:47'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 公开课，课程列表
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
]
