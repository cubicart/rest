from sanic import Blueprint


from . import customers

api_v1 = Blueprint.group(customers.bp, url_prefix='/api/v1')
