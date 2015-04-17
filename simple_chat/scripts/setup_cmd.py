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
        import getpass

        import transaction

        from simple_chat.models import tables
        from simple_chat.models.model_factory import ModelFactory
        from simple_chat.models.database import write_engine as engine
        from simple_chat.models.database import write_session as session

        tables.DeclarativeBase.metadata.create_all(engine)
        model_factory = ModelFactory(session)
        user_model = model_factory.user_model
        group_model = model_factory.group_model
        permission_model = model_factory.permission_model

        with transaction.manager:
            # create user 'admin'
            admin = user_model.get_by_name('admin')
            if admin is None:
                print 'Create admin account'

                email = raw_input(b'Email:')

                password = getpass.getpass(b'Password:')
                confirm = getpass.getpass(b'Confirm:')
                if password != confirm:
                    print 'Password not match'
                    return

                admin = user_model.create(
                    user_name='admin',
                    display_name='Administrator',
                    email=email,
                    password=password,
                    verified=True,
                )
                print 'Created admin, guid=%s' % admin.guid
            # Create permissions
            admin_permission = permission_model.get_by_name('admin')
            if admin_permission is None:
                print 'Create admin permission ...'
                admin_permission = permission_model.create(
                    permission_name='admin',
                    display_name='Administrate',
                )
            # Create group 'admin'
            admin_group = group_model.get_by_name('admin')
            if admin_group is None:
                print 'Create admin group ...'
                admin_group = group_model.create(
                    group_name='admin',
                    display_name='Administrators',
                )
            print 'Add admin permission to admin group'
            group_model.update(admin_group, permissions=[admin_permission])
            session.flush()
            print 'Add admin to admin group'
            user_model.update(admin, groups=[admin_group])
            session.flush()
            print 'Done.'


