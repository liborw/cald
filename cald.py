#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import pprint
import logging


class CaldApi(object):

    def __init__(self, baseurl='http://cald.yosarin.net'):
        self.baseurl = baseurl
        self.token = None
        self.log = logging.getLogger('CaldApi')

    def headers(self):
        if self.token is not None:
            headers = {'token': self.token}
        else:
            headers = {}
        return headers

    def _post(self, addr, data={}):
        url = self.baseurl + addr
        data.update(self.headers())
        req = requests.post(url, json=data)
        try:
            content = json.loads(req.text)
        except json.JSONDecodeError:
            self.log.warn()
            return {'error': 'unable to parse json', 'text': req.text}
        return content

    def _get(self, addr, data={}):
        url = self.baseurl + addr
        data.update(self.headers())
        req = requests.get(url, json=data)
        try:
            content = json.loads(req.text)
        except json.JSONDecodeError:
            self.log.warn()
            return {'error': 'unable to parse json', 'text': req.text}
        return content

    def authorize(self, user, password):
        ret = self._post('/user/login', {'login': user, 'password': password})

        if 'error' in ret:
            return (False, ret)
        else:
            self.token = ret['token']['token']
            return (True, ret['token'])

    def user_me(self):
        ret = self._get('/user/me')
        return ret

    def list(self, what, where=None, extend=None, limit=None, offset=None):

        data = dict()
        if where is not None:
            data['filter'] = where
        if extend is not None:
            data['extend'] = extend
        if limit is not None:
            data['limit'] = limit
        if offset is not None:
            data['offset'] = offset

        ret = self._get('/list/' + what, data=data)

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret['data'])

    def new_player(self, player):
        self.log.debug('update_player: %s %s',
                       player['first_name'],
                       player['last_name'])

        player = dict(player)

        if 'address' in player:
            del player['address']

        # new player
        ret = self._post('/player', data=player)
        self.log.debug('Resp: %s', str(ret))

        if 'error' in ret:
            return (False, ret)

        pid = int(ret['id'])
        return (True, pid)

    def add_team_player(self, teamid, playerid, season):
        self.log.debug('add_team_player teamid: %d, playerid: %d, seasonid: %d',
                       teamid,
                       playerid,
                       season)

        data = {'season_id': season}
        ret = self._post('/team/' + str(teamid) + '/player/' + str(playerid), data)
        self.log.debug('Resp: %s', str(ret))

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret)

    def update_player(self, player, pid):
        self.log.debug('update_player: %s %s pid: %d',
                       player['first_name'],
                       player['last_name'],
                       pid)

        player = dict(player)

        if 'address' in player:
            del player['address']

        # update player
        ret = self._post('/player/' + str(pid), data=player)
        self.log.debug('Resp: %s', str(ret))

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret['data'])

    def update_team(self, team, teamid):
        ret = self._post('/team/' + str(teamid))

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret['data'])

    def get_player_address(self, pid):
        ret = self._get('/player/' + str(pid) + '/address')

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret['data'])

    def get_season_id(self, year):
        ret, data = self.list('season', where={'name': '2018'})
        if ret and data:
            return int(data[0]['id'])
        else:
            return None

    def add_player_address(self, address, pid):

        if 'type' not in address:
            self.log.warning('No address type, set deault')
            address['type'] = 'permanent residence'

        uri = '/player/{}/address'.format(pid)
        ret = self._post(uri, data=address)

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret)

    def update_player_address(self, address, pid, aid):
        uri = '/player/{}/address/{}'.format(pid, aid)
        ret = self._post(uri, data=address)

        if 'error' in ret:
            return (False, ret)
        else:
            return (True, ret)

    def get_player_address_id(self, pid):
        ret, data = self.get_player_address(pid)

        if ret and data:
            return data[0]['id']
        else:
            return []

    def get_team_players(self, teamid):
        return self.list('player_at_team', where={'team_id': teamid})

    def get_player(self, **kvargs):
        return self.list('player', where=kvargs)

    def get_team(self, **kvargs):
        return self.list('team', where=kvargs)

    def is_player_in_team(self, playerid, teamid, seasonid):
        self.log.debug('is_player_in_team: pid: %d, tid: %d sid: %d',
                playerid, teamid, seasonid)
        query = {'player_id': playerid, 'team_id': teamid, 'season_id': seasonid}
        ret, data = self.list('player_at_team', where=query)

        return len(data) > 0


