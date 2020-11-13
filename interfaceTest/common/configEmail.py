# 两种方式，第一种是用的win32com,因为系统等各方面原因，反馈win32问题较多，建议改成下面的smtplib方式
import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from interfaceTest.readConfig import ReadConfig


class SendEmail(object):
    # def __init__(self, username, passwd, recv, title, content,
    #              file=None, ssl=False,
    #              email_host='smtp.qq.com', port=25, ssl_port=465):
    def __init__(self, ssl=False):
        self.username = ReadConfig().get_email('username')  # 用户名
        self.passwd = ReadConfig().get_email('passwd')  # 密码
        self.recv = ReadConfig().get_email('recv').split(",")  # 收件人，多个要传list ['a@qq.com','b@qq.com]
        self.title = ReadConfig().get_email('title')  # 邮件标题
        self.content = ReadConfig().get_email('content')  # 邮件正文
        self.file = ReadConfig().get_email('file')  # 附件路径，如果不在当前目录下，要写绝对路径
        self.email_host = 'smtp.qq.com'  # smtp服务器地址
        self.port = 25  # 普通端口
        self.ssl = ssl  # 是否安全链接
        self.ssl_port = 465  # 安全链接端口

    def send_email(self):
        msg = MIMEMultipart()
        # 发送内容的对象
        if self.file:  # 处理附件的
            file_name = os.path.split(self.file)[-1]  # 只取文件名，不取路径
            try:
                f = open(self.file, 'rb').read()
            except Exception as e:
                raise Exception('附件打不开！！！！')
            else:
                att = MIMEText(f, "base64", "utf-8")
                att["Content-Type"] = 'application/octet-stream'
                # base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 这里是处理文件名为中文名的，必须这么写
                att["Content-Disposition"] = 'attachment; filename="%s"' % (new_file_name)
                msg.attach(att)
        msg.attach(MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = ','.join(self.recv)  # 接收者账号列表
        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.email_host, port=self.port)
        # 发送邮件服务器的对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, msg.as_string())
            pass
        except Exception as e:
            print('出错了。。', e)
        else:
            print('发送成功！')
        self.smtp.quit()


if __name__ == '__main__':
    m = SendEmail()
    m.send_email()