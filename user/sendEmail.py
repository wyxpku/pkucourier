# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.163.com'
mail_user = 'iostream3'
mail_pass = 'password'
mail_postfix = '163.com'


def send_mail(to_list, url):
    content = '哈喽，我是萌萌哒管理员，请点击下面的链接激活您的账户，如果不激活账户，则不能发布意愿或抢单，也不能获得积分，请尽快激活，谢谢^ ^！<br/>'
    link = '<a href="%s">%s</a>' % (url, url)
    content += link
    me = '<' + mail_user + '@' + mail_postfix + '>'
    msg = MIMEText(content, _subtype = 'html', _charset = 'utf-8')
    msg['Subject'] = '【用户身份验证】PKU-Courier'
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    ############### change your mailto list here ###################
    mail_to_list = ['1200012802@pku.edu.cn']

    # this link should be changed to the api url
    url = '<a href="http://its.pku.edu.cn">http://its.pku.edu.cn</a>'
    if send_mail(mail_to_list, url):
        print('Email succeeded!')
    else:
        print('Email failed!')
