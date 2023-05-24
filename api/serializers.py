import base64
import os

from django.core.files.base import ContentFile
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
        duble = BpToYc.objects.filter(SNILS=validated_data['SNILS'], learnCode=validated_data['learnCode'],
                                      dateStartLearn=validated_data['dateStartLearn'])
        if duble.exists():
            instance = duble.first()
        else:
            instance = BpToYc.objects.create()
            YcToBp.objects.create(bp_to_yc=instance)
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
    extra_fields = ['operationType', 'FIO', 'tabNum', 'learnCode']
    for key, value in validated_data.items():
        if key == 'foto':
            removeOldFoto(instance.foto)
            decoded_value = base64.b64decode(value)
            filename = validated_data['tabNum'] + '_' + validated_data['learnCode'] + '_' + validated_data['dateStartLearn'] + '.' + imghdr.what('', decoded_value)
            # file = MediaStorage().save(filename, ContentFile(decoded_value, name=filename))
            file = FileSystemStorage().save(filename, ContentFile(decoded_value, name=filename))
            instance.foto = file
        elif key in extra_fields:
            setattr(instance, key, value)
            setattr(instance.yc_to_bp, key, value)
        else:
            setattr(instance, key, value)
    instance.yc_to_bp.save()
    instance.save()
    return instance


def removeOldFoto(filename):
    try:
        os.remove(f'{MEDIA_ROOT}/{filename}')
    except BaseException:
        pass
