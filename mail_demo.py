import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 设置服务器
mail_host = "smtp.qq.com"
# 用户名
mail_user = "631582864@qq.com"
# 邮箱密码
mail_pass = "zdugzwmxjbgvbcij"
# 发送邮箱
sender = '631582864@qq.com'
# 接收邮箱
receivers = ['a631582864@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Hello Python', 'plain', 'utf-8')
message['From'] = Header("SMZDMSpider", 'utf-8')
message['To'] = Header("my lorder", 'utf-8')
subject = 'SMZDM信息提醒'
message['Subject'] = Header(subject, 'utf-8')
try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.set_debuglevel(1)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
