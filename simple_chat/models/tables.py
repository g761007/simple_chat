from __future__ import unicode_literals

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import object_session
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.expression import func


DeclarativeBase = declarative_base()
    
_now_func = [func.utc_timestamp]


def set_now_func(func):
    """Replace now function and return the old function
    
    """
    old = _now_func[0]
    _now_func[0] = func
    return old


def get_now_func():
    """Return current now func
    
    """
    return _now_func[0]


def now_func():
    """Return current datetime
    
    """
    func = get_now_func()
    return func()


# This is the association table for the many-to-many relationship between
# channels and uesrs
user_channel_table = Table(
    'user_channel',
    DeclarativeBase.metadata,
    Column(
        'user_guid',
        Unicode(64),
        ForeignKey(
            'user.guid',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    ),
    Column(
        'channel_guid',
        Unicode(64),
        ForeignKey(
            'channel.guid',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )
)

class DeclarativeBaseExtension:

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(DeclarativeBase, DeclarativeBaseExtension):
    """A user is the entity contains attributes of a member account
    
    """
    __tablename__ = 'user'

    guid = Column(Unicode(64), primary_key=True)
    
    user_name = Column(Unicode(16), unique=True, nullable=False)

    avatar = Column(Unicode(255), nullable=False, default=u'')
    
    access_token = Column(Unicode(255), nullable=True)
    
    display_name = Column(Unicode(255))

    age = Column(Integer, nullable=False)

    gender = Column(Integer, nullable=False)
    
    password = Column('password', String(80))

    updated_at = Column(DateTime, default=now_func)

    created_at = Column(DateTime, default=now_func)
    
    def __unicode__(self):
        return self.display_name or self.user_name


class Message(DeclarativeBase, DeclarativeBaseExtension):
    """A message

    """

    __tablename__ = 'message'

    guid = Column(Unicode(64), primary_key=True)

    msg = Column(Unicode(255))

    user_guid =  Column(Unicode(64), ForeignKey('user.guid'))

    created_at = Column(DateTime, default=now_func)

    channel_guid = Column(Unicode(64), ForeignKey('channel.guid'))

    def __unicode__(self):
        return self.guid



class Channel(DeclarativeBase, DeclarativeBaseExtension):
    """Channel

    """

    __tablename__ = 'channel'

    guid = Column(Unicode(64), primary_key=True)

    created_at = Column(DateTime, default=now_func)

    user_id1 = Column(Unicode(64), ForeignKey('user.guid'))

    user_id2 = Column(Unicode(64), ForeignKey('user.guid'))

    msgs = relationship('Message')

    def __unicode__(self):
        return self.guid
