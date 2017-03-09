# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


# 所在城市
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 机构信息
class CourseOrg(models.Model):
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, default='pxjg', choices=(
        ('pxjg', u'培训机构'), ('gr', u'个人'), ('gx', u'高校')
    ), verbose_name=u'机构类别')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'机构logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    # 获取机构教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __unicode__(self):
        return self.name


# 教师信息
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名')
    work_years = models.CharField(default=0, max_length=2, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name=u'教师头像', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
