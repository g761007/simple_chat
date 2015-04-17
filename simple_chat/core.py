from __future__ import unicode_literals
import os

from flask import Flask

from simple_chat.models.model_factory import ModelFactory

app = Flask(__name__, '/static')
app.config.from_object('simple_chat.default_settings')



key = 'SIMPLE_CHAT_SETTINGS'
if key in os.environ:
    app.logger.info('Load configuration from %s=%s', key, os.environ[key])
    app.config.from_envvar(key)


def setup_logging():
    """Setup logging configuration

    """
    import logging.config
    import yaml

    log_path = 'logging.yaml'
    if os.path.exists(log_path):
        config = yaml.load(open(log_path, 'rt'))
        logging.config.dictConfig(config)
    else:
        if not app.config['DEBUG']:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)


def load_deps():
    """Load dependencies

    """
    from simple_chat.views.api import api
    app.register_module(api)


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    setup_logging()
    load_deps()
    app.run()