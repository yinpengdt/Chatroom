#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from tornado import web
from tornado.web import HTTPError


class APIError(HTTPError):
    def __init__(self, data):
        super(APIError, self).__init__(status_code=200, reason=json.dumps(data))


class BaseHandler(web.RequestHandler):

    def send_str(self, json_str):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')

        self.set_status(200)
        self.write(json_str)
        self.finish()

    def send_json(self, data={}, errcode=200, errmsg=''):
        res = {
            'errcode': errcode,
            'errmsg': errmsg or '请求成功'
        }
        res.update(data)
        self.send_str(json.dumps(res))

    def write_error(self, status_code, **kwargs):
        err_object = kwargs['exc_info'][1]
        if isinstance(err_object, APIError):  # 自定义异常
            return self.send_str(err_object.reason)
        super(BaseHandler, self).write_error(status_code, **kwargs)

    def get_real_ip(self):
        req_headers = self.request.headers
        real_ip = ''
        try:
            if 'X-Forwarded-For' in req_headers:
                real_ip = req_headers['X-Forwarded-For']
            if not real_ip and 'X-Real-Ip' in req_headers:
                real_ip = req_headers['X-Real-Ip']
            if not real_ip:
                real_ip = self.request.remote_ip
        except:
            real_ip = ''
        if real_ip.count(',') > 0:
            real_ip = re.sub(',.*', '', real_ip).strip()
        return real_ip

    def del_etag_headers(self):
        del self.request.headers['If-None-Match']