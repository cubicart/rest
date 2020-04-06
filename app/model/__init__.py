from tortoise.models import Model
from tortoise import Tortoise, fields


class User(Model):
    class Meta:
        table = 'users'

    id = fields.IntField(pk=True)
    username = fields.CharField(unique=True, max_length=64)
    password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64)
    status = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now=True)


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite',
        modules={'models': ['app.model']}
    )

    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()
