from __future__ import unicode_literals
import hmac

from sqlalchemy.sql.expression import or_
from sqlalchemy.sql.expression import func

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

    def get_by_email(self, email):
        """Get a user by email

        """
        user = (
            self.session
            .query(tables.User)
            .filter_by(email=email)
            .first()
        )
        return user

    def get_by_name_or_email(self, name_or_email):
        """Get a user by name or email

        """
        User = tables.User
        user = (
            self.session
            .query(User)
            .filter(or_(
                func.lower(User.user_name) == name_or_email.lower(),
                func.lower(User.email) == name_or_email.lower()
            ))
        )
        return user.first()

    @classmethod
    def salt_password(cls, password):
        return '$'.join(salt_password(password))

    def create(
        self, 
        user_name, 
        display_name,
        password,
        email,
        verified=False, 
    ):
        """Create a new user and return verification
        
        """
        user_name = user_name.lower()
        email = email.lower()
        salted_password = self.salt_password(password)
        
        # create user
        user = tables.User(
            guid=self.guid_factory(),
            user_name=unicode(user_name),
            email=unicode(email),
            display_name=unicode(display_name), 
            password=salted_password,
            created_at=tables.now_func(),
            verified=verified, 
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
        email=NOT_SET,
        access_token=NOT_SET,
        avatar=NOT_SET,
        verified=NOT_SET,
        password=NOT_SET,
        groups=NOT_SET
    ):
        """Update attributes of a user
        
        """
        if display_name is not NOT_SET:
            user.display_name = display_name
        if email is not NOT_SET:
            user.email = email
        if access_token is not NOT_SET:
            user.access_token = access_token
        if verified is not NOT_SET:
            user.verified = verified
        if avatar is not NOT_SET:
            user.avatar = avatar
        if password is not NOT_SET:
            user.password = self.salt_password(password) 
        if groups is not NOT_SET:
            user.groups = groups
        user.updated_at = tables.now_func()
        self.session.flush()

    def get_recovery_code(self, user, key):
        """Get current recovery code of a user

        """
        h = hmac.new(key)
        h.update('%s%s%s%s' % (
            user.guid,
            user.user_name,
            user.email,
            user.password
        ))
        return h.hexdigest()

    def get_verification_code(self, user, verify_type, secret):
        """Get a verification code of user

        """
        code_hash = hmac.new(secret)
        code_hash.update(str(user.guid))
        code_hash.update(str(user.user_name))
        code_hash.update(str(verify_type))
        return code_hash.hexdigest()
