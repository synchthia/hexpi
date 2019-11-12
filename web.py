#!/usr/bin/env python3

import json
import logging
import tornado.ioloop
import tornado.web
from util import ir, aeha

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(
            status_code=404,
            reason="Not Found"
        )

    def write_error(self, status_code, exc_info=None, **kwargs):
        self.finish({"error": self._reason})

class IRHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            req = tornado.escape.json_decode(self.request.body)
            signal = req['code']
            ir.send(3, signal)

            self.write({})
        except json.decoder.JSONDecodeError as ex:
            raise tornado.web.HTTPError(
                status_code=400,
                reason="Failed decode json"
            )

    def write_error(self, status_code, exc_info=None, **kwargs):
        self.finish({"error": self._reason})

def start(port: int):
    web = tornado.web.Application([
        (r"/api/v1/ir", IRHandler),
    ], default_handler_class=DefaultHandler)

    web.listen(port)
    logging.info("HTTP Server started on %d", port)

    tornado.ioloop.IOLoop.current().start()
