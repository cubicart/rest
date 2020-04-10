import datetime
from typing import List
from http import HTTPStatus

from pydantic import BaseModel, ValidationError, constr
from sanic import Blueprint, response
from sanic.views import HTTPMethodView
from tortoise.exceptions import BaseORMException
import bcrypt
import jwt

from app.model import User
from app import config


bp = Blueprint('users', url_prefix='/users')


class CreateUserData(BaseModel):
    username: constr(min_length=3, max_length=64, strip_whitespace=True)
    password: constr(min_length=6, max_length=10)
    first_name: constr(min_length=2, max_length=64, strip_whitespace=True)
    last_name: constr(min_length=2, max_length=64, strip_whitespace=True)


class LoginData(BaseModel):
    username: constr(min_length=1, max_length=64, strip_whitespace=True)
    password: str


class UserView(HTTPMethodView):
    async def get(self, request):
        return response.json({'a': 200})

    async def post(self, request):
        try:
            data = CreateUserData(**request.json)

            hashed_password = bcrypt.hashpw(
                data.password.encode(), bcrypt.gensalt())

            user = await User.create(
                username=data.username,
                password=hashed_password.decode(),
                first_name=data.first_name,
                last_name=data.last_name,
            )

            return response.json(user.dict(), HTTPStatus.CREATED)
        except ValidationError as e:
            return response.json(e.errors(), HTTPStatus.BAD_REQUEST)
        except BaseORMException as e:
            return response.json(str(e), HTTPStatus.CONFLICT)
        except Exception as e:
            return response.json(str(e), HTTPStatus.BAD_REQUEST)


bp.add_route(UserView.as_view(), '')


@bp.post('/login')
async def login(request):
    try:
        data = LoginData(**request.json)
    except ValidationError as e:
        return response.json(e.errors(), HTTPStatus.BAD_REQUEST)

    user = await User.filter(username=data.username).first()

    if user is None or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        return response.json('username/password does not match', HTTPStatus.NOT_FOUND)

    if not user.is_active:
        return response.json('user not active', HTTPStatus.NOT_FOUND)

    payload = {
        'uid': user.id,
        'rol': user.role,
        'for': 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config.JWT_EXP),
    }
    access_token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS512')

    return response.json({
        'access': access_token,
        'prefix': config.TOKEN_PREFIX
    })
