from sanic import Blueprint, response


bp = Blueprint('customers', url_prefix='/customers')


@bp.get('/login')
async def login(request):
    return response.json({'status': 'ok'})
