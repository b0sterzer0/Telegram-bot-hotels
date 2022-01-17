from peewee import *

db = SqliteDatabase('bot.db')


class Log(Model):
    """
    This class describes model for peewee
    """
    command_name = CharField()
    date_and_time = DateTimeField()
    hotels_data = CharField()

    class Meta:
        database = db
        db_table = 'Logs'

