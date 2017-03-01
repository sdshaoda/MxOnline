# MxOnline

This is a online study Website. Project is base on python Web Django framwork.

[Django](https://www.djangoproject.com/) makes it easier to build better Web apps more quickly and with less code.

## illustration

- MxOnline：项目目录
- apps：存放项目应用
- extra_apps：存放项目的扩展应用，如xadmin
- static：静态文件目录
- templates：HTML模板文件目录
- media：存放上传的资源文件

## How to run?

确保 `MySQL` 服务已启动，并且环境中安装了 `MySQL-python` 驱动

在`MxOnline/settings.py`里可以修改`DATABASES`的配置，默认数据库名为`mxonline`，用户名`root`，密码为空

生成数据表，启动

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver [port]`

Server run at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## modules

`pip list`

```
appdirs (1.4.0)
Django (1.9)
django-crispy-forms (1.6.1)
django-formtools (2.0)
django-pure-pagination (0.3.0)
django-simple-captcha (0.4.6)
httplib2 (0.9.2)
MySQL-python (1.2.5)
olefile (0.44)
packaging (16.8)
Pillow (4.0.0)
pip (9.0.1)
pyparsing (2.1.10)
setuptools (34.2.0)
six (1.10.0)
wheel (0.29.0)
```
