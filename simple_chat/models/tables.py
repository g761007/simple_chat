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
# groups and permissions. This is required by repoze.what.
group_permission_table = Table(
    'group_permission', DeclarativeBase.metadata,
    Column(
        'group_guid', 
        Unicode(64), 
        ForeignKey(
            'group.guid',
            onupdate='CASCADE', 
            ondelete='CASCADE'
        ),
    ),
    Column(
        'permission_guid', 
        Unicode(64), 
        ForeignKey(
            'permission.guid',
            onupdate='CASCADE', 
            ondelete='CASCADE'
        ),
    )
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
user_group_table = Table(
    'user_group', 
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
        'group_guid', 
        Unicode(64), 
        ForeignKey(
            'group.guid',
            onupdate='CASCADE', 
            ondelete='CASCADE'
        )
    )
)

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


class Group(DeclarativeBase):
    """A group is a bundle of users sharing same permissions
    
    """
    
    __tablename__ = 'group'
    
    guid = Column(Unicode(64), primary_key=True)
    
    group_name = Column(Unicode(16), unique=True, nullable=False)
    
    display_name = Column(Unicode(255))
    
    created_at = Column(DateTime, default=now_func)
    
    users = relationship('User', secondary=user_group_table, backref='groups')

    def __unicode__(self):
        return self.group_name

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(DeclarativeBase):
    """A user is the entity contains attributes of a member account
    
    """
    __tablename__ = 'user'

    guid = Column(Unicode(64), primary_key=True)
    
    user_name = Column(Unicode(16), unique=True, nullable=False)

    avatar = Column(Unicode(255), nullable=False, default=u'')

    email = Column(Unicode(255), unique=True)
    
    access_token = Column(Unicode(255), nullable=True)
    
    display_name = Column(Unicode(255))
    
    password = Column('password', String(80))

    verified = Column(Boolean, default=False)

    updated_at = Column(DateTime, default=now_func)

    created_at = Column(DateTime, default=now_func)
    
    def __unicode__(self):
        return self.display_name or self.user_name
    
    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Permission(DeclarativeBase):
    """A permission indicates the operation can be performed by specific users
    
    """
    
    __tablename__ = 'permission'

    guid = Column(Unicode(64), primary_key=True)
    
    permission_name = Column(Unicode(16), unique=True, nullable=False)
    
    display_name = Column(Unicode(255))
    
    groups = relationship(
        Group, 
        secondary=group_permission_table,
        backref='permissions'
    )

    def __unicode__(self):
        return self.permission_name

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Message(DeclarativeBase):
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

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Channel(DeclarativeBase):
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

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

