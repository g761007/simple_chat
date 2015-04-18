from __future__ import unicode_literals

from datetime import datetime

from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel


class MessageModel(BaseTableModel):
    """message data model
    
    """
    TABLE = tables.Message

    guid_factory = GuidFactory('M')

    def add_msg(self, poster, channel, msg):
        message = self.TABLE(
            guid=self.guid_factory(),
            msg=msg,
            user_guid=poster.guid,
            channel_guid=channel.guid
        )
        self.session.add(message)
        self.session.flush()
        return message

    def get_msgs(self, channel_guid, timestamp=None, limit=10):
        dt = datetime.fromtimestamp(timestamp) \
            if timestamp is not None else datetime.now()
        return self.session\
            .query(self.TABLE)\
            .filter_by(channel_guid=channel_guid)\
            .filter(self.TABLE.created_at<=dt)\
            .order_by(self.TABLE.created_at)\
            .limit(limit)

