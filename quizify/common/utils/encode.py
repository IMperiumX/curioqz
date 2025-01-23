import datetime

import jwt
from django.conf import settings


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        return cls.__instance


class Signer(metaclass=Singleton):
    """Used to encrypt, decrypt, and verify tokens based on timestamps"""

    def __init__(self, secret_key=None):
        self.secret_key = secret_key

    def sign(self, value):
        return jwt.encode(value, self.secret_key, algorithm="HS256")

    def unsign(self, value):
        if value is None:
            return value
        try:
            return jwt.decode(value, self.secret_key, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return None

    def sign_t(self, value, expires_in=3600):
        payload = value.copy()
        payload["exp"] = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
            seconds=expires_in,
        )
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def unsign_t(self, value):
        try:
            return jwt.decode(value, self.secret_key, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None


signer = Signer(settings.SECRET_KEY)
