from rest_framework import serializers
from .models import BpToYc, YcToBp
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class BpToYcSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpToYc
        fields = '__all__'

    def create(self, validated_data):
        duble = BpToYc.objects.filter(SNILS=validated_data['SNILS'], edu=validated_data['learnCode'], dateStartEdu=validated_data['dateStartLearn'])
        if duble.exists():
            duble.update(**validated_data)
            return BpToYc.objects.filter(SNILS=validated_data['SNILS'], edu=validated_data['learnCode'], dateStartEdu= validated_data['dateStartLearn']).first()
        else:
            return BpToYc.objects.create(**validated_data)



class YcToBpSerializer(serializers.ModelSerializer):
    class Meta:
        model = YcToBp
        fields = '__all__'

    def create(self, validated_data):
        return YcToBp.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()