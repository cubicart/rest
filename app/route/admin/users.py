from datetime import datetime
from typing import List
from http import HTTPStatus

from pydantic import BaseModel, ValidationError
from sanic import Blueprint, response
from sanic.views import HTTPMethodView
import bcrypt

from ... import model


class UserCreateData(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class LoginData(BaseModel):
    username: str
    password: str


bp = Blueprint('users', url_prefix='/users')


class UsersView(HTTPMethodView):
    async def get(self, request):
        return response.json({'a': 200})

    async def post(self, request):
        try:
            data = UserCreateData(**request.json)

            user = await model.User.create(
                username=data.username,
                password=bcrypt.hashpw(
                    data.password.encode(), bcrypt.gensalt()),
                first_name=data.first_name,
                last_name=data.last_name,
            )

            return response.json({'id': user.id})
        except ValidationError as e:
            return response.json(e.errors(), HTTPStatus.BAD_REQUEST)
        except Exception as e:
            return response.json(str(e), HTTPStatus.BAD_REQUEST)


bp.add_route(UsersView.as_view(), '')


@bp.post('/login')
async def login(request):
    try:
        data = LoginData(**request.json)
        user = await model.User.filter(username=data.username).first()
        if user is None:
           return response.json("username not found")

        if bcrypt.checkpw(data.password.encode(), user.password):
            return response.json(user.id)
        else:
            return response.json('incorrect password')
            
    except ValidationError as e:
        return response.json(e.errors(), HTTPStatus.BAD_REQUEST)

    return response.json(data.username)
