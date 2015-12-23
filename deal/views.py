from django.shortcuts import render
from django.http import HttpResponse
from .models import Deal
from user.models import User
from django.db import transaction
import json
# Create your views here.


def get_info(request, did):
    resp = {}
    if request.method != 'GET':
        resp['status'] = '1'
        resp['message'] = 'Wrong http method'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    deal = Deal.objects.filter(id=did)
    if not deal.exists():
        resp['status'] = '2'
        resp['message'] = 'No such deal'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif len(deal) > 1:
        resp['status'] = '3'
        resp['message'] = 'Too many deal found! Impossible!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    dealinfo = deal[0].to_dict()
    helperinfo = deal[0].helper.to_dict()
    neederinfo = deal[0].needer.to_dict()
    dealinfo['needer'] = neederinfo
    dealinfo['helper'] = helperinfo
    resp['status'] = 0
    resp['message'] = 'Success!'
    resp['data'] = dealinfo
    return HttpResponse(json.dumps(resp), content_type='application/json')


## 返回User参与的所有deal，包括作为Helper的deal => helper_deal，以及作为needer的Deal => needer_deal
def get_user_deals(request, uid):
    resp = {}
    if request.method != 'GET':
        resp['status'] = 1
        resp['message'] = 'Wrong http method!'
        return HttpResponse(json.dums(resp), content_type='application/json')
    user = User.objects.filter(id=uid)
    if not user.exists():
        resp['status'] = 2
        resp['message'] = 'No such user'
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif len(user) > 1:
        resp['status'] = 3
        resp['message'] = 'Too many user found, Impossible!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    helper_deals = Deal.objects.filter(helper=user)
    needer_deals = Deal.objects.filter(needer=user)

    helper_deals_info = []
    needer_deals_info = []
    for helper_deal in helper_deals:
        tmpinfo = helper_deal.to_dict()
        tmpinfo['helper'] = helper_deal.helper.to_dict()
        tmpinfo['needer'] = helper_deal.needer.to_dict()
        helper_deals_info.append(tmpinfo)
    for needer_deal in needer_deals:
        tmpinfo = needer_deal.to_dict()
        tmpinfo['helper'] = needer_deal.helper.to_dict()
        tmpinfo['needer'] = needer_deal.needer.to_dict()
        needer_deals_info.append(tmpinfo)

    resp['status'] = 0
    resp['message'] = 'Success!'
    resp['data']['needer_deal'] = needer_deals_info
    resp['data']['helper_deal'] = helper_deals_info
    return HttpResponse(json.dumps(resp), content_type='application/json')


@transaction.atomic
def complete(request):
    resp = {}
    if request.method != 'POST':
        resp['status'] = 1
        resp['message'] = 'Wrong http method'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    deal_id = request.POST['deal_id']
    email = request.POST['email']
    password = request.POST['password']
    try:
        deal = Deal.objects.select_for_update().filter(id=deal_id)
    except:
        resp['status'] = '4'
        resp['message'] = 'datebase locked!'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    if not deal.exists():
        resp['status'] = 2
        resp['message'] = 'No such deal'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')

    user = deal[0].task.owner
    if user.email == email and user.password == password:
        deal[0].status = 1
        deal[0].save()
        helper = deal[0].helper
        helper.bonus += 1
        helper.save()
        resp['status'] = 0
        resp['message'] = 'Success'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
    else:
        resp['status'] = 3
        resp['message'] = 'No right or wrong password'
        return HttpResponse(json.dumps(resp), content_type = 'application/json')
