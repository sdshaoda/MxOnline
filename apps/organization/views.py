# _*_ coding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from operation.models import UserFavorite
from .forms import UserAskForm
from .models import CourseOrg, CityDict


class OrgView(View):
    # 课程机构列表功能
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        host_orgs = all_orgs.order_by('-click_nums')[:3]

        # 取出 URL 查询字符串中的 city 值，城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出 URL 查询字符串中的 ct 值，机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 进一步筛选：“全部”、“学习人数”、“课程数”
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                # - 倒序排列
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 统计符合筛选条件的课程数
        org_nums = all_orgs.count()

        # 使用插件 pure_pagination ，对课程机构进行分页。从 URL 中取 page 默认为 1
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 每页显示个数为 5
        p = Paginator(all_orgs, 5, request=request)
        # 取到当前页的数组
        page_orgs = p.page(page)

        return render(request, 'org-list.html', {
            'page_orgs': page_orgs,
            'org_nums': org_nums,
            'all_citys': all_citys,
            'city_id': city_id,
            'category': category,
            'host_orgs': host_orgs,
            'sort': sort,
        })


# 用户咨询 POST 处理
class AddUserAskView(View):
    def post(self, request):
        # 验证
        userask_form = UserAskForm(request.POST)
        userask_form.is_valid()
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # Ajax Async，返回 JSON 数据
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 返回的数据交由前端渲染页面
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'has_fav': has_fav,
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers
        })


# 机构课程列表首页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        # 检查用户是否已收藏机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'has_fav': has_fav,
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses
        })


# 机构介绍页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 检查用户是否已收藏机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'has_fav': has_fav,
            'current_page': current_page,
            'course_org': course_org,
        })


# 机构讲师列表首页
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()

        # 检查用户是否已收藏机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'has_fav': has_fav,
            'current_page': current_page,
            'course_org': course_org,
            'all_teacher': all_teacher
        })


# 用户收藏 POST 处理
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 用户未登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"fail","msg":"取消收藏成功"}', content_type='application/json')
        else:
            # 用户未收藏，收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')
