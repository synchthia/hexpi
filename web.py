#!/usr/bin/env python3

import json
import logging
import tornado.ioloop
import tornado.web
from util import ir, aeha
from sensors import swbme

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(
            status_code=404,
            reason="Not Found"
        )

    def write_error(self, status_code, exc_info=None, **kwargs):
        self.finish({"error": self._reason})

class IRHandler(tornado.web.RequestHandler):
    def initialize(self, gpio):
        self.gpio = gpio

    def post(self):
        try:
            req = tornado.escape.json_decode(self.request.body)
            signal = req['code']
            ir.send(self.gpio, signal)

            self.write({})
        except json.decoder.JSONDecodeError as ex:
            raise tornado.web.HTTPError(
                status_code=400,
                reason="Failed decode json"
            )

    def write_error(self, status_code, exc_info=None, **kwargs):
        self.finish({"error": self._reason})

class SensorHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        r = swbme.readData()
        self.write(r)

    def write_error(self, status_code, exc_info=None, **kwargs):
        self.finish({"error": self._reason})

def start(port: int, gpio: int):
    web = tornado.web.Application([
        (r"/api/v1/ir", IRHandler, dict(gpio=gpio)),
        (r"/api/v1/sensors", SensorHandler),
    ], default_handler_class=DefaultHandler)

    web.listen(port)
    logging.info("HTTP Server started on %d", int(port))

    tornado.ioloop.IOLoop.current().start()
