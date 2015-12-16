from django.shortcuts import render
from django.http import HttpResponse
from task.models import Task
from user.models import User

import json
import datetime
# Create your views here.
def new(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    approximate_fplace = request.POST['approximate_fplace']
    detailed_fplace = request.POST['detailed_fplace']
    pto = request.POST['pto']
    code = request.POST['code']
    fetch_btime = request.POST['fetch_btime']
    fetch_etime = request.POST['fetch_etime']
    owner = request.POST['owner']
    give_time = request.POST['give_time']
    curtime = datetime.datetime.now()
    user = User.objects.filter(id = owner)
    if user.exists() and len(user) == 1:
        task = Task(approximate_fplace = approximate_fplace, detailed_fplace = detailed_fplace,
                    pto = pto, code = code, fetch_btime = datetime.datetime.strptime(fetch_btime, '%Y-%m-%d %H:%M:%S'),
                    fetch_etime = datetime.datetime.strptime(fetch_etime, '%Y-%m-%d %H:%M:%S'), owner = user[0],
                    give_time = datetime.datetime.strptime(give_time, '%Y-%m-%d %H:%M:%S'),
                    build_time = curtime)
        task.save()
        if task.id != None:
            resp['status'] = 0
            resp['message'] = 'Success'
            info = task.to_dict()
            info['fetch_btime'] = task.fetch_btime.strftime('%Y-%m-%d %H:%M:%S')
            info['fetch_etime'] = task.fetch_etime.strftime('%Y-%m-%d %H:%M:%S')
            info['give_time'] = task.give_time.strftime('%Y-%m-%d %H:%M:%S')
            info['build_time'] = task.build_time.strftime('%Y-%m-%d %H:%M:%S')
            info['owner'] = task.owner.to_dict()
            info['owner']['signup_time'] = task.owner.signup_time.strftime('%Y-%m-%d %H:%M:%S')
            resp['data'] = info
            return HttpResponse(json.dumps(resp), content_type = 'application/json')
        else:
            resp['status'] = 1
            resp['message'] = 'Build error'
            return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = '2'
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

def get_ap_info(request, tid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    task = Task.objects.filter(id = tid)
    if not task.exists():
        resp['status'] = 2
        resp['message'] = 'No such task!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(task) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many tasks found! Impossible!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    resp['status'] = 0
    resp['message'] = 'Success'
    info = task[0].ap_to_dict()
    info['fetch_btime'] = task[0].fetch_btime.strftime('%Y-%m-%d %H:%M:%S')
    info['fetch_etime'] = task[0].fetch_etime.strftime('%Y-%m-%d %H:%M:%S')
    info['give_time'] = task[0].give_time.strftime('%Y-%m-%d %H:%M:%S')
    info['build_time'] = task[0].build_time.strftime('%Y-%m-%d %H:%M:%S')
    info['owner'] = task[0].owner.to_dict()
    info['owner']['signup_time'] = task[0].owner.signup_time.strftime('%Y-%m-%d %H:%M:%S')
    resp['data'] = info
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def get_info(request, tid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    task = Task.objects.filter(id = tid)
    if not task.exists():
        resp['status'] = 2
        resp['message'] = 'No such task!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(task) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many tasks found! Impossible!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    resp['status'] = 0
    resp['message'] = 'Success'
    info = task[0].to_dict()
    info['fetch_btime'] = task[0].fetch_btime.strftime('%Y-%m-%d %H:%M:%S')
    info['fetch_etime'] = task[0].fetch_etime.strftime('%Y-%m-%d %H:%M:%S')
    info['give_time'] = task[0].give_time.strftime('%Y-%m-%d %H:%M:%S')
    info['build_time'] = task[0].build_time.strftime('%Y-%m-%d %H:%M:%S')
    info['owner'] = task[0].owner.to_dict()
    info['owner']['signup_time'] = task[0].owner.signup_time.strftime('%Y-%m-%d %H:%M:%S')
    resp['data'] = info
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def task_resp(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = '1'
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')


def get_user_tasks(request, uid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong Http method whill get user tasks'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    user = User.objects.filter(id = uid)
    if not user.exists():
        resp['status'] = 2
        resp['message'] = 'No user found!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(user) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many users found, Impossible!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    tasks = Task.objects.filter(owner = user[0])
    userinfo = user[0].to_dict()
    userinfo['signup_time'] = user[0].signup_time.strftime('%Y-%m-%d %H:%M:%S')
    taskinfo = []
    for task in tasks:
        tmp = task.ap_to_dict()
        tmp['fetch_btime'] = task.fetch_btime.strftime('%Y-%m-%d %H:%M:%S')
        tmp['fetch_etime'] = task.fetch_etime.strftime('%Y-%m-%d %H:%M:%S')
        tmp['give_time'] = task.give_time.strftime('%Y-%m-%d %H:%M:%S')
        tmp['build_time'] = task.build_time.strftime('%Y-%m-%d %H:%M:%S')
        tmp['owner'] = userinfo
        taskinfo.append(tmp)
    resp['status'] = 0
    resp['message'] = 'Success!!'
    resp['data'] = taskinfo
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def all(request):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(json), content_type='application/json')

    tasks = Task.objects.all()
    tasks_info = []
    for task in tasks:
        info = task.ap_to_dict()
        info['fetch_btime'] = task.fetch_btime.strftime('%Y-%m-%d %H:%M:%S')
        info['fetch_etime'] = task.fetch_etime.strftime('%Y-%m-%d %H:%M:%S')
        info['build_time'] = task.build_time.strftime('%Y-%m-%d %H:%M:%S')
        info['give_time'] = task.give_time.strftime('%Y-%m-%d %H:%M:%S')
        userinfo = task.owner.to_dict()
        userinfo['signup_time'] = task.owner.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        info['owner'] = userinfo
        tasks_info.append(info)
    resp['status'] = 0
    resp['message'] = 'Success'
    resp['data'] = tasks_info
    return HttpResponse(json.dumps(resp), content_type='application/json')