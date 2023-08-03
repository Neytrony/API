from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import SoutToAc, SoutFromAc, Employee, RM, ResultMapSOUT, BadFactor, CommissionMember
from rest_framework.response import Response
from rest_framework import viewsets, permissions, views
from django.db.models import Q
from django.db import transaction


modelDict = {
    "employees": {
        'model': Employee,
        'unique_params': ['SNILS'],
        'fk_rel':  {
            'field': 'soutToAc',
        },
    },
    "RMs": {
        'model': RM,
        'unique_params': ['amountRM', 'numberRM'],
        'fk_rel': {
            'field': 'soutToAc',
        },
    },
    "earlierSOUT": {
        'model': ResultMapSOUT,
        'unique_params': ['numberSOUT'],
        'fk_rel': {
            'field': 'soutToAc',
        },
    },
    "commissionMembers": {
        'model': CommissionMember,
        'unique_params': ['FIO', 'position'],
        'fk_rel': {
            'field': 'soutToAc',
        },
    },
    "badFactors": {
        'model': BadFactor,
        'unique_params': ['badFactor'],
        'fk_rel': {
            'field': 'resultMapSOUT',
        },
    },
}


class SoutFromAcAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        return Response([obj.serializer() for obj in queryset])

    def get_queryset(self):
        queryset = SoutFromAc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        my_dict = dict()
        for key, value in query_params_dict.items():
            new_key = f'{key}__in'
            my_dict[new_key] = value
        queryset = queryset.filter(Q(**my_dict))
        return queryset


class OneSoutFromAcAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cardNum):
        queryset = self.get_queryset(cardNum)
        if queryset:
            return Response([obj.serializer() for obj in queryset], HTTP_200_OK)
        else:
            return Response({'message': f'Object with cardNum = {cardNum} not found.'}, HTTP_404_NOT_FOUND)

    def get_queryset(self, cardNum):
        queryset = SoutFromAc.objects.filter(cardNum=cardNum)
        return queryset


class SoutToAcAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        return Response([obj.serializer() for obj in queryset])

    def get_queryset(self):
        queryset = SoutToAc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        my_dict = dict()
        for key, value in query_params_dict.items():
            new_key = f'{key}__in'
            my_dict[new_key] = value
        queryset = queryset.filter(Q(**my_dict))
        return queryset

    def post(self, request):
        data = request.data
        result = []
        for validated_data in data:
            result.append(model_obj_create_or_update(SoutToAc, ['cardNum'], validated_data))
            SoutFromAc.objects.update_or_create(cardNum=validated_data['cardNum'])
        return Response([res.serializer() for res in result])


def model_obj_create_or_update(model, unique_params, validated_data, fk_rel=None):
    unique_params_dict = {key: validated_data[key] for key in unique_params}
    if fk_rel is not None:
        unique_params_dict[fk_rel['field']] = fk_rel['extra_instance']
    duble = model.objects.filter(**unique_params_dict)
    if duble.exists():
        instance = duble.first()
    else:
        instance = model.objects.create(**unique_params_dict)
    return obj_create_or_update(instance, validated_data, fk_rel)


@transaction.atomic
def obj_create_or_update(instance, validated_data, fk_rel=None):
    fk_fields_list = modelDict.keys()
    for key, value in validated_data.items():
        if key not in fk_fields_list:
            setattr(instance, key, value)
        else:
            extra_model = modelDict[key]['model']
            extra_dict = modelDict[key]['fk_rel']
            extra_params = modelDict[key]['unique_params']
            extra_dict['extra_instance'] = instance

            extra_model.objects.filter(**{extra_dict['field']: instance}).delete()
            for extra_value in value:
                model_obj_create_or_update(extra_model, extra_params, extra_value, extra_dict)
    if fk_rel is not None:
        setattr(instance, fk_rel['field'], fk_rel['extra_instance'])
    instance.save()
    return instance
