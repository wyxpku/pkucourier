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
    print(len(user))
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
            info['fetch_etime'] = str(task.fetch_etime)
            info['give_time'] = str(task.give_time.strftime)
            info['build_time'] = str(task.build_time)
            resp['data'] = json.dumps(info)
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
    info['fetch_btime'] = str(task.fetch_btime)
    info['fetch_etime'] = str(task.fetch_etime)
    info['give_time'] = str(task.give_time.strftime)
    info['build_time'] = str(task.build_time)
    resp['data'] = json.dumps(info)
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
    info['fetch_btime'] = task[0].fetch_btime.strftime('YYYY-MM-DD HH:MM')
    info['fetch_etime'] = str(task.fetch_etime)
    info['give_time'] = str(task.give_time.strftime)
    info['build_time'] = str(task.build_time)
    resp['data'] = json.dumps(info)
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def task_resp(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = '1'
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

