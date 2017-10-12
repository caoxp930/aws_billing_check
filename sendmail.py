#coding=utf-8
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_mail(sender, pwd, recipient, subject,email_content):
    to_list =[]
    to_list.append(recipient)
    #print to_list
    host_list = sender
    username = sender
    password = pwd
    smtpserver = 'smtp.139.com'
    time.sleep(1)
    msg = MIMEMultipart()

    # print email_content
    msgtext = MIMEText(email_content, "html", "utf-8")
    msg.attach(msgtext)
    # subject = 'testing'
    msg['Subject'] = Header(subject, 'utf-8')  # 头信息添加到根容器
    msg['From'] = sender
    msg['To'] = ",".join(to_list)

    smtp = smtplib.SMTP()  # 建立连接
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(host_list, to_list, msg.as_string())
    smtp.close()
    #print '邮件已发送'

if __name__=='__main__':
    send_mail('wkatios@139.com', ur'wk123456', 'wkatios@139.com', 'AWS Billing', 'test')