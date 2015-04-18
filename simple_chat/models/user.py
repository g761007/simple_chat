from __future__ import unicode_literals

from ..utils import salt_password
from ..utils import GuidFactory
from . import tables
from .base import BaseTableModel
from .base import NOT_SET


class UserModel(BaseTableModel):
    """User data model
    
    """
    TABLE = tables.User

    guid_factory = GuidFactory('US')
        
    def get_by_name(self, user_name):
        """Get a user by name
        
        """
        user = (
            self.session
            .query(tables.User)
            .filter_by(user_name=user_name)
            .first()
        )
        return user

    def validate_access_token(self, user_name, access_token):
        # TODO:
        pass

    def get_by_access_token(self, access_token):
        """Get a user by access_token

        """
        user = (
            self.session
            .query(tables.User)
            .filter_by(access_token=access_token)
            .first()
        )
        return user

    @classmethod
    def salt_password(cls, password):
        return '$'.join(salt_password(password))

    def create(
        self, 
        user_name, 
        display_name,
        password,
        age,
        gender,
        avatar='',
        access_token=None,
        **kwargs
    ):
        """Create a new user

        """
        user_name = user_name.lower()
        salted_password = self.salt_password(password)
        if not (-1 <gender < 2):
            raise ValueError
        if age < 0:
            raise ValueError
        # create user
        user = tables.User(
            guid=self.guid_factory(),
            user_name=unicode(user_name),
            display_name=unicode(display_name),
            age=age,
            gender=gender,
            avatar=avatar,
            password=salted_password,
            created_at=tables.now_func(),
            updated_at=tables.now_func()
        )
        self.session.add(user)
        self.session.flush()
        return user
    
    def validate_password(self, user, password):
        """Validate password of a user
        
        """
        hash_name, salt, hashed_password = user.password.split('$')
        _, _, input_hashed_password = salt_password(password, salt, hash_name)
        return input_hashed_password == hashed_password

    def update(
        self, 
        user, 
        display_name=NOT_SET, 
        age=NOT_SET,
        gender=NOT_SET,
        access_token=NOT_SET,
        avatar=NOT_SET,
        verified=NOT_SET,
        password=NOT_SET,
    ):
        """Update attributes of a user
        
        """
        if display_name is not NOT_SET:
            user.display_name = display_name
        if age is not NOT_SET and age >= 0:
            user.age = age
        if access_token is not NOT_SET:
            user.access_token = access_token
        if verified is not NOT_SET:
            user.verified = verified
        if avatar is not NOT_SET:
            user.avatar = avatar
        if password is not NOT_SET:
            user.password = self.salt_password(password) 
        if gender is not NOT_SET and not (-1 < gender < 2):
            user.gender = gender
        user.updated_at = tables.now_func()
        self.session.flush()

