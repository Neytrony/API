import os
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from djangoProject import settings
from drf_base64.serializers import ModelSerializer
from drf_extra_fields.fields import Base64ImageField
from .models import BpToYc, YcToBp
from djangoProject.s3_storage import MediaStorage
import imghdr


MEDIA_ROOT = settings.MEDIA_ROOT


class BpToYcSerializer(ModelSerializer):
    foto = Base64ImageField(required=False)

    class Meta:
        model = BpToYc
        fields = '__all__'

    def create(self, validated_data):
        duble = BpToYc.objects.filter(SNILS=validated_data['SNILS'], edu=validated_data['learnCode'], dateStartEdu=validated_data['dateStartLearn'])
        if duble.exists():
            instance = duble.first()
        else:
            instance = BpToYc()

        return Bp_To_Yc_cteate_or_update(instance, validated_data)


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


def Bp_To_Yc_cteate_or_update(instance, validated_data):
    for key, value in validated_data.items():
        if key == 'foto':
            removeOldFoto(instance.foto)
            filename = validated_data['tabNum'] + '_' + validated_data['learnCode'] + '_' + validated_data['dateStartLearn'] + '.' + imghdr.what(value)
            # file = MediaStorage().save(filename, value)
            file = FileSystemStorage().save(filename, value)
            instance.foto = file
        else:
            setattr(instance, key, value)
    instance.save()
    return instance


def removeOldFoto(filename):
    try:
        os.remove(f'{MEDIA_ROOT}/{filename}')
    except BaseException:
        pass
