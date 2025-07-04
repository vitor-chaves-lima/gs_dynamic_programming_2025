import jwt
from functools import wraps
from quart import request
from logic.exceptions import InvalidTokenException


def optional_jwt(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                pass

        if token:
            try:
                from logic.config import get_config
                config = get_config()
                secret_key = config.SECRET_KEY

                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                request.current_user_id = payload['user_id']
                request.current_user = payload

            except jwt.ExpiredSignatureError:
                raise InvalidTokenException()
            except jwt.InvalidTokenError:
                raise InvalidTokenException()
            except Exception:
                raise InvalidTokenException()
        else:
            request.current_user_id = None
            request.current_user = None

        return await f(*args, **kwargs)

    return decorated_function