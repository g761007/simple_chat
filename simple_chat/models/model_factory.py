from __future__ import unicode_literals

from .user import UserModel
from .message import MessageModel
from .channel import ChannelModel


class ModelFactory(object):
    def __init__(self, session, settings=None):
        self.session = session
        _settings = settings or {}
        model_cls = _settings.get('model_classes') or {}
        model_classes = {k: v for k, v in model_cls.items()}
        self._model_classes = dict(
            user_model=UserModel,
            message_model=MessageModel,
            channel_model=ChannelModel,
        )
        self._model_classes.update(model_classes)

    def __getattr__(self, attr):
        model_cls = self._model_classes.get(attr)
        if not model_cls:
            raise RuntimeError('no model named {} available!!'.format(attr))
        model = model_cls(self)

        # cache the result
        setattr(self, attr, model)

        return model