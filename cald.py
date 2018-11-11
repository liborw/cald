#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json


class CaldApi(object):

    def __init__(self, baseurl='http://cald.yosarin.net'):
        self.baseurl = baseurl
        self.token = None

    def headers(self):
        if self.token is not None:
            headers = {'token': self.token}
        else:
            headers = {}
        return headers

    def _post(self, addr, data={}):
        url = self.baseurl + addr
        data.update(self.headers())
        req = requests.post(url, data=data)
        content = json.loads(req.text)
        return content

    def _get(self, addr, data={}):
        url = self.baseurl + addr
        data.update(self.headers())
        req = requests.get(url, data=data)
        content = json.loads(req.text)
        return content

    def authorize(self, user, password):
        ret = self._post('/user/login', {'login': user, 'password': password})

        if 'error' in ret:
            return (False, ret)
        else:
            self.token = ret['token']['token']
            return (True, ret)

    def user_me(self):
        ret = self._get('/user/me')
        return ret


##

baseurl = 'http://cald.yosarin.net'

def get(url):
    url = 'http://evidence.cald.cz/api/' + url
    headers = {'X-Auth-Token': "9855f563851b600756496b976a14d60a2e99aceec5653c920526d1e10e34bc47"}
    req = requests.get(url, headers=headers)
    req = requests.get(url, headers=headers)
    content = json.loads(req.text)
    return content


def create_user(user, password, email):
    url = baseurl + '/user'
    data = {'email': email, 'password': password, 'login': user}
    req = requests.post(url, data=data)
    content = json.loads(req.text)
    return content


def get_auth_token(user, password):
    url = baseurl + '/user/login'
    data = {'login': user, 'password': password}
    req = requests.post(url, data=data)
    content = json.loads(req.text)
    return content['token']['token']

## authentication

user = 'agentSunset'
password = 'sunset2018'

# create_user(user, password, 'test@test.cz')

resp = {'id': '67', 'info': 'User created', 'mail_send': True, 'status': 'OK'}


resp = get_auth_token(user, password)

##

cald = CaldApi(baseurl)
cald.authorize(user, password)
cald.user_me()




