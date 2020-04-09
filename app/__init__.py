from sanic import Sanic

from . import route
from .route import admin as admin_route
from . import model

app = Sanic(__name__)


app.blueprint(route.api_v1)
app.blueprint(admin_route.api_v1)


@app.listener('before_server_start')
async def before_start(sanic, loop):
    await model.start()


@app.listener('after_server_stop')
async def after_stop(sanic, loop):
    await model.stop()
