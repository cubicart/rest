from datetime import datetime
from typing import List
from http import HTTPStatus

from pydantic import BaseModel, ValidationError
from sanic import Blueprint, response
from sanic.views import HTTPMethodView
from tortoise.exceptions import BaseORMException
import bcrypt

from app.model import User


bp = Blueprint('users', url_prefix='/users')


class CreateUserData(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class LoginData(BaseModel):
    username: str
    password: str


class UserView(HTTPMethodView):
    async def get(self, request):
        return response.json({'a': 200})

    async def post(self, request):
        try:
            data = CreateUserData(**request.json)

            user = await User.create(
                username=data.username,
                password=bcrypt.hashpw(
                    data.password.encode(), bcrypt.gensalt()),
                first_name=data.first_name,
                last_name=data.last_name,
            )

            return response.json(str(user), HTTPStatus.CREATED)
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

    if user is None or not bcrypt.checkpw(data.password.encode(), user.password):
        return response.json("username not found", HTTPStatus.NOT_FOUND)

    return response.json(user.id)
