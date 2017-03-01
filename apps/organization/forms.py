# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/25 20:46'
import re

from django import forms

from operation.models import UserAsk


# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


# 与 users.forms.py 中的不同，这里我们使用 ModelForm ，ModelForm 会继承在 Model 中定义的验证信息
class UserAskForm(forms.ModelForm):
    # my_field = forms.CharField()

    class Meta:
        # 在此处定义验证的 Model 和 Fields
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 追加验证。必须以 clean_ 开头
    def clean_mobile(self):
        # 固定用法，取值
        mobile = self.cleaned_data['mobile']
        # 正则表达式验证手机号
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            # 验证通过，返回值
            return mobile
        else:
            # 固定用法，返回错误信息
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')
