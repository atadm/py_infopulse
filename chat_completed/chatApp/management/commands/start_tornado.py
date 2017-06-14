from tornado.options import options, define
import django.core.handlers.wsgi
import tornado.httpserver, tornado.ioloop
import tornado.web, tornado.wsgi
import chatApp.sockets

import sockjs.tornado


define('port', type=int, default=8888)
wsgi_app = tornado.wsgi.WSGIContainer(
               django.core.handlers.wsgi.WSGIHandler())

tornado_app = tornado.web.Application(
    sockjs.tornado.SockJSRouter(chatApp.sockets.SocketHandler, '/sockjs')
     .urls + [('.*', tornado.web.FallbackHandler,dict(fallback=wsgi_app)),])

server = tornado.httpserver.HTTPServer(tornado_app)
server.listen(options.port)
print("[*] Listening at 0.0.0.0:%i" % (options.port,))
tornado.ioloop.IOLoop.instance().start()