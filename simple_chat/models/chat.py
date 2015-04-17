from __future__ import unicode_literals

from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel
from .base import NOT_SET
from sqlalchemy import and_, or_


class ChatModel(BaseTableModel):
    """chat data model
    
    """
    TABLE = tables.Channel

    channel_guid_factory = GuidFactory('C')
    msg_guid_factory = GuidFactory('M')

    def add_msg(self, poster, channel, msg):
        message = tables.Message(
            guid=self.msg_guid_factory(),
            msg=msg,
            user_guid=poster.guid,
            channel_guid=channel.guid
        )
        self.session.add(message)
        self.session.flush()
        return message

    def get_channel(self, user_id1, user_id2):
        return self.session\
            .query(tables.Channel)\
            .filter(or_(and_(tables.Channel.user_id1==user_id1,
                    tables.Channel.user_id2==user_id2), and_(tables.Channel.user_id1==user_id2,
                    tables.Channel.user_id2==user_id1)))\
            .first()

    def create_channel(self, user1, user2):
        channel = tables.Channel(
            guid=self.channel_guid_factory(),
            user_id1=user1.guid,
            user_id2=user2.guid,
        )
        self.session.add(channel)
        self.session.flush()
        return channel

    def get_msgs(self, channel_guid, timestamp=None, limit=10):
        msgs = self.session\
            .query(tables.Message)\
            .filter_by(channel_guid=channel_guid)
        if timestamp:
            msgs = msgs.filter(tables.Message.created_at<=channel_guid)
        return msgs.limit(limit)

