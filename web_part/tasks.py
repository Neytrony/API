import datetime
import csv
from openpyxl import Workbook
from djangoProject.celery import app
from api.models import YcToBp

YcToBpDict = {
    'Тип операции': 'operationType',
    'Табельный номер': 'tabNum',
    'ФИО': 'FIO',
    'Код обучения': 'learnCode',
    'Стоимость курса': 'courseCost',
    'Наименование программы обучения': 'eduName',
    'Продолжительность обучения': 'eduTime',
    'Ссылка на курс обучения сотрудника': 'eduUrl',
    'Статус обучения': 'eduStatus',
    'Результат пр знаний': 'result',
    'Документы протокола': 'protocol',
    'Номер протокола': 'protocolNum',
    'Дата протокола': 'protocolDate',
    'Член комиссии 1': 'memberId1',
    'Член комиссии 2': 'memberId2',
    'Член комиссии 3': 'memberId3',
    'Удостоверение(файл)': 'cert',
    'Дата удостоверения ': 'certDate',
    'Номер удостоверения': 'certNum',
    'Номер ФГИС ': 'FGISNum',
    'Статус СДО': 'platformStatus',
}

@app.task
def update_info(filename):
    reader = csv.DictReader(open(f'mediafiles/{filename}'))

    for row in reader:
        instance = YcToBp.objects.filter(id=row['id'])
        if instance.exists():
            instance = instance.first()
            for key, value in row.items():
                if key != 'id':
                    setattr(instance, YcToBpDict[key], value)
            instance.save()


@app.task
def get_info_csv():
    instances = YcToBp.objects.all()
    now = datetime.datetime.now()
    with open(f'mediafiles/YcToBp_{now}.csv', 'w', newline='') as f:
        YcToBpKeys = YcToBpDict.keys()
        fieldanames = ['id'] + list(YcToBpKeys)
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldanames)
        headers = {'id': 'id'}
        for key in YcToBpKeys:
            headers[key] = key
        writer.writerow(headers)
        for instance in instances:
            line = {'id': instance.id}
            for YcToBpKey in list(YcToBpKeys):
                line[YcToBpKey] = getattr(instance, YcToBpDict[YcToBpKey])
            writer.writerow(line)


@app.task
def get_info_xlsx():
    instances = YcToBp.objects.all()
    now = datetime.datetime.now()
    YcToBpKeys = YcToBpDict.keys()
    # with open(f'mediafiles/YcToBp_{now}.csv', 'w', newline='') as f:
    #     YcToBpKeys = YcToBpDict.keys()
    #     fieldanames = ['id'] + list(YcToBpKeys)
    #     writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldanames)
    #     header = {'id': 'id'}
    #     for key in YcToBpKeys:
    #         header[key] = key
    #     writer.writerow(header)
    #
    #
    #         writer.writerow(line)

    book = Workbook()
    sheet = book.create_sheet()
    headers = {'id': 'id'}
    for key in YcToBpKeys:
        headers[key] = key
    # Rows and columns are zero indexed.
    row = 0
    column = 0
    # iterating through the content list
    for header in headers.keys():
        sheet.cell(row=row, column=column, value=header)
        column += 1
    max_column = column
    row = 1
    for instance in instances:
        for col in range(0, max_column + 1):
            cell = sheet.cell_value(row=0, col=col)
            value = getattr(instance, cell)
            sheet.cell(row=row, column=col, value=value)
    book.save(f'mediafiles/YcToBp_{now}.xlsx')



#excelData = xlrd.open_workbook(file)
# sheet = excelData.sheet_by_index(0)
#    line = {'Payment': sheet.row_values(4)[1].split(" ")[-1], 'Data': sheet.row_values(4)[11],
#                             'Payer': sheet.row_values(8)[1],
#                             'INN_P': sheet.row_values(7)[1].split(" ")[1],
#                             'KPP_P': sheet.row_values(7)[6].split(" ")[-1], 'Sum': sheet.row_values(7)[14],
#                             'Bank_R_Check': sheet.row_values(9)[14],
#                             'Bank_P': sheet.row_values(11)[1], 'BIK_R': sheet.row_values(11)[14],
#                             'Korr_R': sheet.row_values(12)[14], 'Bank_R': sheet.row_values(14)[1],
#                             'BIK_P': sheet.row_values(14)[14],
#                             'Korr_P': sheet.row_values(15)[14],
#                             'Recipient': sheet.row_values(18)[1], 'INN_R': sheet.row_values(17)[1].split(" ")[-1],
#                             'KPP_R': sheet.row_values(17)[6].split(" ")[1],
#                             'Bank_P_Check': sheet.row_values(17)[14],
#                             'Purpose': sheet.row_values(23)[1]}
#                     writer.writerow((line))

