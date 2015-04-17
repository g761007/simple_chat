from __future__ import unicode_literals
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from simple_chat.core import app
from simple_chat.models import tables

read_engine = create_engine(app.config['READ_DATABASE_URI'],
                            convert_unicode=True,
                            pool_recycle=3600)
read_session = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(keep_session=True),
    bind=read_engine))

if app.config['READ_WRITE_SAME']:
    write_engine= read_engine
    write_session = read_session
else:
    write_engine = create_engine(app.config['WRITE_DATABASE_URI'],
                                 convert_unicode=True,
                                 pool_recycle=3600)
    write_session = scoped_session(sessionmaker(
        extension=ZopeTransactionExtension(keep_session=True),
        bind=write_engine))


tables.set_now_func(datetime.datetime.utcnow)

# clean database after request
@app.after_request
def shutdown_session(response):
    read_session.remove()
    write_session.remove()
    return response