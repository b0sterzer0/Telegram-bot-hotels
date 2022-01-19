from peewee import SqliteDatabase, Model, CharField, DateTimeField
from playhouse.sqlite_ext import JSONField

db = SqliteDatabase('bot.db')


class Log(Model):
    """
    This class describes model for peewee
    """
    command_name = CharField()
    date_and_time = DateTimeField()
    hotels_data = JSONField()

    class Meta:
        database = db
        db_table = 'Logs'

