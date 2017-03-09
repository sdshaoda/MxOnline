# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView

urlpatterns = [
    # 公开课，课程列表
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节页
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),
]
