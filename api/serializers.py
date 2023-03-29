from rest_framework import serializers
from .models import BpToYc, YcToBp
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class BpToYcSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpToYc
        fields = '__all__'

    def create(self, validated_data):
        answer, created = BpToYc.objects.update_or_create(SNILS=validated_data['SNILS'],
           defaults={
               'operationType': validated_data['operationType'],
               'idYL': validated_data['idYL'],
               'idPos': validated_data['idPos'],
               'FIO': validated_data['FIO'],
               'posName': validated_data['posName'],
               'birthday': validated_data['birthday'],
               'tabNum': validated_data['tabNum'],
               'phone': validated_data['phone'],
               'dateEmployment': validated_data['dateEmployment'],
               'dateStartPos': validated_data['dateStartPos'],
               'edu': validated_data['edu'],
               'dateStartEdu': validated_data['dateStartEdu'],
               'dateEndEdu': validated_data['dateEndEdu'],
               'eduInst': validated_data['eduInst'],
               'serialDoc': validated_data['serialDoc'],
               'numDoc': validated_data['numDoc'],
               'dateDoc': validated_data['dateDoc'],
               'PFM': validated_data['PFM'],
               'depName': validated_data['depName'],
               'timeZone': validated_data['timeZone'],
               'address': validated_data['address'],
               'email': validated_data['email'],
               'learnCode': validated_data['learnCode'],
               'dateStartLearn': validated_data['dateStartLearn'],
           })
        return answer


class YcToBpSerializer(serializers.ModelSerializer):
    class Meta:
        model = YcToBp
        fields = '__all__'

    def create(self, validated_data):
        return YcToBp.objects.create(**validated_data)
