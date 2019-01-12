from django.core.mail import send_mail
from django.conf import settings

email_title = 'Pyhton SMTP 邮件服务测试'
email_body = '飞个教程独家测试'
email = '1271570224@qq.com'  #对方的邮箱
send_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, [email])

if send_status:
    print('发送成功')

"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1271570224@qq.com"  # 用户名
mail_pass = "euvtrglugggubagj"  # 口令

sender = '1271570224@qq.com'
receivers = ['1271570224@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("飞哥教程", 'utf-8')
message['To'] = Header("测试", 'utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(str(e))
"""