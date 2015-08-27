from __future__ import unicode_literals
import logging
logger = logging.getLogger(__name__)

from flask import Module
from flask import request
from flask import jsonify
from flask import abort

from ..models.database import write_session
from ..models.model_factory import ModelFactory

model_factory = ModelFactory(write_session)

api = Module(__name__)


@api.route('/version', methods=['GET'])
def version():
    logger.debug('version')
    if request.method == 'GET':
        from ..default_settings import VERSION
        return jsonify(status=1, version=VERSION)
    abort(403)


@api.route('/signup', methods=['POST'])
def signup():
    logger.debug('signup')
    if request.method == 'POST':
        try:
            import transaction
            with transaction.manager:
                request_form = request.form
                params = dict(
                    user_name=request_form['user_name'],
                    display_name=request_form['display_name'],
                    password=request_form['password'],
                    age=int(request_form['age']),
                    gender=int(request_form['gender']),
                    avatar=request_form['avatar']
                )
                user_model = model_factory.user_model
                user = user_model.get_by_name(params['user_name'])
                if user is not None:
                    return jsonify(
                        status=-1,
                        message='username (%s) does exist' % params['user_name']
                    )
                user = user_model.create(**params)
                return jsonify(status=1, data=dict(guid=user.guid,
                                                   user_name=user.user_name,
                                                   display_name=user.display_name,
                                                   age=user.age,
                                                   gender=user.gender,
                                                   avatar=user.avatar,
                                                   created_at=user.created_at))
        except Exception as err:
            logger.error('Error: %r', err)
            data = dict(status=-1, message='{}'.format(err))
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
                if user is None:
                    return jsonify(status=0, error='No user:%s' % user_name)
                if user_model.validate_password(user, password):
                    from ..utils import make_guid
                    user_model.update(user, access_token=make_guid())
                    return jsonify(
                        status=1,
                        data=dict(user_name=user.user_name,
                                  display_name=user.display_name,
                                  age=user.age,
                                  access_token=user.access_token,
                                  gender=user.gender,
                                  avatar=user.avatar,
                                  updated_at=str(user.updated_at),
                                  created_at=str(user.created_at),
                        ))
        except Exception as err:
            logger.error('Error: %r', err)
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
            if not request_values.get('debug'):
                # FIXME: refacotring this
                access_token = request_values['access_token']
                owner = user_model.get_by_access_token(access_token)
                if not owner:
                    return jsonify(status=0, error='Error access token')
            offset = request_values.get('offset', 0)
            limit = request_values.get('limit', 10)
            users = user_model.get_list(offset=offset, limit=limit)
            data = dict(status=1,
                        total=user_model.count(),
                        data=[dict(user_name=user.user_name,
                                   avatar=user.avatar,
                                   gender=user.gender,
                                   age=user.age,
                                   display_name=user.display_name,
                                   updated_at=user.updated_at
                        ) for user in users])
        except Exception as err:
            logger.error('Error: %r', err)
            data = dict(status=-1, error='{}'.format(err))
        return jsonify(**data)
    abort(403)


def send_msg():
    try:
        import transaction
        with transaction.manager:
            request_form = request.form
            user_model = model_factory.user_model
            access_token = request_form['access_token']
            poster = user_model.get_by_access_token(access_token)
            if not poster:
                return jsonify(status=0, error='access token error')
            user_name = request_form['user_name']
            if poster.user_name == user_name:
                return jsonify(status=0, error='user_name error')
            receiver = user_model.get_by_name(user_name)
            if not receiver:
                return jsonify(status=0, error='No user:%s' % user_name)

            channel_model = model_factory.channel_model
            message_model = model_factory.message_model
            channel = channel_model.get_channel(poster.guid, receiver.guid)
            if not channel:
                channel = channel_model.create_channel(poster.guid,
                                                       receiver.guid)
            msg = request_form.get('msg')
            message = message_model.add_msg(poster=poster,
                                            channel=channel,
                                            msg=msg)
            data = dict(status=1, data=dict(guid=message.guid,
                                            msg=message.msg,
                                            create_at=message.created_at,
                                            channel_guid=message.channel_guid,
                                            user_name=poster.user_name))
    except Exception as err:
        logger.error('Error: %r', err)
        data = dict(status=-1, error='{}'.format(err))
    return jsonify(**data)

