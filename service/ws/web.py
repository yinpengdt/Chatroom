# -*-coding:utf-8-*-
import logging
from client import redis
import asyncio
from service.base import BaseHandler
from tornado.websocket import WebSocketHandler
from client.rabbitmq import ConnPikaClient
from tornado.ioloop import IOLoop
from client import redis
import json

chat_register = {}

class HomeHandler(BaseHandler):
    def get(self):
        roomid = self.get_argument('roomid')
        nickname = self.get_argument('nickname')
        self.render('chat/home.html', roomid=roomid, nickname=nickname)

class NewChatStatus(WebSocketHandler, BaseHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        roomid = str(self.get_argument('roomid'))
        self.pika_client = ConnPikaClient()

        # Share common tornado connections and channel with  RabbitMQ
        self.pika_client.connected = self.application.pc.connected
        self.pika_client.connection = self.application.pc.connection
        self.pika_client.connecting = self.application.pc.connecting
        self.pika_client.io_loop = self.application.pc.io_loop
        self.pika_client.channel = self.application.pc.channel
        self.pika_client.exchange = roomid

        # Assign websocket object to a Pika client object attribute.
        self.pika_client.websocket = self

        # print rabbit_conn.connection,rabbit_conn.connected, rabbit_conn.connecting, rabbit_conn.channel

        IOLoop.current().add_timeout(1000, self.pika_client.setup_exchange)

    def on_message(self, msg):
        'A message on the Webscoket.'

        roomid = str(self.get_argument('roomid'))
        nickname = str(self.get_argument('nickname'))
        message = {
            'from': nickname,
            'message': msg
        }
        self.pika_client.sample_message(roomid, json.dumps(message))

    def on_close(self):
        self.pika_client.on_basic_cancel()
        logging.error("WebSocket closed")

