from django.shortcuts import render
from django.http import HttpResponse
from task.models import Task
from user.models import User
from deal.models import Deal
from django.db import transaction
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
    if not user.exists():
        resp['status'] = 1
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    elif len(user) > 1:
        resp['status'] = 2
        resp['message'] = 'Too many user found, impossible!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    if user[0].status == 0:
        resp['status'] = 3
        resp['message'] = 'Not authenticated yet!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    task = Task(approximate_fplace = approximate_fplace, detailed_fplace = detailed_fplace,
                pto = pto, code = code, fetch_btime = datetime.datetime.strptime(fetch_btime, '%Y-%m-%d %H:%M:%S'),
                fetch_etime = datetime.datetime.strptime(fetch_etime, '%Y-%m-%d %H:%M:%S'), owner = user[0],
                give_time = datetime.datetime.strptime(give_time, '%Y-%m-%d %H:%M:%S'), build_time = curtime)
    task.save()
    if task.id is None:
        resp['status'] = 4
        resp['message'] = 'create task error'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = 0
        resp['message'] = 'Success'
        info = task.to_dict()
        info['owner'] = task.owner.to_dict()
        resp['data'] = info
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
    info['owner'] = task[0].owner.to_dict()
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
    info['owner'] = task[0].owner.to_dict()
    resp['data'] = info
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@transaction.atomic
def task_resp(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    task_id = request.POST['task_id']
    #owner_id = request.POST['owner_id']
    user_id = request.POST['user_id']
    task = None

    try:
        task = Task.objects.select_for_update().filter(id=task_id)
    except:
        resp['status'] = '7'
        resp['message'] = 'datebase locked!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if not task.exists():
        resp['status'] = 2
        resp['message'] = 'No such task'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif len(task) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many tasks found'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    if task[0].status == 1:
        resp['status'] = 4
        resp['message'] = 'Task is already toke by others'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    user = User.objects.filter(id=user_id)
    if not user.exists():
        resp['status'] = 5
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    if len(user) > 1:
        resp['status'] = 6
        resp['message'] = 'Too many user found, impossible!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    if user[0].status == 0:
        resp['status'] = 7
        resp['message'] = 'Not authenticated yet!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    if task[0].owner.id == user[0].id:
        resp['status'] = 8
        resp['message'] = 'You can\'t response to your own task!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    task[0].status = 1
    task[0].save()
    deal = Deal(task = task[0], needer = task[0].owner, helper=user[0], build_time=datetime.datetime.now())
    deal.save()
    if deal.id is None:
        resp['status'] = 7
        resp['message'] = 'Failed to create new deal'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    dealinfo = deal.to_dict()
    neederinfo = deal.needer.to_dict()
    helperinfo = deal.helper.to_dict()
    dealinfo['needer'] = neederinfo
    dealinfo['helper'] = helperinfo
    dealinfo['task'] = task[0].id
    resp['status'] = 0
    resp['message'] = 'Success'
    resp['data'] = dealinfo
    return HttpResponse(json.dumps(resp), content_type='application/json')


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
    taskinfo = []
    for task in tasks:
        tmp = task.ap_to_dict()
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
        userinfo = task.owner.to_dict()
        info['owner'] = userinfo
        tasks_info.append(info)
    resp['status'] = 0
    resp['message'] = 'Success'
    resp['data'] = tasks_info
    return HttpResponse(json.dumps(resp), content_type='application/json')

def delete_task(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method'
        return HttpResponse(json.dumps(json), content_type='application/json')

    uid = request.POST['uid']
    password = request.POST['password']
    tid = request.POST['tid']

    task = Task.objects.get(id=tid)
    if task.owner.id != uid or task.owner.password != password:
        resp['status'] = 2
        resp['message'] = 'No authority'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    if task.status == 1:    # already accepted
        resp['status'] = 3
        resp['message'] = 'Already accepted, cannot delete'
    task.delete()
    resp['status'] = 0
    resp['message'] = 'ok'
    return HttpResponse(json.dumps(resp), content_type='application/json')
