# -*- coding: UTF-8 -*-
from urllib import request
import json


def send_message(user, message):
    # get token, do not change
    url_gettoken = "https://a1.easemob.com/ziyuanliu/pkucarrier/token"
    header = {"Content-Type":"application/json"}
    body = '{"grant_type": "client_credentials","client_id": "YXA6OlYUgJjEEeWXOb1RowOi2A","client_secret": "YXA6Nsfj21Zw60aTAwDd8PWvCnn5obI"}'
    body = body.encode()
    req = request.Request(url_gettoken, body, header)
    resp = request.urlopen(req)
    html = resp.read().decode()
    s = json.loads(html)
    token = s['access_token']

    # send message
    url = "https://a1.easemob.com/ziyuanliu/pkucarrier/messages"
    # need to change:
    # message: params[msg][msg] field
    # target user: params[target], must be a dict
    params = '{"target_type" : "users", "target" : ["%s"], "msg" : {"type" : "txt", "msg" : "%s"}}' % (user, message)
    header = {"Content-Type":"application/json", "Authorization":"Bearer %s" % (token)}
    params = params.encode()
    req = request.Request(url, params, header)
    resp = request.urlopen(req)
    html = resp.read().decode()

    return html
    # print(html)