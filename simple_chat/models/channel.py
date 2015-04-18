from __future__ import unicode_literals

from datetime import datetime

from sqlalchemy import and_, or_, desc

from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel
from .base import NOT_SET




class ChannelModel(BaseTableModel):
    """chat data model
    
    """
    TABLE = tables.Channel

    guid_factory = GuidFactory('C')

    def get_channel(self, user_id1, user_id2):
        return self.session\
            .query(self.TABLE)\
            .filter(or_(
            and_(self.TABLE.user_id1==user_id1, self.TABLE.user_id2==user_id2),
            and_(self.TABLE.user_id1==user_id2, self.TABLE.user_id2==user_id1))
            ).first()

    def get_channels_by_user_id(self, user_id):
        return self.session\
            .query(self.TABLE)\
            .filter(or_(self.TABLE.user_id1==user_id,
                        self.TABLE.user_id2==user_id))\
            .order_by(desc(self.TABLE.created_at))

    def create_channel(self, user_id1, user_id2):
        channel = tables.Channel(
            guid=self.guid_factory(),
            user_id1=user_id1,
            user_id2=user_id2,
        )
        self.session.add(channel)
        self.session.flush()
        return channel

