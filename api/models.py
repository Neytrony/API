import json
import base64

from django.db import models


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
            'fotoName': self.foto.name,
            'fotoPath': f'https://apiuc.hb.bizmrg.com/{self.foto.url}',
            'foto': json.dumps(open(self.foto.path, 'rb').read(), cls=Base64Encoder)[1:-1],
        }

    def __str__(self):
        return f'{self.SNILS} {self.learnCode} {self.dateStartLearn}'


class YcToBp(models.Model):
    bp_to_yc = models.OneToOneField(BpToYc, on_delete=models.CASCADE, primary_key=True, related_name='yc_to_bp')
    operationType = models.CharField(max_length=255)
    tabNum = models.CharField(max_length=255)
    FIO = models.CharField(max_length=255, null=True)
    learnCode = models.CharField(max_length=255)
    courseCost = models.CharField(max_length=255)
    eduName = models.CharField(max_length=255)
    eduTime = models.CharField(max_length=255)
    eduUrl = models.CharField(max_length=255)
    eduStatus = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    protocol = models.FileField(upload_to='', null=True, blank=True, verbose_name='Протокол')
    protocolNum = models.CharField(max_length=255)
    protocolDate = models.CharField(max_length=255)
    memberId1 = models.CharField(max_length=255)
    memberId2 = models.CharField(max_length=255)
    memberId3 = models.CharField(max_length=255)
    cert = models.FileField(upload_to='', null=True, blank=True, verbose_name="Удостоверение")
    certDate = models.CharField(max_length=255)
    certNum = models.CharField(max_length=255)
    FGISNum = models.CharField(max_length=255)
    platformStatus = models.CharField(max_length=255)

    def serializer(self):
        if self.protocol:
            protocolName = self.protocol.name
            protocolPath = f'https://apiuc.hb.bizmrg.com/{self.protocol.path}'
            protocolBase64 = json.dumps(open(self.protocol.path, 'rb').read(), cls=Base64Encoder)[1:-1]
        else:
            protocolName = ''
            protocolPath = ''
            protocolBase64 = ''
        if self.cert:
            certName = self.cert.name
            certPath = f'https://apiuc.hb.bizmrg.com/{self.cert.path}'
            certBase64 = json.dumps(open(self.cert.path, 'rb').read(), cls=Base64Encoder)[1:-1]
        else:
            certName = ''
            certPath = ''
            certBase64 = ''

        return {
            'input_model': self.bp_to_yc.serializer(),
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
            'protocolBase64': protocolBase64,
            'protocolNum': self.protocolNum,
            'protocolDate': self.protocolDate,
            'memberId1': self.memberId1,
            'memberId2': self.memberId2,
            'memberId3': self.memberId3,
            'certName': certName,
            'certPath': certPath,
            'certBase64': certBase64,
            'certDate': self.certDate,
            'certNum': self.certNum,
            'FGISNum': self.FGISNum,

        }
