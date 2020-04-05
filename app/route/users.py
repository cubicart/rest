from sanic import Blueprint, response


bp = Blueprint('users', url_prefix='/users')


@bp.get('/login')
async def login(request):
    return response.json({'status': 'ok'})
