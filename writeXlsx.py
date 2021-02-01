import xlsxwriter


def write_in_xlsx(date, stat, count=1) -> None:
    """ Создание экзель файла для записи сотрудников"""
    workbook = xlsxwriter.Workbook('./xlsx-files/statistics' + str(date) + '.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Дата')
    worksheet.write(0, 1, 'ФИО')
    worksheet.write(0, 2, 'Отдел')
    worksheet.write(0, 3, 'Время прихода')
    worksheet.write(0, 4, 'Время ухода')
    worksheet.write(0, 5, 'Опоздание')

    for x in stat:
        worksheet.write(count, 0, str(x[0]))
        worksheet.write(count, 1, x[1])
        worksheet.write(count, 2, str(x[2]))
        worksheet.write(count, 3, str(x[3]))
        worksheet.write(count, 4, str(x[4]))
        worksheet.write(count, 5, x[5])
        count += 1
    workbook.close()
