from sanic import Blueprint


from . import users

api_v1 = Blueprint.group(users.bp, url_prefix='/api/v1')

