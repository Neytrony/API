from rest_framework import serializers
from .models import BpToYc, YcToBp

class BpToYcSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpToYc
        fields = '__all__'

    def create(self, validated_data):
        return BpToYc.objects.create(**validated_data)

class YcToBpSerializer(serializers.ModelSerializer):
    class Meta:
        model = YcToBp
        fields = '__all__'

    def create(self, validated_data):
        return YcToBp.objects.create(**validated_data)