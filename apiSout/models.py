from django.db import models


class SoutFromAc(models.Model):
    cardNum = models.CharField(max_length=255, null=False, verbose_name='Номер карты', primary_key=True, unique=True)
    analogPlaceAmount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Кол-во аналогичных мест')
    analogPlaceNum = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер аналогичного места')
    finalWorkingConditionClass = models.CharField(max_length=255, blank=True, null=True, verbose_name='Итоговый класс (подкласс) условий труда')
    chemical = models.CharField(max_length=255, null=True, blank=True, verbose_name='Химический')
    biological = models.CharField(max_length=255, null=True, blank=True, verbose_name='Биологический')
    aerosols = models.CharField(max_length=255, null=True, blank=True, verbose_name='Аэрозоли')
    noise = models.CharField(max_length=255, null=True, blank=True, verbose_name='Шум')
    infraSound = models.CharField(max_length=255, null=True, blank=True, verbose_name='Инфрозвук')
    airUltraSound = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ультразвук воздушный')
    generalVibration = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вибрация общая')
    localVibration = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вибрация локальная')
    nonIonizingRadiation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Неионизирующие излучения')
    ionizingRadiation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ионизирующие излучения')
    microClimateParams = models.CharField(max_length=255, null=True, blank=True, verbose_name='Параметры микроклимата')
    lightEnvParams = models.CharField(max_length=255, null=True, blank=True, verbose_name='Параметры световой среды')
    hardshipWorkProcess = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тяжесть трудового процесса')
    intensityWorkProcess = models.CharField(max_length=255, null=True, blank=True, verbose_name='Напряженность трудового процесса')
    increasedEmployeePay = models.CharField(max_length=255, null=True, blank=True, verbose_name='Повышенная оплата труда работника (работников)')
    annualAddPaidHoliday = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ежегодный дополнительный оплачиваемый отпуск')
    shortenedWorkTime = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сокращенная продолжительность рабочего времени')
    milk = models.CharField(max_length=255, null=True, blank=True, verbose_name='Молоко или другие равноценные пищевые продукты')
    therapeuticNutrition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Лечебно - профилактическое питание')
    earlyPension = models.CharField(max_length=255, null=True, blank=True, verbose_name='Право на досрочное назначение страховой пенсии')
    carryingMedInspections = models.CharField(max_length=255, null=True, blank=True, verbose_name='Проведение медицинских осмотров')
    recommendations = models.CharField(max_length=255, null=True, blank=True, verbose_name='Рекомендации')
    improvements = models.CharField(max_length=255, null=True, blank=True, verbose_name='Улучшения')
    improvementsText = models.CharField(max_length=255, null=True, blank=True, verbose_name='Текстовое поле улучшений')
    womenLabor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Труд женщин')
    laborUnder18 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Труд до 18 лет')
    invalids = models.CharField(max_length=255, null=True, blank=True, verbose_name='Инвалиды')
    operationMode = models.CharField(max_length=255, null=True, blank=True, verbose_name='Режим работы (текстовое поле рекомендаций)')
    expertGUID = models.CharField(max_length=255, null=True, blank=True, verbose_name='GUID эксперта')
    employeeSNILS = models.CharField(max_length=255, null=True, blank=True, verbose_name='Снилс работника ')
    linkMapSout = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка на документ карта СОУТ')
    protocolAmount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Кол-во протоколов к карте')
    protocolNum = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер протокола')
    protocolDate = models.CharField(max_length=255, null=True, blank=True, verbose_name='дата протокола')
    protocolType = models.CharField(max_length=255, null=True, blank=True, verbose_name='тип протокола (тяжесть и т.п.)')
    measurementDate = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата измерений')
    conclusion = models.CharField(max_length=255, null=True, blank=True, verbose_name='Заключение')
    engineerFIO = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фио инженера')
    engineerPosition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Должность инженера')
    expertFIO = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фио эксперта')
    expertPosition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Должность эксперта')
    registerExpertsNum = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер в реестре экспертов')
    linkProtocol = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка на протокол')
    cardCost = models.CharField(max_length=255, null=True, blank=True, verbose_name='Стоимость карты')

    def serializer(self):
        return {
            'cardNum': self.cardNum,
            'analogPlaceAmount': self.analogPlaceAmount,
            'analogPlaceNum': self.analogPlaceNum,
            'finalWorkingConditionClass': self.finalWorkingConditionClass,
            'chemical': self.chemical,
            'biological': self.biological,
            'aerosols': self.aerosols,
            'noise': self.noise,
            'infraSound': self.infraSound,
            'airUltraSound': self.airUltraSound,
            'generalVibration': self.generalVibration,
            'localVibration': self.localVibration,
            'nonIonizingRadiation': self.nonIonizingRadiation,
            'ionizingRadiation': self.ionizingRadiation,
            'microClimateParams': self.microClimateParams,
            'lightEnvParams': self.lightEnvParams,
            'hardshipWorkProcess': self.hardshipWorkProcess,
            'intensityWorkProcess': self.intensityWorkProcess,
            'increasedEmployeePay': self.increasedEmployeePay,
            'annualAddPaidHoliday': self.annualAddPaidHoliday,
            'shortenedWorkTime': self.shortenedWorkTime,
            'milk': self.milk,
            'therapeuticNutrition': self.therapeuticNutrition,
            'earlyPension': self.earlyPension,
            'carryingMedInspections': self.carryingMedInspections,
            'recommendations': self.recommendations,
            'improvements': self.improvements,
            'improvementsText': self.improvementsText,
            'womenLabor': self.womenLabor,
            'laborUnder18': self.laborUnder18,
            'invalids': self.invalids,
            'operationMode': self.operationMode,
            'expertGUID': self.expertGUID,
            'employeeSNILS': self.employeeSNILS,
            'linkMapSout': self.linkMapSout,
            'protocolAmount': self.protocolAmount,
            'protocolNum': self.protocolNum,
            'protocolDate': self.protocolDate,
            'protocolType': self.protocolType,
            'measurementDate': self.measurementDate,
            'conclusion': self.conclusion,
            'engineerFIO': self.engineerFIO,
            'engineerPosition': self.engineerPosition,
            'expertFIO': self.expertFIO,
            'expertPosition': self.expertPosition,
            'registerExpertsNum': self.registerExpertsNum,
            'linkProtocol': self.linkProtocol,
            'cardCost': self.cardCost,
        }

    class Meta:
        verbose_name = 'Исходящие данные СОУТ'
        verbose_name_plural = 'Исходящие данные СОУТ'

    def __str__(self):
        return f'{self.cardNum}'


