from sanic import Sanic

from . import route

app = Sanic(__name__)


app.blueprint(route.api_v1)
