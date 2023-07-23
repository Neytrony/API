import json
import base64

from django.conf import settings
from django.db import models
from djangoProject.s3_storage import MediaStorage

media_storage = MediaStorage()
MEDIA_ROOT = settings.MEDIA_ROOT

class Base64Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode()
        return json.JSONEncoder.default(self, o)

class BpToYc(models.Model):
    id = models.AutoField(primary_key=True)
    operationType = models.CharField(max_length=255, null=True, blank=True)
    idYL = models.CharField(max_length=255, null=True, blank=True,)
    idPos = models.CharField(max_length=255, null=True, blank=True,)
    FIO = models.CharField(max_length=255, null=False)
    posName = models.CharField(max_length=255, null=True, blank=True,)
    birthday = models.CharField(max_length=255, null=True, blank=True)
    tabNum = models.CharField(max_length=255, null=False, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    SNILS = models.CharField(max_length=255, null=False)
    dateEmployment = models.CharField(max_length=255, null=True, blank=True)
    dateStartPos = models.CharField(max_length=255, null=True, blank=True)
    edu = models.CharField(max_length=255, null=True, blank=True)
    dateStartEdu = models.CharField(max_length=255, null=True, blank=True)
    dateEndEdu = models.CharField(max_length=255, null=True, blank=True)
    eduInst = models.CharField(max_length=255, null=True, blank=True)
    serialDoc = models.CharField(max_length=255, null=True, blank=True)
    numDoc = models.CharField(max_length=255, null=True, blank=True)
    dateDoc = models.CharField(max_length=255, null=True, blank=True)
    PFM = models.CharField(max_length=255, null=True, blank=True)
    depName = models.CharField(max_length=255, null=True, blank=True)
    timeZone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    learnCode = models.CharField(max_length=255, null=True, blank=True)
    dateStartLearn = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='', null=True, blank=True, verbose_name="Фото")

    def serializer(self):
        if self.foto:
            fotoName = self.foto.name
            fotoPath = f'https://apiuc.hb.bizmrg.com/{MEDIA_ROOT}/{self.foto}'
            try:
                S3_foto = media_storage.open(self.foto.name, 'rb')
                fotoBase64 = json.dumps(S3_foto.read(), cls=Base64Encoder)[1:-1]
            except BaseException:
                fotoBase64 = "Не удалось преобразовать файл"
        else:
            fotoName = ''
            fotoPath = ''
            fotoBase64 = ''
        return {
            'id': self.id,
            'operationType': self.operationType,
            'idYL': self.idYL,
            'idPos': self.idPos,
            'FIO': self.FIO,
            'posName': self.posName,
            'birthday': self.birthday,
            'tabNum': self.tabNum,
            'phone': self.phone,
            'SNILS': self.SNILS,
            'dateEmployment': self.dateEmployment,
            'dateStartPos': self.dateStartPos,
            'edu': self.edu,
            'dateStartEdu': self.dateStartEdu,
            'dateEndEdu': self.dateEndEdu,
            'eduInst': self.eduInst,
            'serialDoc': self.serialDoc,
            'numDoc': self.numDoc,
            'dateDoc': self.dateDoc,
            'PFM': self.PFM,
            'depName': self.depName,
            'timeZone': self.timeZone,
            'address': self.address,
            'email': self.email,
            'learnCode': self.learnCode,
            'dateStartLearn': self.dateStartLearn,
            'fotoName': fotoName,
            'fotoPath': fotoPath,
            'foto': fotoBase64,
        }

    def __str__(self):
        return f'{self.SNILS} {self.learnCode} {self.dateStartLearn}'


