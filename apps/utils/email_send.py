# coding:utf-8
from random import Random

from django.core.mail import send_mail

from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


# 生成验证码函数
def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送验证邮件
def send_register_email(email, send_type='register'):
    # 生成随机的验证码，并保存到数据库
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活您的账号：http://localhost:9000/active/{0}'.format(code)

        # 发送状态，成功为 1，失败为 0
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('发送验证码邮件成功')
    elif send_type == 'forget':
        email_title = '慕学在线网密码重置链接'
        email_body = '请点击下面的链接激活您的账号：http://localhost:9000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('发送验证码邮件成功')
