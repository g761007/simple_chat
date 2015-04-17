from __future__ import unicode_literals

from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel
from .base import NOT_SET


class PermissionModel(BaseTableModel):
    """Permission data model
    
    """
    TABLE = tables.Permission

    guid_factory = GuidFactory('PM')
    
    def get_by_name(self, permission_name):
        """Get a permission by name
        
        """
        permission = (
            self.session
            .query(tables.Permission)
            .filter_by(permission_name=permission_name)
        ).first()
        return permission
    
    def create(
        self, 
        permission_name, 
        display_name=None,
    ):
        """Create a new permission and return its id
        
        """
        permission = tables.Permission(
            guid=self.guid_factory(),
            permission_name=unicode(permission_name), 
            display_name=unicode(display_name) if display_name is not None else None, 
        )
        self.session.add(permission)
        self.session.flush()
        return permission
    
    def update(
        self, 
        permission, 
        display_name=NOT_SET, 
        permission_name=NOT_SET,
    ):
        """Update attributes of a permission
        
        """
        if display_name is not NOT_SET:
            permission.display_name = display_name
        if permission_name is not NOT_SET:
            permission.permission_name = permission_name
        self.session.flush()
