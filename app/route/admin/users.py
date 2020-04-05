from datetime import datetime
from typing import List

from pydantic import BaseModel
from sanic import Blueprint, response


bp = Blueprint('users', url_prefix='/users')


@bp.post('/login')
async def login(request):
    data = LoginModel(**request.json)
    return response.json(data.username)


class LoginModel(BaseModel):
    username: str
    password: str
