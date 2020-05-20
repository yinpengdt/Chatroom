#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sentry_sdk
import uuid
import base64
import tornado.web
import os
import sys
import service.ws.web
from sentry_sdk.integrations.tornado import TornadoIntegration
from client.rabbitmq import PikaClient
from tornado import ioloop


STATIC_PATH = os.path.join(sys.path[0], 'static')
from tornado.options import define, options
define('port', default=6111, help='run on this port', type=int)
define('debug', default=True, help='enable debug mode')
options.parse_command_line()

RuleList = [
    (r'/chat/newChatStatus', service.ws.web.NewChatStatus),
    (r'/chat/home', service.ws.web.HomeHandler),

]
settings = {
    'xsrf_cookies': False,
    'compress_response': True,
    'debug': options.debug,
    'template_path': STATIC_PATH,
    'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'vadd_ws').bytes),
}

if __name__ == '__main__':
    if not options.debug:
        sentry_sdk.init(
            dsn="http://40a17c4b832c406d9fbeeec9316941ac:595dc2b4085f4b18aefab5d7045e03e9@ktv.sentry.ktvsky.com/4",
            integrations=[TornadoIntegration()])

    application = tornado.web.Application(RuleList, **settings)
    io_loop = tornado.ioloop.IOLoop.instance()
    application.pc = PikaClient(io_loop)
    application.pc.connect()
    application.listen(options.port)
    print('Running on port %d' % options.port)
    io_loop.start()
