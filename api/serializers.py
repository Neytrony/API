from rest_framework import serializers
from .models import BC_TO_YC, YC_TO_BC


class BC_TO_YC_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BC_TO_YC
        fields = '__all__'

    def create(self, validated_data):
        return BC_TO_YC.objects.create(**validated_data)

class YC_TO_BC_Serializer(serializers.ModelSerializer):
    class Meta:
        model = YC_TO_BC
        fields = '__all__'

    def create(self, validated_data):
        return YC_TO_BC.objects.create(**validated_data)