def get_msgs():
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

        channel_model = model_factory.channel_model
        message_model = model_factory.message_model
        channel = channel_model.get_channel(user.guid, receiver.guid)
        if not channel:
            import transaction
            with transaction.manager:
                channel = channel_model.create_channel(user.guid, receiver.guid)
        ts = request_values.get('ts')
        if ts is not None:
            ts = int(ts)
        limit = int(request_values.get('limit', 10))
        direct = int(request_values.get('direct', -1))
        msgs = message_model.get_msgs(channel.guid,
                                      timestamp=ts,
                                      limit=limit,
                                      direct=direct)
        data = dict(status=1,
                    total=len(channel.msgs),
                    data=[dict(guid=msg.guid,
                               msg=msg.msg,
                               created_at=msg.created_at,
                               channel_guid=msg.channel_guid,
                               user_name=receiver.user_name if msg.user_guid == receiver.guid else user.user_name) for msg in msgs])
    except Exception as err:
        logger.error('Error: %r', err)
        data = dict(status=-1, error='{}'.format(err))
    return jsonify(**data)


@api.route('/msgs', methods=['POST', 'GET'])
def msgs():
    logger.debug('send_msg')
    if request.method == 'POST':
        return send_msg()
    elif request.method == 'GET':
        return get_msgs()
    abort(403)


@api.route('/channels', methods=['GET'])
def get_channels():
    logger.debug('get channels')
    if request.method == 'GET':
        try:
            request_values = request.values
            user_model = model_factory.user_model
            access_token = request_values['access_token']
            user = user_model.get_by_access_token(access_token)
            if not user:
                return jsonify(status=0, error='Error access token')
            channel_model = model_factory.channel_model
            channels = list(channel_model.get_channels_by_user_id(user.guid))
            user_ids = set()
            for c in channels:
                user_ids.add(c.user_id1)
                user_ids.add(c.user_id2)
            user_ids.remove(user.guid)
            users = dict()
            for u in user_model.get_list(ids=user_ids):
                users[user.guid] = u
            data = []
            for c in channels:
                u = users[c.user_id1] if c.user_id1 == user.guid \
                    else users[c.user_id2]
                data.append({
                    'channel_guid': c.guid,
                    'user_name': u.user_name,
                    'display_name': u.display_name,
                    'avatar': u.avatar,
                    'gender': u.gender,
                    'age': u.age,
                    'msgs': len(c.msgs),
                    'created': c.created_at,
                })
            return jsonify(status=1, data=data, total=len(channels))
        except Exception as err:
            logger.error('Error: %r', err)
            return jsonify(status=-1, error='{}'.format(err))
    abort(403)


@api.route('/test_users', methods=['POST'])
def create_test_users():
    if request.method == 'POST':
        import random
        import transaction
        prefix = request.form.get('prefix', 'testuser')
        cnt = int(request.form.get('cnt', 10))
        with transaction.manager:
            user_model = model_factory.user_model
            for i in range(1, cnt+1):
                name = '%s%d' % (prefix, i)
                user = user_model.create(
                    user_name=name,
                    display_name=name,
                    gender=random.randrange(0,2),
                    age=random.randrange(18,100),
                    avatar='http://z.m.ipimg.com/-150c-/8/D/8/7/0/4/1/B/8D87041BE46F9711B4BBA88B3409C1EB.jpg',
                    password='123456'
                )
                logger.info('Created user %s, guid=%s', name, user.guid)
        return 'ok'
    abort(403)
