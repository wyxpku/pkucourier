from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import json
from datetime import *
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
from urllib.error import URLError
from .sendEmail import *
import base64
from .easemobSendMessage import *
# Create your views here.


def signup(request):
    if request.method != 'POST':
        return HttpResponse('Access Denied!')

    resp = {}
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    avatar = request.POST['avatar']
    if User.objects.filter(email = email).exists():
        resp['status'] = 1;
        resp['message'] = 'The email account has been used!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    cur_time = datetime.now()

    # 创建环信用户
    index_at = email.index('@')
    helo = email[0:index_at]
    hx_username = "pkucourier_" + helo
    hx_password = password
    # 向用户发送验证邮件
    if certify(email) is False:
        return HttpResponse('The email is wrong!')
    if signupHX(hx_username, hx_password) is False:
        return HttpResponse('Huanxin register failed!')
    u1 = User(name = username, email = email, password = password, signup_time = cur_time,
              hx_username = hx_username, hx_password = hx_password, avatar=avatar)
    u1.save()
    if u1.id is None:
        resp['status'] = 1
        resp['message'] = 'Failed!'
        HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = 0
        resp['message'] = 'Success!'
        resp['data'] = u1.to_dict()
        return HttpResponse(json.dumps(resp), content_type = 'application/json')


def login(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email = email)
    if not user.exists():
        resp['status'] = 1
        resp['message'] = 'User don\'t exits'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(user) > 1:
        resp['status'] = 2
        resp['message'] = 'More than one user found! impossible'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    if user[0].password == password:
        resp['status'] = 0
        resp['message'] = 'Success'
        resp['data'] = user[0].to_dict()
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = 3
        resp['message'] = 'Wrong password!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')


def getall(request):
    resp = {}
    users = User.objects.all()
    usersinfo = []
    for usertmp in users:
        usersinfo.append(usertmp.to_dict())
    resp['data'] = usersinfo
    return HttpResponse(json.dumps(resp), content_type='application/json')


def user_info(request, uid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = '1'
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    tmpuser = User.objects.filter(id = uid)
    if not tmpuser.exists():
        resp['status'] = '1'
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(tmpuser) > 1:
        resp['status'] = '1'
        resp['message'] = 'Too many user found, Impossilble!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = '0'
        resp['message'] = 'Success!'
        resp['data'] = tmpuser[0].to_dict()
        return HttpResponse(json.dumps(resp), content_type = 'application/json')


# 用户验证的入口
def verify(request):
    resp = {}
    if request.method != 'GET':
        resp['status'] = '1'
        resp['message'] = 'Wrong method'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    # 暂时先只用邮箱加密，后面可以再做修改
    code = request.GET['coding']
    code = code.encode()
    code = base64.urlsafe_b64decode(code).decode()
    tmp = User.objects.get(email = code)
    if not tmp:
        resp['status'] = '1'
        resp['message'] = 'No such user!'
    tmp.status = 1
    tmp.save()
    resp['status'] = 0
    resp['message'] = 'Success'
    return HttpResponse(json.dumps(resp), content_type='application/json')


# 系统发送消息
def send_message_admin(request):
    resp = {}
    if request.method != 'GET':
        resp['status'] = '1'
        resp['message'] = 'Wrong method'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    user = request.GET['user']
    needer_id = request.GET['needer_id']

    needer = User.objects.get(id=needer_id)
    if needer is None:
        resp['status'] = 2
        resp['message'] = 'The needer does not exist'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    message = "PKU-Courier小秘书提醒您：%s(id: %s) 想让您帮TA取快递" % (needer.name, needer_id)
    html = send_message(user, message)
    tmp = json.loads(html)
    try:
        if tmp['data'][user] == 'success':
            resp['status'] = 0
            resp['message'] = 'ok'
            resp['admin_name'] = 'PKU-Courier小秘书'
            resp['avatar'] = 0
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            resp['status'] = 2
            resp['message'] = 'Message sent failed'
            return HttpResponse(json.dumps(resp), content_type='application/json')
    except:
        resp['status'] = 2
        resp['message'] = 'Message sent failed'
        return HttpResponse(json.dumps(resp), content_type='application/json')

# 注册环信
def signupHX(username, password):
    url_gettoken = "https://a1.easemob.com/ziyuanliu/pkucarrier/token"
    header = {"Content-Type": "application/json"}
    body = '{"grant_type": "client_credentials", "client_id": "YXA6OlYUgJjEEeWXOb1RowOi2A", \
                "client_secret": "YXA6Nsfj21Zw60aTAwDd8PWvCnn5obI"}'
    body = body.encode("UTF-8")
    req = urllib.request.Request(url_gettoken, body, header)
    hxresp = urllib.request.urlopen(req)
    html = hxresp.read().decode("UTF-8")
    s = json.loads(html)
    token = s['access_token']
    url = "https://a1.easemob.com/ziyuanliu/pkucarrier/users"
    params = '{"username" : "%s", "password" : "%s", "nickname" : ""}' % (username, password)
    params = params.encode("UTF-8")
    header = {"Content-Type":"application/json", "Authorization":"Bearer %s" % (token)}
    req = urllib.request.Request(url, params, header)
    try:
        hxresp = urllib.request.urlopen(req)
        html = hxresp.read().decode()
    except URLError as e:
        print(e.reason)
        return False
    return True


# 向用户发送包含特定链接的邮件，验证用户的身份
# coding参数
def certify(email):
    to_list = [email]
    code = email.encode()
    code = base64.urlsafe_b64encode(code)
    code = code.decode()
    # this url should be changed
    url = 'http://wyxpku.com/user/verify/?coding=' + code
    if send_mail(to_list, url):
        return True
    else:
        return False
