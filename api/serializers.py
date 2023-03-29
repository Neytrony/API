from rest_framework import serializers
from .models import BpToYc, YcToBp
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class BpToYcSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpToYc
        fields = '__all__'

    def create(self, validated_data):
        defaults = {}
        print(validated_data)
        for key, value in validated_data.items():
            if key != 'SNILS':
                defaults[key] = value

        print(defaults)
        answer, created = BpToYc.objects.update_or_create(SNILS=validated_data['SNILS'], defaults=defaults)
        return answer


class YcToBpSerializer(serializers.ModelSerializer):
    class Meta:
        model = YcToBp
        fields = '__all__'

    def create(self, validated_data):
        return YcToBp.objects.create(**validated_data)
