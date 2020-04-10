from sanic import Blueprint, response
from sanic.log import logger
import jwt
from jwt.exceptions import DecodeError


from app import config
from . import users

api_v1 = Blueprint.group(users.bp, url_prefix='/api/v1/admin')


white_paths = [
    '/api/v1/admin/users/login',
]


@api_v1.middleware('request')
async def authorization_middleware(request):
    if request.path in white_paths:
        return None

    token = request.headers.get('authorization')
    if token is None or not token.startswith(config.TOKEN_PREFIX):
        return response.json('invalid authorization header', 400)

    x = len(config.TOKEN_PREFIX) + 1
    token = token[x:]

    try:
        decoded = jwt.decode(token, config.SECRET_KEY,
                             leeway=10, algorithms='HS512')
    except DecodeError as e:
        return response.json(f'JWT decode error: {e}', 400)

    if decoded['for'] != 'admin':
        return response.json('invalid token', 400)

    request.ctx.user = {
        'id': decoded['uid'],
        'role': decoded['rol']
    }

    return None
