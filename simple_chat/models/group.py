from __future__ import unicode_literals

from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel
from .base import NOT_SET


class GroupModel(BaseTableModel):
    """Group data model
    
    """
    TABLE = tables.Group

    guid_factory = GuidFactory('GP')

    def get_by_name(self, group_name):
        """Get a group by name
        
        """
        group = (
            self.session
            .query(tables.Group)
            .filter_by(group_name=group_name)
        ).first()
        return group
    
    def create(
        self, 
        group_name, 
        display_name=None,
        permissions=None,
    ):
        """Create a new group and return its id
        
        """
        group = tables.Group(
            guid=self.guid_factory(),
            group_name=unicode(group_name), 
            display_name=unicode(display_name) if display_name is not None else None, 
            created_at=tables.now_func()
        )
        if permissions is not None:
            group.permissions = permissions
        self.session.add(group)
        self.session.flush()
        return group
    
    def update(
        self, 
        group, 
        display_name=NOT_SET, 
        group_name=NOT_SET,
        permissions=NOT_SET,
    ):
        """Update attributes of a group
        
        """
        if display_name is not NOT_SET:
            group.display_name = display_name
        if group_name is not NOT_SET:
            group.group_name = group_name
        if permissions is not NOT_SET:
            group.permissions = permissions
        self.session.flush()
