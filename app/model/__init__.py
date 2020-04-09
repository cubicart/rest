from tortoise.models import Model
from tortoise import Tortoise, fields


async def start():
    await Tortoise.init(
        db_url='sqlite://db.sqlite',
        modules={'models': ['app.model']}
    )

    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()


###########################################################

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

    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'status': self.status,
        }
