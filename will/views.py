from django.shortcuts import render
from django.http import HttpResponse
import json, datetime
from user.models import User
from will.models import Will
# Create your views here.


def new(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong Http method!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    pfrom = request.POST['pfrom']
    pto = request.POST['pto']
    info = request.POST['info']
    uid = request.POST['owner_id']

    owner = User.objects.filter(id = uid)
    if not owner.exists():
        resp['status'] = 2
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif len(owner) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many user found! Impossible'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    owner = owner[0]
    curtime = datetime.datetime.now()
    will = Will(pfrom=pfrom, pto=pto, info=info, owner=owner, build_time=curtime)
    will.save()

    if will.id is None:
        resp['status'] = 4
        resp['message'] = 'Failed to create new will'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    resp['status'] = 0
    resp['message'] = 'Success!'
    info = will.to_dict()
    ownerinfo = owner.to_dict()
    info['owner'] = ownerinfo
    resp['data'] = info
    return HttpResponse(json.dumps(resp), content_type='application/json')


def get_info(request, wid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    will = Will.objects.filter(id=wid)
    if not will.exists():
        resp['status'] = 2
        resp['message'] = 'No such will!'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif len(will) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many will found! Impossible!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    resp['status'] = 0
    resp['message'] = 'Success!!'
    willinfo = will[0].to_dict()
    userinfo = will[0].owner.to_dict()
    willinfo['owner'] = userinfo
    resp['data'] = willinfo
    return HttpResponse(json.dumps(resp), content_type='application/json')


def all(request):
    resp = {}
    if request.method != 'GET':
        resp['staus'] = 1
        resp['message'] = 'Wrong http method'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    wills = Will.objects.all()

    wills_info = []
    for will in wills:
        info = will.to_dict()
        ownerinfo = will.owner.to_dict()
        info['owner'] = ownerinfo
        wills_info.append(info)

    resp['status'] = 0
    resp['message'] = 'Success'
    resp['data'] = wills_info
    return HttpResponse(json.dumps(resp), content_type='application/json')


def delete_will(request):
    resp = {}
    if request.method == 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    uid = request.POST['uid']
    password = request.POST['password']
    wid = request.POST['wid']

    will = Will.objects.get(id=wid)
    user = User.objects.get(id=uid)
    if str(user.id) != str(uid) or str(user.password) != str(password):
        resp['status'] = 2
        resp['message'] = 'No authority'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    resp['status'] = 0
    resp['message'] = 'ok'
    will.delete()
    return HttpResponse(json.dumps(resp), content_type='application/json')
