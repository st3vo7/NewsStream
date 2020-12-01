import os.path
import json
import pprint
import asyncio
from typing import Optional, Awaitable

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.httpclient

import motor.motor_tornado

from tornado.options import define, options

from user_handlers import *
from news_handlers import *


define("port", default=8000, help="run on the given port", type=int)


if __name__ == '__main__':
    tornado.options.parse_command_line()

    client = motor.motor_tornado.MotorClient('localhost', 27017)
    db = client.test
    collection = db.test

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "s8iJWyTeSQ+Hfgj59nTy4bFKahPdAEnbhsH5CRuUN1g=",
        "login_url": "/login",
        "db": db,
        "debug": True,
        "xsrf_cookies": True

    }

    app = tornado.web.Application(
        handlers=[(r'/', MainHandler),
                  (r'/sources', SourceHandler),
                  (r'/login', LoginHandler),
                  (r'/signin', SigninHandler),
                  (r'/profile', ProfileHandler),
                  (r'/favicon.ico', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                  ],
        **settings

    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Server has shut down.')
