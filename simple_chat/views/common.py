from __future__ import unicode_literals
from functools import wraps

from flask import request
from flask import abort
from flask import current_app

from simple_chat.core import app


"""check flask_scaffold api

"""
def check_api_key():
    api_key = request.values.get('api_key', '')
    if not api_key in app.config['API_KEYS']:
        abort(403)


"""Taken from:  https://gist.github.com/1094140

"""
def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function