class YcToBp(models.Model):
    id = models.AutoField(primary_key=True)
    bp_to_yc = models.OneToOneField(BpToYc, on_delete=models.CASCADE, related_name='yc_to_bp')
    operationType = models.CharField(max_length=255, verbose_name="Тип операции")
    tabNum = models.CharField(max_length=255, verbose_name="Табельный номер")
    FIO = models.CharField(max_length=255, null=True, verbose_name="ФИО")
    learnCode = models.CharField(max_length=255, verbose_name="Код обучения")
    courseCost = models.CharField(max_length=255, verbose_name="Стоимость курса")
    eduName = models.CharField(max_length=255, verbose_name="Наименование программы обучения")
    eduTime = models.CharField(max_length=255, verbose_name="Продолжительность обучения")
    eduUrl = models.CharField(max_length=255, verbose_name="Ссылка на курс обучения сотрудника")
    eduStatus = models.CharField(max_length=255, verbose_name="Статус обучения")
    result = models.CharField(max_length=255, verbose_name="Результат пр знаний")
    protocol = models.FileField(upload_to='', null=True, blank=True, verbose_name='Протокол')
    protocolNum = models.CharField(max_length=255, verbose_name="Номер протокола")
    protocolDate = models.CharField(max_length=255, verbose_name="Дата протокола")
    memberId1 = models.CharField(max_length=255, default="100999852", verbose_name="Член комиссии 1")
    memberId2 = models.CharField(max_length=255, default="100999853", verbose_name="Член комиссии 2")
    memberId3 = models.CharField(max_length=255, default="100999854", verbose_name="Член комиссии 3")
    cert = models.FileField(upload_to='', null=True, blank=True, verbose_name="Удостоверение")
    certDate = models.CharField(max_length=255, verbose_name="Дата удостоверения")
    certNum = models.CharField(max_length=255, verbose_name="Номер удостоверения")
    FGISNum = models.CharField(max_length=255, verbose_name="Номер ФГИС")
    platformStatus = models.CharField(max_length=255, verbose_name="Статус СДО")


   # id = models.AutoField(primary_key=True)
   # bp_to_yc = models.OneToOneField(BpToYc, on_delete=models.CASCADE, related_name='yc_to_bp')
   # operationType = models.CharField(max_length=255)
   # tabNum = models.CharField(max_length=255)
   # FIO = models.CharField(max_length=255, null=True)
   # learnCode = models.CharField(max_length=255)
   # courseCost = models.CharField(max_length=255)
   # eduName = models.CharField(max_length=255)
   # eduTime = models.CharField(max_length=255)
   # eduUrl = models.CharField(max_length=255)
   # eduStatus = models.CharField(max_length=255)
   # result = models.CharField(max_length=255)
   # protocol = models.FileField(upload_to='', null=True, blank=True, verbose_name='Протокол')
   # protocolNum = models.CharField(max_length=255)
   # protocolDate = models.CharField(max_length=255)
   # memberId1 = models.CharField(max_length=255)
   # memberId2 = models.CharField(max_length=255)
   # memberId3 = models.CharField(max_length=255)
   # cert = models.FileField(upload_to='', null=True, blank=True, verbose_name="Удостоверение")
   # certDate = models.CharField(max_length=255)
   # certNum = models.CharField(max_length=255)
   # FGISNum = models.CharField(max_length=255)
   # platformStatus = models.CharField(max_length=255)

    def serializer(self):
        if self.protocol:
            protocolName = self.protocol.name
            protocolPath = f'https://apiuc.hb.bizmrg.com/media/{self.protocol}'
            try:
                S3_protocol = media_storage.open(self.protocol.name, 'rb')
                protocolBase64 = json.dumps(S3_protocol.read(), cls=Base64Encoder)[1:-1]
            except BaseException:
                protocolBase64 = "Не удалось преобразовать файл"
        else:
            protocolName = ''
            protocolPath = ''
            protocolBase64 = ''
        if self.cert:
            certName = self.cert.name
            certPath = f'https://apiuc.hb.bizmrg.com/media/{self.cert}'
            try:
                S3_cert = media_storage.open(self.cert.name, 'rb')
                certBase64 = json.dumps(S3_cert.read(), cls=Base64Encoder)[1:-1]
            except BaseException:
                certBase64 = "Не удалось преобразовать файл"
        else:
            certName = ''
            certPath = ''
            certBase64 = ''

        return {
            'id': self.id,
            'operationType': self.operationType,
            'tabNum': self.tabNum,
            'FIO': self.FIO,
            'learnCode': self.learnCode,
            'courseCost': self.courseCost,
            'eduName': self.eduName,
            'eduTime': self.eduTime,
            'eduUrl': self.eduUrl,
            'eduStatus': self.eduStatus,
            'result': self.result,
            'protocolName': protocolName,
            'protocolPath': protocolPath,
           # 'protocolBase64': protocolBase64,
            'protocolNum': self.protocolNum,
            'protocolDate': self.protocolDate,
            'memberId1': self.memberId1,
            'memberId2': self.memberId2,
            'memberId3': self.memberId3,
            'certName': certName,
            'certPath': certPath,
           # 'certBase64': certBase64,
            'certDate': self.certDate,
            'certNum': self.certNum,
            'FGISNum': self.FGISNum,
            'platformStatus': self.platformStatus
        }
