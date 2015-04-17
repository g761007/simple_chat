from __future__ import unicode_literals
import os
import hmac
import uuid
import hashlib


B58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B58_BASE = len(B58_CHARS)


def b58encode(s):
    """Do a base 58 encoding (alike base 64, but in 58 char only)

    From https://bitcointalk.org/index.php?topic=1026.0

    by Gavin Andresen (public domain)

    """
    value = 0
    for i, c in enumerate(reversed(s)):
        value += ord(c) * (256 ** i)

    result = []
    while value >= B58_BASE:
        div, mod = divmod(value, B58_BASE)
        c = B58_CHARS[mod]
        result.append(c)
        value = div
    result.append(B58_CHARS[value])
    return ''.join(reversed(result))


def make_guid():
    """Generate a GUID and return in base58 encoded form

    """
    uid = uuid.uuid1().bytes
    return b58encode(uid)


class GuidFactory(object):
    """A GUID factory which generates prefix + guid

    """
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self):
        return self.prefix + make_guid()


def generate_random_code():
    """Generate random code

    """
    random_code = os.urandom(60)
    return hmac.new(random_code).hexdigest()


def salt_password(password, salt=None, hash_name='sha1'):
    """Generate hashed password with salt hash(password + salt)

    if salt is not given, generate_random_code will be used for generating
    the salt value

    """
    if isinstance(password, unicode):
        password = password.encode('utf8')
    if isinstance(salt, unicode):
        salt = salt.encode('utf8')
    if salt is None:
        salt = generate_random_code()

    hash_method = getattr(hashlib, hash_name)

    # generate hashed password
    hashed_pwd = hash_method()
    hashed_pwd.update(password)
    hashed_pwd.update(salt)
    hex_hashed_pwd = hashed_pwd.hexdigest()
    return hash_name, salt, hex_hashed_pwd