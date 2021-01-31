import db
import datetime


def added_late_statistic(result) -> list:
    """  """
    time = datetime.time(9, 30)
    response = []
    count = 0
    for row in result:
        response.append(list(row))
        response[count].append('Не опоздал')
        if response[count][3] is not None and response[count][3] > time:
            response[count][5] = 'Опоздал'
        if response[count][3] is None:
            response[count][5] = 'Еще не пришел'
        count += 1
    return response


def get_all_statistic() -> list:
    """ Вывод всех сотрудников """
    cursor = db.conn.cursor()
    cursor.execute("select * from statistics")
    result = cursor.fetchall()
    response = added_late_statistic(result)
    return response


def get_yesterday_statistic() -> list:
    """ Вывод всех сотрудников, за вчерашний день"""
    cursor = db.conn.cursor()
    cursor.execute("select * from statistics where indate = current_date - INTERVAL '1 day'")
    result = cursor.fetchall()
    response = added_late_statistic(result)
    return response


def get_today_statistic() -> list:
    """ Вывод всех сотрудников, за сегоднящний день"""
    cursor = db.conn.cursor()
    cursor.execute("select * from statistics where indate = current_date")
    result = cursor.fetchall()
    response = added_late_statistic(result)
    return response
