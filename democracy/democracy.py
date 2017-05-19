import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import os.path
import psycopg2
import momoko

define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/statistics/.*", StatisticsHandler),
            (r"/about/.*", AboutHandler),
            (r"/faq/.*", FAQHandler),
            (r"^/.*", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            )
        
        tornado.web.Application.__init__(self, handlers, **settings)


class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("statistics.html")


class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")


class FAQHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("faq.html")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
    ioloop = IOLoop.instance()

    application.db = momoko.Pool(
        dsn='dbname=democracydb user=exampleuser password=thiswillnotbelive '
            'host=localhost port=5432',
        size=1,
        ioloop=ioloop,
    )
    
    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(8888, 'localhost')
    ioloop.start()