import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/statistics/", StatisticsHandler),
            (r"/about/", AboutHandler),
            (r"/faq/", FAQHandler),
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)


class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")


class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")


class FAQHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()