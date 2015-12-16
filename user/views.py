from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import json
from datetime import *
from django.core.exceptions import ObjectDoesNotExist
import urllib.request
# Create your views here.

def signup(request):
    if request.method != 'POST':
        return HttpResponse('Access Denied!')

    resp = {}
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    if len(User.objects.filter(email = email)) > 0:
        resp['status'] = 1;
        resp['message'] = 'The email account has been used!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    cur_time = datetime.now()

    # 创建环信用户
    hx_username = "pkucourier_" + email
    hx_password = password
    #signupHX(hx_username, hx_password)
    u1 = User(name = username, email = email, password = password, signup_time = cur_time,
              hx_username = hx_username, hx_password = hx_password)
    u1.save()
    if u1.id != None:
        resp['status'] = 0
        resp['message'] = 'Success!'
        mydict = u1.to_dict()
        mydict['signup_time'] = u1.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        resp['data'] = json.dumps(mydict)
    else:
        resp['status'] = 1
        resp['message'] = 'Failed!'
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
        info = user[0].to_dict()
        info['signup_time'] = user[0].signup_time.strftime('%Y-%m-%d %H:%M:%S')
        resp['data'] = json.dumps(info)
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = 3
        resp['message'] = 'Wrong password!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

def all(request):
    users = User.objects.all()
    return HttpResponse(len(users))

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
        info = tmpuser[0].to_dict()
        info['signup_time'] = tmpuser[0].signup_time.strftime('%Y-%m-%d %H:%M:%S')
        resp['data'] = json.dumps(info)
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

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
    hxresp = urllib.request.urlopen(req)
    html = hxresp.read()