# Create your models here.
class SoutToAc(models.Model):
    cardNum = models.CharField(max_length=255, null=False, verbose_name='Номер карты', primary_key=True, unique=True)
    soutAddress = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес проведения СОУТ')
    badFactorsSout = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вредные факторы СОУТ')
    badFactorsMO = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вредные факторы МО')
    badWorkMO = models.CharField(max_length=255, null=False, verbose_name='Вредные работы МО')
    usedSIZ = models.CharField(max_length=255, null=True, blank=True, verbose_name='Используемые СИЗ')
    usedMaterials = models.CharField(max_length=255, null=True, blank=True, verbose_name='Используемые материалы и сырье')
    usedEquipment = models.CharField(max_length=255, null=False, blank=True, verbose_name='Используемое оборудование в работе')
    dateOpenRM = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата открытия Р/М')
    addAgreementNum = models.CharField(max_length=255, null=False, verbose_name='Номер ДопСог')
    positionSOUT = models.CharField(max_length=255, null=True, blank=True, verbose_name='Должность в Карте СОУТ')
    codeOK = models.CharField(max_length=255, null=True, blank=True, verbose_name='Код по ОК - 016-94')
    ETKS = models.CharField(max_length=255, null=True, blank=True, verbose_name='Выпуск по ЕТКС,ЕКС')
    numPFM = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название подразделения (номер ПФМ)')
    employeesAmount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество сотрудников в карте')
    FC = models.CharField(max_length=255, null=True, blank=True, verbose_name='ФС')
    subdivisionVY = models.CharField(max_length=255, null=True, blank=True, verbose_name='Подразделение ВУ')
    employerName = models.CharField(max_length=255, null=True, blank=True, verbose_name='Наименование работодателя')
    fioGD = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фио ГД')
    yrAddress = models.CharField(max_length=255, null=True, blank=True, verbose_name='Юр адрес')
    INN = models.CharField(max_length=255, null=True, blank=True, verbose_name='ИНН')
    OKPO = models.CharField(max_length=255, null=True, blank=True, verbose_name='ОКПО')
    OKOGY = models.CharField(max_length=255, null=True, blank=True, verbose_name='ОКОГУ')
    OKVED = models.CharField(max_length=255, null=True, blank=True, verbose_name='ОКВЭД')
    OKTMO = models.CharField(max_length=255, null=True, blank=True, verbose_name='ОКТМО')
    latestDateSOUT = models.CharField(max_length=255, null=True, blank=True, verbose_name='Крайняя дата проведения СОУТ')
    earlierResultSOUT = models.CharField(max_length=255, null=True, blank=True, verbose_name='Результаты ранее проведенных СОУТ')
    commissionMembersAmount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Число членов комиссии')
    fioChairman = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фио председателя')
    positionChairman = models.CharField(max_length=255, null=True, blank=True, verbose_name='Должность председателя')
    linkCommissionCreation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка на приказ о создании комиссии')
    linkPMListSOUT = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка на перечень РМ подлежащих СОУТ')

    def serializer(self):
        return {
            'cardNum': self.cardNum,
            'soutAddress': self.soutAddress,
            'badFactorsSout': self.badFactorsSout,
            'badFactorsMO': self.badFactorsMO,
            'badWorkMO': self.badWorkMO,
            'usedSIZ': self.usedSIZ,
            'usedMaterials': self.usedMaterials,
            'usedEquipment': self.usedEquipment,
            'dateOpenRM': self.dateOpenRM,
            'addAgreementNum': self.addAgreementNum,
            'positionSOUT': self.positionSOUT,
            'codeOK': self.codeOK,
            'ETKS': self.ETKS,
            'numPFM': self.numPFM,
            'employeesAmount': self.employeesAmount,
            'employees': [obj.serializer() for obj in self.employees.all()],
            'FC': self.FC,
            'subdivisionVY': self.subdivisionVY,
            'employerName': self.employerName,
            'fioGD': self.fioGD,
            'yrAddress': self.yrAddress,
            'INN': self.INN,
            'OKPO': self.OKPO,
            'OKOGY': self.OKOGY,
            'OKVED': self.OKVED,
            'OKTMO': self.OKTMO,
            'latestDateSOUT': self.latestDateSOUT,
            'earlierResultSOUT': self.earlierResultSOUT,
            'earlierSOUT': [obj.serializer() for obj in self.earlierSOUT.all()],
            'RMs': [obj.serializer() for obj in self.RMs.all()],
            'commissionMembersAmount': self.commissionMembersAmount,
            'fioChairman': self.fioChairman,
            'positionChairman': self.positionChairman,
            'commissionMembers': [obj.serializer() for obj in self.commissionMembers.all()],
            'linkCommissionCreation': self.linkCommissionCreation,
            'linkPMListSOUT': self.linkPMListSOUT,
        }

    def __str__(self):
        return f'{self.cardNum}'

    class Meta:
        verbose_name = 'Входящие данные СОУТ'
        verbose_name_plural = 'Входящие данные СОУТ'


