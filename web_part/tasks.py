import csv
from openpyxl import Workbook, load_workbook
from djangoProject.celery import app
from api.models import YcToBp
from web_part.models import Files

YcToBpDict = {
    'id': 'id',
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
    'Номер протокола': 'protocolNum',
    'Дата протокола': 'protocolDate',
    'Член комиссии 1': 'memberId1',
    'Член комиссии 2': 'memberId2',
    'Член комиссии 3': 'memberId3',
    'Дата удостоверения ': 'certDate',
    'Номер удостоверения': 'certNum',
    'Номер ФГИС ': 'FGISNum',
    'Статус СДО': 'platformStatus',
    'Документы протокола': 'protocol',
    'Удостоверение(файл)': 'cert',
}


@app.task
def update_info(filename):
    ext = filename.split('.')[-1]
    full_path = f'mediafiles/import/{filename}'
    if ext == 'csv':
        csv_update(full_path)
    elif ext == 'xlsx' or ext == 'xls':
        xlsx_update(full_path)


def csv_update(filename):
    reader = csv.DictReader(open(filename), delimiter=';')
    for row in reader:
        row = dict(row)
        with open('mediafiles/logs/error.log', 'w') as f:
            f.write(str(row))
        instance = YcToBp.objects.filter(id=row['id'])
        if instance.exists():
            instance = instance.first()
            for key, value in row.items():
                if key != 'id':
                    setattr(instance, YcToBpDict[key], value)
            instance.save()


def xlsx_update(filename):
    book = load_workbook(filename=filename)
    sheet = book.active
    for row in range(2, sheet.max_row + 1):
        instance = YcToBp.objects.filter(id=sheet.cell(row=row, column=1).value)
        if instance.exists():
            instance = instance.first()
            for column in range(2, sheet.max_column + 1):
                value = sheet.cell(row=row, column=column).value
                if value is not None:
                    setattr(instance, YcToBpDict[sheet.cell(row=1, column=column).value], value)
            instance.save()


@app.task
def get_info_csv(filename):
    instances = YcToBp.objects.all()
    with open(f'mediafiles/export/{filename}', 'w', newline='', encoding='Windows-1251') as f:
        YcToBpKeys = YcToBpDict.keys()
        fieldnames = list(YcToBpKeys)
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
        headers = dict()
        for key in YcToBpKeys:
            headers[key] = key
        writer.writerow(headers)
        for instance in instances:
            line = dict()
            for YcToBpKey in list(YcToBpKeys):
                line[YcToBpKey] = getattr(instance, YcToBpDict[YcToBpKey])
            writer.writerow(line)
    file = Files.objects.get(name=filename)
    file.fileField = f'export/{filename}'
    file.save()


@app.task
def get_info_xlsx(filename):
    instances = YcToBp.objects.all()
    YcToBpKeys = YcToBpDict.keys()
    book = Workbook()
    sheet = book.active
    headers = dict()
    for key in YcToBpKeys:
        headers[key] = key
    row = 1
    column = 1
    for header in headers.keys():
        sheet.cell(row=row, column=column, value=header)
        column += 1
    max_column = column
    row = 2
    for instance in instances:
        for col in range(1, max_column):
            cell = sheet.cell(row=1, column=col).value
            value = getattr(instance, YcToBpDict[cell])
            if cell == 'Документы протокола' or cell == 'Удостоверение(файл)':
                value = value.name
            sheet.cell(row=row, column=col, value=value)
        row += 1
    book.save(f'mediafiles/export/{filename}')
    file = Files.objects.get(name=filename)
    file.fileField = f'export/{filename}'
    file.save()
    with open('mediafiles/logs/1.txt','w') as g:
        g.write(file.name)
        g.write(file.fileField.path)
        g.write('123213213')

# excelData = xlrd.open_workbook(file)
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
