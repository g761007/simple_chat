from __future__ import unicode_literals
import logging
logger = logging.getLogger(__name__)

from flask import Module
from flask import request
from flask import jsonify
from flask import abort

from simple_chat.models.database import write_session
from simple_chat.models.model_factory import ModelFactory
model_factory = ModelFactory(write_session)

api = Module(__name__)


@api.route('/version', methods=['GET'])
def version():
    logger.debug('version')
    if request.method == 'GET':
        from ..default_settings import VERSION
        return jsonify(data=dict(version=VERSION))
    abort(403)


@api.route('/login', methods=['POST'])
def login():
    logger.debug('login')
    if request.method == 'POST':
        try:
            import transaction
            with transaction.manager:
                request_form = request.form
                user_name = request_form['user_name']
                password = request_form['password']
                user_model = model_factory.user_model
                user = user_model.get_by_name(user_name)

                if user_model.validate_password(user, password):
                    from simple_chat.utils import make_guid
                    user_model.update(user, access_token=make_guid())
                    data = dict(status=1,
                                data=dict(user_name=user.user_name,
                                          avatar=user.avatar,
                                          access_token=user.access_token,
                                          create_at=str(user.created_at),
                                          updated_at=str(user.updated_at)
                                ))
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status=-1, message='{}'.format(err))
        return jsonify(**data)
    abort(403)


@api.route('/users', methods=['GET'])
def user_list():
    logger.debug('user list')
    if request.method == 'GET':
        try:
            request_values = request.values
            user_model = model_factory.user_model
            access_token = request_values['access_token']
            user = user_model.get_by_access_token(access_token)
            if not user:
                return jsonify(status=0, error='Error access token')
            user_model = model_factory.user_model
            access_token = request_values['access_token']
            owner = user_model.get_by_access_token(access_token)
            if not owner:
                return jsonify(status=0, error='Error access token')
            users = user_model.get_list()
            data = dict(status=1, data=[dict(user_name=user.user_name,
                                      avatar=user.avatar,
                                      updated_at=user.updated_at
                            ) for user in users \
                                        if user.user_name != owner.user_name])
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status=0, error='{}'.format(err))
        return jsonify(**data)
    abort(403)


@api.route('/msgs', methods=['POST', 'GET'])
def msgs_apis():
    logger.debug('send_msg')
    if request.method == 'POST':
        try:
            import transaction
            with transaction.manager:
                request_form = request.form
                user_model = model_factory.user_model
                access_token = request_form['access_token']
                poster = user_model.get_by_access_token(access_token)
                if not poster:
                    return jsonify(status=0, error='Error access token')
                user_name = request_form['user_name']
                receiver = user_model.get_by_name(user_name)
                if not receiver:
                    return jsonify(status=0, error='No user:%s' % user_name)

                chat_model = model_factory.chat_model
                channel = chat_model.get_channel(poster.guid, receiver.guid)
                if not channel:
                    channel = chat_model.create_channel(poster, receiver)
                msg = request_form.get('msg')
                message = chat_model.add_msg(poster=poster, channel=channel, msg=msg)
                data = dict(status=1, data=message.as_dict())
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status=0, error='{}'.format(err))
        return jsonify(**data)
    elif request.method == 'GET':
        try:
            request_values = request.values
            user_model = model_factory.user_model
            access_token = request_values['access_token']
            user = user_model.get_by_access_token(access_token)
            if not user:
                return jsonify(status=0, error='Error access token')

            user_name = request_values['user_name']
            receiver = user_model.get_by_name(user_name)
            if not receiver:
                return jsonify(status=0, error='No user:%s' % user_name)

            chat_model = model_factory.chat_model
            channel = chat_model.get_channel(user.guid, receiver.guid)
            if not channel:
                import transaction
                with transaction.manager:
                    channel = chat_model.create_channel(user, receiver)
            ts = int(request_values.get('ts'))
            limit = int(request_values.get('limit', 10))
            msgs = chat_model.get_msgs(channel.guid, timestamp=ts, limit=limit)
            data = dict(status=1, data=[msg.as_dict() for msg in msgs])
        except Exception as err:
            logger.warn('Error: %r', err)
            data = dict(status=0, error='{}'.format(err))
        return jsonify(**data)
    abort(403)

@api.route('/test', methods=['GET'])
def create_users():
    import transaction
    with transaction.manager:
        user_model = model_factory.user_model
        for i in range(10):
            user = user_model.create(
                user_name='test_user%d' % i,
                display_name='test_user%d' % i,
                email='test_user%d@test.com' % i,
                password='123456',
                verified=True,
            )
            logger.info('Created admin, guid=%s' % user.guid)
    return 'ok'
