import datetime
from database import connection


def checked_user_in_list(user_id, message) -> bool:
    """ """
    is_checked = False
    for user in user_id:
        if user == message.from_user.id:
            is_checked = True
            break
    return is_checked


def added_late_statistic(result) -> list:
    """  """
    time = datetime.time(9, 30)
    response = []
    count = 0
    for row in result:
        response.append(list(row))
        response[count].append('Не опоздал')
        if response[count][3] is not None and response[count][3] > str(time):
            response[count][5] = 'Опоздал'
        if response[count][3] is None:
            response[count][5] = 'Еще не пришел'
        count += 1
    return response


def get_yesterday_statistic() -> list:
    """ Вывод всех сотрудников, за вчерашний день"""
    dp = connection.create_pool()
    cursor = dp.cursor()
    table_name = checked_date(True)
    cursor.execute(
        "SELECT ATTENDANCE_DATE, SWIPE_NAME, DEPT_NAME, SIGNIN_TIME, SIGNOUT_TIME FROM " + table_name + " join dss.adm_card_department on " + table_name + ".DEPT_CODE = dss.adm_card_department.DEPT_CODE WHERE ATTENDANCE_DATE = CURRENT_DATE() - INTERVAL 1 DAY and dss.adm_card_department.DEPT_CODE like '001001%'")
    result = cursor.fetchall()
    response = added_late_statistic(result)
    return response


def get_today_statistic() -> list:
    """ Вывод всех сотрудников, за сегодняшний день"""
    dp = connection.create_pool()
    cursor = dp.cursor()
    table_name = checked_date(False)
    cursor.execute(
        "SELECT ATTENDANCE_DATE, SWIPE_NAME, DEPT_NAME, SIGNIN_TIME, SIGNOUT_TIME FROM " + table_name + " join dss.adm_card_department on " + table_name + ".DEPT_CODE = dss.adm_card_department.DEPT_CODE WHERE ATTENDANCE_DATE = CURRENT_DATE() and dss.adm_card_department.DEPT_CODE like '001001%'")
    result = cursor.fetchall()
    response = added_late_statistic(result)
    return response


def checked_date(isPresent) -> str:
    response = ''
    date_now = datetime.date.today()
    date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    format_date_day = date_now.strftime("%d")
    format_today_month = date_now.strftime("20" + "%y%m")
    format_yesterday_month = date_yesterday.strftime("20" + "%y%m")
    table_name = 'dss.adm_attendance_record_info_'
    if format_date_day == '01' and isPresent:
        response = table_name + format_yesterday_month
        return response
    response = table_name + format_today_month
    return response
