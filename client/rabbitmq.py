import pika
import json
import logging
from pika.adapters import tornado_connection


class PikaClient:
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.event_listeners = set()

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        cred = pika.PlainCredentials('root', '123')
        param = pika.ConnectionParameters(host="127.0.0.1", credentials=cred)
        self.connection = tornado_connection.TornadoConnection(param, custom_ioloop = self.io_loop, on_open_callback = self.on_connected)
        self.connection.add_on_open_error_callback(self.error)
        self.connection.add_on_close_callback(self.on_closed)

    def error(self, conn):
        logging.error('socket error', conn)
        pass

    def on_connected(self, conn):
        logging.error('hehe, connected')
        self.connected = True
        self.connection = conn
        self.connection.channel(channel_number = 1, on_open_callback = self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel

    def on_closed(self, conn, c):
        logging.error('pika close!')
        self.io_loop.stop()


class ConnPikaClient(object):
    def __init__(self):
        self.queue_name = "queue-%s" % (id(self),)

        # Default values
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.io_loop = None
        self.exchange = None

        # Webscoket object.
        self.websocket = None

    def setup_exchange(self):
        self.channel.exchange_declare(
            callback=self.on_exchange_declared,
            exchange=self.exchange,
            exchange_type='fanout',
        )

    def on_exchange_declared(self, unused_frame):
        logging.error('PikaClient: Exchange Declared, Declaring Queue')
        self.channel.queue_declare(auto_delete=True,
                                   queue=self.queue_name,
                                   durable=False,
                                   exclusive=True,
                                   callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        logging.error('PikaClient: Queue Declared, Binding Queue')
        self.channel.queue_bind(exchange=self.exchange,
                                queue=self.queue_name,
                                routing_key='',
                                callback=self.on_queue_bound)

    def on_queue_bound(self, frame):
        logging.error('PikaClient: Queue Bound, Issuing Basic Consume')
        self.ctag = self.channel.basic_consume(on_message_callback=self.on_pika_message,
                                               queue=self.queue_name)

    def on_pika_message(self, channel, method, header, body):
        logging.error('PikaCient: Message receive, delivery tag #%i' % \
                      method.delivery_tag)
        self.websocket.write_message(body)

    def on_basic_cancel(self):
        logging.error('PikaClient: Basic Cancel Ok')
        self.channel.queue_delete(queue=self.queue_name)

    def on_closed(self, connection):
        self.io_loop.stop()

    def sample_message(self, exchange, message):
        properties = pika.BasicProperties(content_type="text/plain", delivery_mode=1)
        self.channel.basic_publish(exchange=exchange,
                                   routing_key='',
                                   body=message,
                                   properties=properties)



