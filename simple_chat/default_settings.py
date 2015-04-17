from __future__ import unicode_literals
# is the debug mode on
DEBUG = True

# !!!WARNING!!! MODIFY THIS IN PRODUCTION
SECRET_KEY = ''

# interface to bind
SERVER_HOSTNAME = '0.0.0.0'

# port to bind
SERVER_PORT = 5000

# should we use reloader to run the server
SERVER_USE_RELOADER = False

# should we use debugger to run the server
SERVER_USE_DEBUGGER = False

#: URI of database for reading
READ_DATABASE_URI = 'sqlite:///simple_chat.db'

#: URI of data for writing
WRITE_DATABASE_URI = READ_DATABASE_URI

#: Use same database for reading and writing
READ_WRITE_SAME = True

VERSION = '0.0.0'

#: API kyes
API_KEYS = set([
    '40b27e02d446ed1eca42dce3753cb46e3df82cae',
])