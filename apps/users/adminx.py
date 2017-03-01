# _*_ coding:utf-8 _*_
import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner


# 修改 xadmin 的默认显示
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 修改 xadmin 的默认显示
class GlobalSettings(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


# 通用 xadmin 的写法
class UserProfileAdmin(object):
    # 在列表中显示的项
    list_display = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    # 搜索支持的字段
    search_fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']
    # 过滤器
    list_filter = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'image']


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 将 Admin 注册到 Model 中
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 重设基本设置
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
