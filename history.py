from peewee_models import db, Log
from datetime import datetime


def start_db() -> None:
    """
    This func is called at the beginning main.py. It cleans the table in database or creates new table, if not exist
    :return: None
    """
    with db:
        if Log.table_exists():
            dlt = Log.delete()
            dlt.execute()
        else:
            db.create_tables([Log])


def add_instance(data_list: list) -> None:
    """
    This func add new instance in table
    :param data_list: a list that contains command name and info about all hotels (list)
    :return: None
    """
    dtime = datetime.now()
    with db:
        Log.create(command_name=data_list[1], date_and_time=dtime, hotels_data=data_list[0]).save()


def get_history_data_generator() -> str:
    """
    This func gives all logs from database
    :return: str
    """
    data = Log.select()
    if data:
        for log in data:
            h_data_send = ''
            for hotel_data_dict in log.hotels_data:
                h_data_send += f'\n{"".join(hotel_data_dict.values())}'
                h_data_send += "\n"

            r_str = f'Название команды: {log.command_name}\nДата и время: {log.date_and_time}\nИстория отелей:\n' \
                    f'{h_data_send}'
            yield r_str
    else:
        return 'История поиска еще пустая'
