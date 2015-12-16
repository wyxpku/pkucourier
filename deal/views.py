from django.shortcuts import render
from django.http import HttpResponse
from .models import Deal
from user.models import User
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
    dealinfo['build_time'] = deal[0].build_time.strftime('%Y-%m-%d %H:%M:%S')
    helperinfo = deal[0].helper.to_dict()
    neederinfo = deal[0].needer.to_dict()
    helperinfo['signup_time'] = deal[0].helper.signup_time.strftime('%Y-%m-%d %H:%M:%S')
    neederinfo['signup_time'] = deal[0].needer.signup_time.strftime('%Y-%m-%d %H:%M:%S')
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
        tmpinfo['build_time'] = helper_deal.build_time.strftime('%Y-%m-%d %H:%M:%S')
        tmpinfo['helper'] = helper_deal.helper.to_dict()
        tmpinfo['helper']['signup_time'] = helper_deal.helper.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        tmpinfo['needer'] = helper_deal.needer.to_dict()
        tmpinfo['needer']['signup_time'] = helper_deal.needer.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        helper_deals_info.append(tmpinfo)
    for needer_deal in needer_deals:
        tmpinfo = needer_deal.to_dict()
        tmpinfo['build_time'] = needer_deal.build_time.strftime('%Y-%m-%d %H:%M:%S')
        tmpinfo['helper'] = needer_deal.helper.to_dict()
        tmpinfo['helper']['signup_time'] = needer_deal.helper.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        tmpinfo['needer'] = needer_deal.needer.to_dict()
        tmpinfo['needer']['signup_time'] = needer_deal.needer.signup_time.strftime('%Y-%m-%d %H:%M:%S')
        needer_deals_info.append(tmpinfo)

    resp['status'] = 0
    resp['message'] = 'Success!'
    resp['data']['needer_deal'] = needer_deals_info
    resp['data']['helper_deal'] = helper_deals_info
    return HttpResponse(json.dumps(resp), content_type='application/json')