class Employee(models.Model):
    TN = models.CharField(max_length=255, null=True, blank=True, verbose_name='ТН сотрудника')
    SNILS = models.CharField(max_length=255, null=True, blank=True, verbose_name='Снилс сотрудника')
    surname = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия сотрудника')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя сотрудника')
    secondName = models.CharField(max_length=255, null=True, blank=True, verbose_name='Отчество сотрудника')
    birthDate = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата рождения сотрудника')
    gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='Пол сотрудника')
    invalid = models.CharField(max_length=255, null=True, blank=True, verbose_name='Инвалид')
    soutToAc = models.ForeignKey(SoutToAc, related_name='employees', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сотрудник')

    def __str__(self):
        return f'{self.SNILS}; {self.surname} {self.name} {self.secondName}'

    def serializer(self):
        return {
            'TN': self.TN,
            'SNILS': self.SNILS,
            'surname': self.surname,
            'name': self.name,
            'secondName': self.secondName,
            'birthDate': self.birthDate,
            'gender': self.gender,
            'invalid': self.invalid
        }

    class Meta:
        unique_together = [["SNILS", "soutToAc"]]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class RM(models.Model):
    amountRM = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество аналогичных Р/М')
    numberRM = models.CharField(max_length=255, null=True, blank=True, verbose_name='номер Р/М')
    soutToAc = models.ForeignKey(SoutToAc, related_name='RMs', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Р/М')

    def __str__(self):
        return f'{self.amountRM}; {self.numberRM}'

    def serializer(self):
        return {
            'amountRM': self.amountRM,
            'numberRM': self.numberRM
        }

    class Meta:
        unique_together = [["numberRM", "soutToAc"]]
        verbose_name = 'Р/М'
        verbose_name_plural = 'Р/М'


class CommissionMember(models.Model):
    FIO = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фио члена комиссии')
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name='Должность члена комиссии')
    soutToAc = models.ForeignKey(SoutToAc, related_name='commissionMembers', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Член комиссии')

    def __str__(self):
        return f'{self.FIO}; {self.position}'

    def serializer(self):
        return {
            'FIO': self.FIO,
            'position': self.position,
        }

    class Meta:
        unique_together = [["FIO", "soutToAc"]]
        verbose_name = 'Член комиссии'
        verbose_name_plural = 'Члены комиссии'


class ResultMapSOUT(models.Model):
    numberSOUT = models.CharField(max_length=255, null=True, blank=True, verbose_name='Номер прошлой карты СОУТ')
    agreementDate = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата утверждения отчета прошлой СОУТ')
    workingConditionClass = models.CharField(max_length=255, null=True, blank=True, verbose_name='Класс условий труда прошлой СОУТ')
    soutToAc = models.ForeignKey(SoutToAc, related_name='earlierSOUT', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Результат прошлой СОУТ')

    def __str__(self):
        return f'{self.numberSOUT}; {self.agreementDate}'

    def serializer(self):
        return {
            'numberSOUT': self.numberSOUT,
            'agreementDate': self.agreementDate,
            'workingConditionClass': self.workingConditionClass,
            'badFactors': [obj.serializer() for obj in self.badFactors.all()]
        }

    class Meta:
        unique_together = [["numberSOUT", "soutToAc"]]
        verbose_name = 'Ранее проведенный СОУТ'
        verbose_name_plural = 'Ранее проведенные СОУТ'


class BadFactor(models.Model):
    badFactor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вредные фактор прошлой СОУТ')
    factorConditionClass = models.CharField(max_length=255, null=True, blank=True, verbose_name='Класс условий фактора')
    resultMapSOUT = models.ForeignKey(ResultMapSOUT, related_name='badFactors', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Вредный фактор')

    def __str__(self):
        return f'{self.badFactor}; {self.factorConditionClass}'

    def serializer(self):
        return {
            'badFactor': self.badFactor,
            'factorConditionClass': self.factorConditionClass
        }

    class Meta:
        unique_together = [["badFactor", "resultMapSOUT"]]
        verbose_name = 'Вредный фактор'
        verbose_name_plural = 'Вредные факторы'
