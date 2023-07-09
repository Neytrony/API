import datetime

from djangoProject.celery import app
import time
import csv
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
    'Статус обучения Результат пр знаний': 'eduStatus',
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
        writer = csv.DictWriter(f, delimiter=';', fieldnames=list(YcToBpKeys))
        header = dict()
        for key in YcToBpKeys:
            header[key] = key
        writer.writerow(header)
        for instance in instances:
            line = dict()
            for YcToBpKey in list(YcToBpKeys):
                line[YcToBpKey] = getattr(instance, YcToBpDict[YcToBpKey])
            writer.writerow(line)
