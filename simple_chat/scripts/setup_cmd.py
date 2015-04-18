from __future__ import unicode_literals

from distutils.core import Command

class RunServerCommand(Command):
    description = "run server"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from simple_chat.core import load_deps, app, setup_logging
        setup_logging()
        load_deps()
        import  logging
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(
            address=app.config['SERVER_HOSTNAME'],
            port=app.config['SERVER_PORT'])
        logger = logging.getLogger(__name__)
        logger.info('start to run server at %s:%s',
                    app.config['SERVER_HOSTNAME'],
                    app.config['SERVER_PORT'])
        IOLoop.instance().start()


class InitDBCommand(Command):
    description = "Initialize db"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from ..models import tables
        from ..models.database import write_engine as engine
        tables.DeclarativeBase.metadata.create_all(engine)
        print 'Done.'


