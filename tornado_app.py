import os
import tornado
from tornado.wsgi import WSGIContainer
from tornado.web import FallbackHandler, Application
from pred import app

container = WSGIContainer(app)
handlers = [(r".*", FallbackHandler, dict(fallback=container))]
tornado_app = Application(handlers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    tornado_app.listen(port)
    tornado.ioloop.IOLoop.current().start()

